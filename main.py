from shuntingYard.syv2 import getPostfixRegex
from lab4.AFNBuilder import AFNBuilder

def main():
    postfixArr = getPostfixRegex()
    
    for postfix in postfixArr:
        afn = AFNBuilder(postfix).build()
        afn.terminal.printAFN(postfix)

def testing():
    afn = AFNBuilder('ab|?t.').build()
    afn.terminal.printAFN('test')

main()