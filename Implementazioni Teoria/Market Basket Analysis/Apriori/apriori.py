import sys

from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser


def subsets(arr):
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def joinSet(itemSet, length):
    """
    Crea le tuple-triple...
    Dunque collega ogni item con quello successivo in modo iterativo

    :param itemSet:
    :param length:
    :return:
    """
    return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])


def getItemSetTransactionList(data_iterator):
    """
    Crea una lista con i frozenset delle transizioni e un set con i frozenset degli item.
    In particolare si ricordi che un frozenset implementa nativamente un hashmap.

    :param data_iterator:
    :return:
        transactionList: list
        itemSet: set()
    """
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))  # Genera un 1-itemSet
    return itemSet, transactionList


def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
    """
    Calcola il valore del support (cioè la frequenza di ogni item) del'itemSet e restituisce
    la sottorete che soffisfa il supporto minimo

    :param itemSet:
    :param transactionList:
    :param minSupport:
    :param freqSet:
    :return:

    """
    _itemSet = set()
    localSet = defaultdict(int)

    for item in itemSet:
        for transaction in transactionList:

            if item.issubset(transaction):
                # Verifica se l'item è presente nella transizione
                freqSet[item] += 1
                localSet[item] += 1
    for item, count in localSet.items():
        support = float(count) / len(transactionList) # Calcolo supporto

        if support >= minSupport:
            # Se il supporto supera quello minimo lo aggiungo
            _itemSet.add(item)

    return _itemSet


def runApriori(data_iter, minSupport, minConfidence):
    itemSet, translactionList = getItemSetTransactionList(data_iter)

    freqSet = defaultdict(int)
    # Dizionario globale che salva come chiave il numero dell'itemSet e come valore il support
    # che supera la soglia 'minSupport'
    largeSet = dict()
    # Dizionazio che contiene le regole associative
    assocRules = dict()

    oneCset = returnItemsWithMinSupport(itemSet, translactionList, minSupport, freqSet)

    currentLSet = oneCset
    k = 2
    while (currentLSet != set([])): # La condizione di uscita è quando non è possibile creare nuovi set
        largeSet[k - 1] = currentLSet
        currentLSet = joinSet(currentLSet, k) # k rappresenta il numero di item da collegare (2,3, ...)
        currentCSet = returnItemsWithMinSupport(currentLSet, translactionList,
                                                minSupport, freqSet)
        currentLSet = currentCSet
        k = k + 1

    def getSupport(item):
        return float(freqSet[item] / len(translactionList))

    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item)) for item in value])

    # Applico la potatura
    toRetRules = []
    for key, value in list(largeSet.items())[1:]:
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSupport(item) / getSupport(element)
                    if confidence >= minConfidence:
                        toRetRules.append(((tuple(element), tuple(remain)), confidence))

    return toRetItems, toRetRules


def dataFromFile(fname):
    file_iter = open(fname, 'rU')
    for line in file_iter:
        line = line.strip().rstrip(',')
        record = frozenset(line.split(','))
        yield record


def printResults(items, rules):
    for item, support in items:
        print("item: %s , %.3f" % (str(item), support))
    print("\n------------------------ RULES:")

    for rule, confidence in rules:
        pre, post = rule
        print("Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence))


if __name__ == '__main__':

    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='input',
                         help='filename containing csv',
                         default=None)

    optparser.add_option('-s', '--minSupport',
                         dest='minS',
                         help='minimum support value',
                         default=0.15,
                         type='float')

    optparser.add_option('-c', '--minConfidence',
                         dest='minC',
                         help='minimum confidence value',
                         default=0.6,
                         type='float')

    (options, args) = optparser.parse_args()

    inFile = None
    if options.input is None:
        inFile = sys.stdin
    elif options.input is not None:
        inFile = dataFromFile(options.input)
    else:
        print('Il nome del dataset non è stato specificato, exit...')
        sys.exit('Chiusura')

    minSupport = options.minS
    minConfidence = options.minC

    item, rules = runApriori(inFile, minSupport, minConfidence)

    printResults(item, rules)
