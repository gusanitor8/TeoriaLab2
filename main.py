from shuntingYard.syv2 import getPostfixRegex
from AFN.AFNBuilder import AFNBuilder
from AFD.AFDBuilder import AFDBuilder
from AFD.AFDReducer import AFDReducer
from AFD.AFDReader import AFDReader
from AFN.AFNReader import AFNReader

postfixArr = getPostfixRegex()


def main():
    for postfix in postfixArr:
        afn_builder = AFNBuilder(postfix)
        afn = afn_builder.build()
        afn.terminal.printAFN(postfix)
        alphabet = afn_builder.alphabet

        afd_builder = AFDBuilder(afn=afn, alphabet=alphabet)
        afd = afd_builder.build()

        afd_reducer = AFDReducer(afd)
        afd_reducer.reduce()





main()
