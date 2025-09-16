from proyecto1.afd import * 
def get_simulator(regex:str)->AFD:
    POINT = {'.': '\\.'}
    regex = ''.join([POINT.get(a, a) for a in regex])
    postfix = shunting_yard(regex)
    nfa = regex_to_nfa(postfix)
    afd = AFD(nfa)
    afd.minimizing()
    return afd

class Simulator:
    def __init__(self, regex:str) -> None:
        self.afd = get_simulator(regex)
        self.escaped = {
            '?': '\\?',
            '*': '\\*',
            '+': '\\+',
            '(': '\\(',
            ')': '\\)',
            '{': '\\{',
            '}': '\\}',
            '|': '\\|',
            'ε': '\\ε',
            '.': '\\.'
        }

    def simulate(self, text:str) -> bool:
        return self.afd.simulate(''.join([self.escaped.get(a, a) for a in text]))


if __name__ == "__main__":
    filename = input("Nombre del archivo: ")
    try:
        with open(filename, 'r') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if line:  
                    try:
                        validate_regex(line)
                        postfix = shunting_yard(line)
                        print(f"Original: {line}")
                        print(f"Postfix: {postfix}")
                        nfa = regex_to_nfa(postfix)
                        # nfa.plot()
                        afd = AFD(nfa)
                        # afd.plot()
                        afd.minimizing()
                        # afd.plot()
                        while True:
                            try:
                                ex = input("Expresión: ")
                                ESCAPED = {
                                    '?': '\\?',
                                    '*': '\\*',
                                    '+': '\\+',
                                    '(': '\\(',
                                    ')': '\\)',
                                    '{': '\\{',
                                    '}': '\\}'
                                }
                                ex = ''.join([ESCAPED.get(a, a) for a in ex])
                                print(f'AFN: {nfa.simulate(ex)}')
                                print(f'AFD: {afd.simulate(ex)}')
                            except KeyboardInterrupt as e:
                                break
                    except ValueError as e:
                        print(f"Expresión regular inválida: {e}")
                    print('\n'+"="*50)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
