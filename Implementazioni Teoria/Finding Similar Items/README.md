Finding Similar Items
============

Implementazione dell'algoritmo di *Finding Similar Items* in Python.

Descrizione:
-------------
Questo algoritmo si applica ai documenti, siti web e altri file in formato testuale per la ricerca di termini simili. Le fasi che descrivono il procedimento sono le seguenti:

<p align="center">
  <img width="460" height="300" src="https://i.imgur.com/GZnisl0.png">
</p>
###Documents
Il documento viene caricato

### Shipling
Il documento viene convertito in dei *sets*. In particolare ognuno di essi rappresenta una stringa di lunghezza relativamente breve del documento iniziale. Viene quindi definito un **k-shingle** cioè una sottostringa del documento di lunghezza k. Quindi al documento viene associato un set di k-shingle che appaiono una o più volte al suo interno. Ad esempio:
>Avendo un documento composto da una stringa 'abcab' e settando k uguale a 2 si ottiene: 
S(D) = {ab, bc, ca}

Un'opzione è quella di rappresentare i singles con degli *hash* per ridurre lo spazio occupato in memoria. Infatti se ad esempio si utilizza un hash di 4 byte e un *9-shingles* si ha che nel primo caso si utilizzano 18 byte mentre nel secondo 8. 
> (aaabbbccc) (abcabcabc) utilizzano 18 byte
>h(aaabbbccc) h(abcabcabc) utiizzano 8 byte

#### Min-Hashing
Poiché la rappresentazione degli shingles nella forma matriciale non è efficiace in tempi di tempi computazioni (sono presenti troppe righe) viene utilizzata la tecnica del *Min-Hashing* che tramite le *Signature* crea una nuova matrice di dimensioni ridotte. In particolare vengono creati degli hash che codifichino i dati. 
E' importante prestare però attenzione al concetto di similarità tra due hash, infatti si possono trovare due casi:
> sim(C1, C2) è alta quando è alta la probabilità che h(C1) = h(C2)
> sim(C1, C2) è alta quando è bassa quando la probabilità che h(C1) sia diverso da h(C2) sia alta

La figura riassume il concetto di Min-Hashing
![fig](imgs/20180123-222657.png)

La probabilità che il minhash per una permutazione casuale delle righe produca lo stesso valore per due set è uquale alla similarità dei set. Ad esempio osservano solo due set si può notare che ci sono tre possbili classi che si possono creare:

1. Le colonne di tipo X che hanno 1 in entrambe le colonne
2. Le colonne di tipo Y che hanno _solamente_ un 1
3. Le colonne di tipo Z che hanno 0 in entrambe le colonne

class| C1 | C2|
-----| ---| ---|
x    | 1 | 1 |
y    | 1 | 0 |
y    | 0 | 1 |
z    | 0 | 0 |

#### Similarità di Jaccard
Dato un documento *D* e un set di parole definito con *C=S(D)* viene definita **Similarità di Jaccard** la sequente quantità:
> Sim(D1, D2) =  intesezione di C1 e C2 divisa l'unione di C1 C2
 
 Ricordando che l'interzione equivale all **AND LOGICO**  e l'unione all'**OR LOGICO** si può definire la similarità come 
 
 > x /(x+y)
 
 I passi dell'algoritmo sono:
 
```
for each row r do begin
 	for each hash function hi do
 	computer hi(r)
 	for each column c
 		if c has 1 in row r
 			for each hash function hi do
 				if hi(r) is smaller that M(i,c) then
 					M(i,c) = hi(r);
 	end
 	  
```
E' possibile vedere un [video](https://www.youtube.com/watch?v=96WOGPUgMfw&t=31s&ab_channel=MiningMassiveDatasets) su YouTube che spiega bene il funzionamento. 


### LSH - Locality-Sensitive Hashing
Nonostanze la compressione dei dati in piccoli *signature* la ricerca di coppie simili non risulta essere possibile in termini computazionali. Quindi tramite LSH si cerca di ridurre i tempi. L'idea generale è quella di usare una funzione *f(x,y)* che indica se *x* e *y* sono una possibile coppia.
Le colonne hash vengono inserite in molti *bucket* e vengono considerati possibili candidati solamente quelli di uno stesso bucket. In questo modo si spera che le coppie diverse non verranno inserite nello stesso bucket e quindi non saranno controllate. Le coppie diverse presenti nello stesso bucket sono dei falsi positivi e si spera che siano in minoranza rispetto alle coppie simili. 
La matrice M viene divisa in *b* bande di *r* righe ciascuna. Per ogni banda viene presa una sua porzione e viene inserita in uno dei *k* bucket (k deve essere più grande possibile). Le coppie di colonne candidate sono quelle che hanno l'hash nello stesso bucket per la banda maggiore di 1. 

<p align="center">
  <img width="460" height="300" src="https://i.imgur.com/FqhILvH.jpg">
 </p>
 
 
Dipendences
------------------
* **sortedcontainers**: Libreria di Python che contiene dei tipi di collezioni ordinate. [link](https://pypi.python.org/pypi/sortedcontainers)
* **ntlk**: Modulo utilizzato per trattare ed elaborare la sintassi testuale. [link](http://www.nltk.org/)
* **sklearn**: Tools per data mining e data analysis [link](http://scikit-learn.org/stable/)


