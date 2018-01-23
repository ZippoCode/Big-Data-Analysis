import operator
import math, random, sys, csv


def parse(filename, isDirected):
    reader = csv.reader(open(filename, 'r'), delimeter = ',')
    data = [row for row in reader]



if __name__ == '__main__':

    if len(sys.argv) == 1:
        print('Error.')

    else:
        filename = sys.argv[1]
        isDirected = False
        if sys.argv[2] == 'directed':
            isDirected = True

        graf = parse(filename, isDirected)