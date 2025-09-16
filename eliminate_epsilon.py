from itertools import combinations

def nullable_set(grammar:dict[str,set[str]]) -> set[str]:
    N = set()
    new_added = True 
    while new_added:
        new_added = False
        for nonterminal, productions in grammar.items():
            if nonterminal in N:
                continue
            for prod in productions:
                is_null = True
                if prod == 'ε':
                    new_added = True 
                    N.add(nonterminal)
                    print(f'{nonterminal} es nulable: {prod}')
                    break
                for char in prod:
                    if char not in N:
                        is_null = False
                        break
                if is_null:
                    new_added = True
                    N.add(nonterminal)  
                    print(f'{nonterminal} es nulable: {prod}')
                    break
    return N

def subsets(s:list[int]) -> list[set[int]]:
    S = []
    for i in range(len(s)+1):
        for comb in combinations(s, i):
            S.append(set(comb))
    return S

def modify_productions(grammar:dict[str, set[str]]) -> dict[str, set[str]]:
    new_grammar = {}
    N = nullable_set(grammar)
    print(f'Conjunto nulable: {N}')

    for nonterminal, productions in grammar.items():
        new_grammar[nonterminal] = set()
        for prod in productions:
            if prod == 'ε':
                continue
            for subset in subsets([i for i, char in enumerate(prod) if char in N]):
                new_prod = ''.join([char for i, char in enumerate(prod) if i not in subset])
                if new_prod == '':
                    new_prod = 'ε'
                else:
                    new_grammar[nonterminal].add(new_prod)
                print(f'Modificando {nonterminal}->{prod} con subconjunto {subset}: {new_prod}')

    if 'S' in N:
        print('**** La cadena vacía ε pertenece a la gramática ****')
        new_grammar['S'].add('ε')
    return new_grammar



if __name__ == '__main__':
    grammar = {
        'S': set(['B']),
        'B': set(['bB', 'ε']),
        'A': set(['aS', 'aAA'])
    }
    print(nullable_set(grammar))
    print(modify_productions(grammar))