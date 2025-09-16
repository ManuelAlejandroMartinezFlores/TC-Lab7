from proyecto1.main import Simulator
from eliminate_epsilon import *

AZ = 'A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z'
az = 'a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z'
D = '0|1|2|3|4|5|6|7|8|9'
REGEX = f"({AZ})->(({AZ}|{az}|{D})*\\|)*(({AZ}|{az}|{D})*|\\ε)"
'''
    [A-Z]->([A-Za-z0-9]+\\|)*([A-Za-z0-9]+|\\ε)
'''

def read_productions(line:str)->tuple[str, set[str]]:
    nonterminal, prods = line.split('->')
    return nonterminal, set(prods.split('|'))

def format_grammar(grammar:dict[str, set[str]]) -> str:
    return '\n'.join([f'{nonterminal}->{'|'.join(prods)}' for nonterminal, prods in grammar.items()])

if __name__ == '__main__':
    sim = Simulator(REGEX)

    filename = input("Nombre del archivo: ")
    try:
        with open(filename, 'r') as file:
            grammar = {}
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if line:  
                    if not sim.simulate(line):
                        raise ValueError(f'Producción no aceptable:\n\t{line}')
                    nonterminal, prods = read_productions(line)
                    grammar[nonterminal] = prods 
            print('='*80)
            print(format_grammar(grammar))
            print('='*80)
            new_grammar = modify_productions(grammar)
            print('='*80)
            print(format_grammar(new_grammar))
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
