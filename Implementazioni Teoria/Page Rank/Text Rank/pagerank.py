import os
import sys
import math

import numpy as np
import pandas as pd


def _extractNode(matrix):
    """
    Data una matrice di adiacenza restituisce i nodi

    :param matrix: np.array (shape nxn)
    :return: matrix: set
    """
    nodes = set()
    for colKey in matrix:
        nodes.add(colKey)
    for rowKey in matrix.T:
        nodes.add(rowKey)
    return nodes


def _makeSparse(matrix, keys, default=0.8):
    """
    Rende la matrice quadrata e modifica il valore di NaN sostituindolo con il valore 'default'


    :param matrix:
    :param keys:
    :param default:
    :return:
    """
    matrix = matrix.copy()

    def insertMissingColumns(matrix):
        for key in keys:
            if not key in matrix:
                matrix[key] = pd.Series(default, index=matrix.index)
        return matrix

    matrix = insertMissingColumns(matrix)  # Insert missing columns
    matrix = insertMissingColumns(matrix.T).T  # Insert missing rows

    return matrix.fillna(default)


def _ensureRowsPositive(matrix):
    """
    Prende la matrice e modifica le righe che hanno tutti elementi uguali a 0
    inserendo un serie composta da 1


    :param matrix:
    :return:
    """
    matrix = matrix.T
    for colKey in matrix:
        if matrix[colKey].sum() == 0.0:
            matrix[colKey] = pd.Series(np.ones(len(matrix[colKey])), index=matrix.index)
    return matrix.T


def _normalizeRows(matrix):
    """
    Normalizza la matrice per righe. (La somma dei valori lungo la riga deve essere uguale a 1)

    :param matrix:
    :return:
    """
    return matrix.div(matrix.sum(axis=1), axis=0)


def _euclideaNorm(series):
    return math.sqrt(series.dot(series))


# PageRank specific functionality

def _startState(nodes):
    """
    Prende i nodi e crea una Series nei quali inserisce tutti i valori uguali e pari a
    1 diviso il numero dei nodi

    :param nodes:
    :return:
    """
    if len(nodes) == 0:
        raise ValueError('Deve essere presente almeno un nodo')
    startProb = 1.0 / float(len(nodes))
    return pd.Series({node: startProb for node in nodes})


def _integrateRandomSurfer(nodes, transitionProbs, rsp):
    """
    Aggiunge il valore alpha

    :param nodes:
    :param transitionProbs:
    :param rsp:
    :return:
    """
    alpha = 1.0 / float(len(nodes)) * rsp
    return transitionProbs.copy().multiply(1.0 - rsp) + alpha


def powerIteration(transitionWeights, rsp=0.15, epsilon=0.00001, maxIterations=1000):
    transitionWeights = pd.DataFrame(transitionWeights)
    nodes = _extractNode(transitionWeights)
    transitionWeights = _makeSparse(transitionWeights, nodes, default=0.0)
    transitionWeights = _ensureRowsPositive(transitionWeights)

    # Setup    print(transitionWeights)

    state = _startState(nodes)
    transitionProbs = _normalizeRows(transitionWeights)
    transitionProbs = _integrateRandomSurfer(nodes, transitionProbs, rsp)

    # Power iteration:
    for iteration in range(maxIterations):
        oldState = state.copy()
        state = state.dot(transitionProbs)
        delta = state - oldState
        if _euclideaNorm(delta) < epsilon:
            break

    return state
