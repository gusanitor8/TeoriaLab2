from shuntingYard.syv2 import getPostfixRegex
from AFN.AFNBuilder import AFNBuilder
from AFD.AFDBuilder import AFDBuilder
from AFN.AFNReader import AFNReader

postfixArr = getPostfixRegex()


def main():
    for postfix in postfixArr:
        afn_builder = AFNBuilder(postfix)
        afn = afn_builder.build()
        afn.terminal.printAFN(postfix)
        alphabet = afn_builder.alphabet

        afd = AFDBuilder(afn=afn, alphabet = alphabet)
        afd.build()
        afd

# def testing():
#     afn = AFNBuilder('ab|?t.').build()
#     afn.terminal.printAFN('test')

# def menu():
#     menu = True
#
#     while menu:
#         print("Eliga su expresion regular o ingrese 'q' para salir: ")
#         for posfixRegex in range(len(postfixArr)):
#             print(str(posfixRegex) + ". " + postfixArr[posfixRegex])
#
#             try:
#                 option = int(input("Opcion: "))
#                 if option == 'q':
#                     menu = False
#                     break
#
#                 afn = AFNBuilder(postfixArr[option]).build()
#                 string = input("Ingrese la cadena a evaluar: ")
#                 reader = AFNReader(afn, string)
#                 print(reader.read())
#
#             except ValueError:
#                 pass


main()