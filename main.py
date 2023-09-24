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

        afn_reader = AFNReader(afn)

        display2 = True
        while display2:
            print("AFN READER")
            print("Ingrese alguna cadena para la regex: " + postfix + " (postfix)")
            print("Ingrese 'q' para salir")

            cadena = str(input("ingrese la cadena: "))

            if cadena == 'q':
                display2 = False
            else:
                print(afn_reader.read(cadena))

        afd_builder = AFDBuilder(afn=afn, alphabet=alphabet)
        afd = afd_builder.build()

        afd_reducer = AFDReducer(afd)
        afd_reducer.reduce()

        afd_reader = AFDReader(afd)

        display = True
        while display:
            print("AFD READER")
            print("Ingrese alguna cadena para la regex: " + postfix + " (postfix)")
            print("Ingrese 'q' para salir")

            cadena = str(input("ingrese la cadena: "))

            if cadena == 'q':
                display = False
            else:
                print(afd_reader.readAFD(cadena))








main()
