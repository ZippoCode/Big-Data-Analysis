import random
import numpy as np
import scipy.optimize as op
from hashlib import md5
from sortedcontainers import SortedSet
from nltk import ngrams
from sklearn.metrics import jaccard_similarity_score


def shingle_text(text: str, k):
    """
    Prende una linea e la partiziona in hashed (di quattro byte) shingles
    di lunghezza k

    :param text: stringa contenente il testo
    :param k: il numero di caratteri in un shingle
    :return:
        Un set ordinato contenente tutti gli hashes
    """
    shingled_text = SortedSet()
    text = text.replace('\n', '').replace('\r', '')
    # Shingles dei caratteri (i spazi vengono conteggiati come caratteri)
    kgram = ngrams(text, k)
    for gram in kgram:
        # Crea un Hash dei shingle con MD5 dentro un token 4 byte (8 esadecimali)
        # Tutte le combinazioni di 8 caratteri di tipo esadecimale sono tutti possibili
        # shingle hash
        text_gram = ''.join(gram).encode('utf-8')
        shingled_text.add(int(md5(text_gram).hexdigest()[0:8], 16))
    return shingled_text


def compareSignatures(sig1, sig2):
    """
    Confronta due array di interi (hanno la stessa lunghezza) considerando
    quanti sono quanti sono gli interi uguali per ogni posizione

    :param sig1:
    :param sig2:
    :return:
         
    """
    return jaccard_similarity_score(sig1, sig2)


def minHashing(allSets, num_function=100):
    """
    Costruisce un minhash signature per tutte i sets. Il numero si signature
    viene passato come parametro. Di defaut sono 100

    :param allSets:
    :param num_function: il numero di hash che si vuole generare
    :return:
    """
    print('Elaborazione Min-Hashing...')
    # Unisce (Operazione di OR) tutte gli hash che sono in un sets
    # E' importante notare che le operazioni avverranno solo su di esse perché
    # la altre colonne saranno zero per tutti gli altri documenti
    U = SortedSet()
    for i in range(0, len(allSets)):
        U |= allSets[i]  # Operazione di OR

    # Per evitare collisione si crea un numero di bucket nell'hash molto grande
    # Idealmente, questo numero dovrebbe essere più grande di 2^32 (numero degli shingle hash), ma al fine di
    # avere una lista di bucket ragionevole nella funzione LSH si è ridotto il valore del modulo
    mod = 2971215073
    # Inoltre si è scelto valori alti dei parametri per il modulo per evitare funzioni di hash
    # che non permutino le colonne (equivalentemente alla funzione identità)
    low = 1000
    high = 1000000
    functions = []
    for i in range(0, num_function):
        def function(x):
            a = random.randint(low, high)
            b = random.randint(low, high)
            return (a * x + b) % mod

        functions.append(function)

    # ALGORITMO MIN-HASHING
    Mic = [[float("inf")] * len(allSets) for i in range(num_function)]  # Inizialmente le istanze sono infinito
    i = 1

    # Si itera sull'unione di tutti i shingles hash
    for u in U:
        hr = []
        # Calcolo funzione hash per ogni specifica riga
        for h in range(0, len(functions)):
            result = functions[h](i)
            hr.append(result)
        c_count = 0
        # Iterazione sulle colonne
        for c in allSets:
            if (c.__contains__(u)):  # Se la colonna contiene il valore u
                for hh in range(0, len(functions)):
                    if (hr[hh] < Mic[hh][c_count]):
                        Mic[hh][c_count] = hr[hh]
            c_count += 1
        i += 1

    return Mic


def LSH(signature_vectors, threshold):
    """
    Calcola in modo efficiente tutte le coppie di documenti che sono, con molto probabilità,
    sopra (oppure molto vicini) alla soglia predefinita di somiglianza.

    :param signature_vectors:
    :param threshold:
    :return:
    """
    print('Elaborazione LSH...')
    sign_length = len(signature_vectors[0])  # Lunghezza delle colonne
    print('Threshold richiesta:', threshold)
    root_res = op.root(lambda r: (r / sign_length) ** (1 / r) - threshold, 2)
    # la funzione 'r' definita sopra potrebbe non divedere esattamente sign_lenght
    # L'ultima riga potrebbe essere più piccola
    r = int(root_res['x'][0])
    print('Numero di righe in bande da LSH:', r)

    candidate_pairs = set()
    start_idx = 0
    end_idx = r

    # Per ogni banda della signature
    while start_idx < sign_length:

        hash_buckets = [[-1]] * (2 ** 16)
        for doc in range(len(signature_vectors)):
            string = ''.join(str(signature_vectors[doc][start_idx:end_idx])).encode('utf-8')
            to_bucket = int(md5(string).hexdigest()[0:4], 16)
            # print(to_bucket)
            if hash_buckets[to_bucket][0] == -1:
                hash_buckets[to_bucket] = [doc]
            else:
                for doc_in_bucket in hash_buckets[to_bucket]:
                    candidate_pairs.add((doc_in_bucket, doc))
                hash_buckets[to_bucket].append(doc)

        start_idx = start_idx + r
        end_idx = end_idx + r
        if end_idx > sign_length:
            end_idx = sign_length
    return candidate_pairs


if __name__ == '__main__':
    file = open('dataset.txt', 'r')
    allSets = []
    for line in file.readlines():
        allSets.append(shingle_text(line, 10))
    signature_matrix = np.array(minHashing(allSets, 100)).T
    coppie_candidate = LSH(signature_matrix, 0.8)
    similar_pairs = []
    for pair in coppie_candidate:
        if(compareSignatures(signature_matrix[pair[0]], signature_matrix[pair[1]])):
            similar_pairs.append(pair)

    print(similar_pairs)