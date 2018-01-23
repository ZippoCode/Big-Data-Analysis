Algoritmo Apriori
==========

Implentazione in Python dell'algoritmo Apriori

Descrizione
-------------

L'algoritmo Apriori è il più noto per quanto riguarda la ricerca degli itemset più frequenti e si basa su due step. 

* **Primo step**: Crea due tabelle

	- Nella prima tabella trasforma i nomi degli item in interi
	- Nella seconda invece inserisce il conteggio degli item (inizialmente sono tutti settati a 0)
	
* **Al secondo step**: calcolo item set più frequenti
	In questo passaggio tramite un doppio ciclo di for calcola gli item set più frequenti. In particolare al primo step nella seconda matrice, calcolato nello step precedente, inserisce i *singoletti* e successivamente elimina quelli che non superano una certa soglia. Successivamente da questi costruisce le *tuple* e di nuovo calcola la frequenza di ognuna di esse ed elimina quelli non frequenti. L'algoritmo procede così finché non è più possibile costruire nuovi item. 
	
I passaggi dell'algoritmo sono i seguenti
> Filtro -> Verifica -> Filtro -> Verifica


Descrizione file *apriori.py*
----------------------------
Inzialmente viene letto il file *INTEGRATED-DATASET* e successivamente viene invocato il metodo *runApriori*. Al'interno di questo metodo vengono creati:
	
* Una lista che contiene tutti gli item
* Un set contenente tutte le transizioni (le righe del file .cvs)

Successivamente calcola gli item più frequenti all'interno delle transizioni tramite il metodo *returnItemsWithMinSupport*

```
        for item in itemSet:
                for transaction in transactionList:
                        if item.issubset(transaction):
                                freqSet[item] += 1
                                localSet[item] += 1

        for item, count in localSet.items():
                support = float(count)/len(transactionList)

                if support >= minSupport:
                        _itemSet.add(item)

        return _itemSet
```

Successivamente collega tra gli loro gli item set, prima a coppie, poi a triple ecc.., e calcola ad ogni iterazione quelle che hanno un valore di support maggiore della soglia minima. Il ciclo termina quando non è più possibile generare dei nuovi collegamenti tra gli item.

Come ultimo step applica la *potatura* degli itemset meno frequenti.

    for key, value in list(largeSet.items())[1:]:
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSupport(item) / getSupport(element)
                    if confidence >= minConfidence:
                        toRetRules.append(((tuple(element), tuple(remain)), confidence))
Lista di file
------------
I file contenuti sono i sequenti:

1. **priory.py** : Implementazione dell'algoritmo
2. **INTEGRATED-DATASET.csv**:  Scaricato presso il sequente sito web [link]()
3. **README.md**


Come si usa:
--------------

Per eseguire il programma spostarsi nella cartella contente il file ed eseguire
> python apriori.py -f INTEGRATED-DATASET.csv

Oppure se si vuole specificare support e confidenza
> python apriori.py -f INTEGRATED-DATASET.csv -s 0.17 -c 0.68

