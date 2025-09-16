def shunting_yard(regex):
    """Convert infix regex to postfix notation using shunting yard algorithm"""
    precedence = {
        '|': 1,     # alternation (lowest precedence)
        '.': 2,     # concatenation
        '*': 3,     # zero or more (highest precedence)
        '+': 3,     # one or more
        '?': 3,     # zero or one
    }
    
    output = []     
    ops = []        
    i = 0           
    
    # Track what the last token was to handle implicit concatenation
    last_was_operand = False  # True if last token was operand or closing paren
    
    while i < len(regex):
        char = regex[i]
        
        # Handle escaped characters
        if char == '\\':
            if i + 1 < len(regex):
                # Add implicit concatenation if needed
                if last_was_operand:
                    while ops and ops[-1] != '(' and precedence.get(ops[-1], 0) >= precedence['.']:
                        output.append(ops.pop())
                    ops.append('.')
                
                token = regex[i:i+2]
                output.append(token)
                last_was_operand = True
                i += 2
                continue
            else:
                raise ValueError("Invalid escape sequence at end of input")
        
        # Handle opening parenthesis
        elif char == '(':
            # Add implicit concatenation if needed
            if last_was_operand:
                while ops and ops[-1] != '(' and precedence.get(ops[-1], 0) >= precedence['.']:
                    output.append(ops.pop())
                ops.append('.')
            
            ops.append(char)
            last_was_operand = False
            i += 1
        
        # Handle closing parenthesis
        elif char == ')':
            # Pop operators until we find the matching '('
            while ops and ops[-1] != '(':
                output.append(ops.pop())
            
            if not ops:
                raise ValueError("Mismatched parentheses")
            
            ops.pop()  # Remove the '('
            last_was_operand = True
            i += 1
        
        # Handle unary postfix operators
        elif char in {'*', '+', '?'}:
            if not last_was_operand:
                raise ValueError(f"Unary operator '{char}' without operand")
            output.append(char)
            # last_was_operand stays True since these are postfix
            i += 1
        
        # Handle binary operators
        elif char == '|':
            # Pop operators with higher or equal precedence
            while ops and ops[-1] != '(' and precedence.get(ops[-1], 0) >= precedence[char]:
                output.append(ops.pop())
            
            ops.append(char)
            last_was_operand = False
            i += 1
        
        # Handle regular operands (characters)
        else:
            # Add implicit concatenation if needed
            if last_was_operand:
                while ops and ops[-1] != '(' and precedence.get(ops[-1], 0) >= precedence['.']:
                    output.append(ops.pop())
                ops.append('.')
            
            output.append(char)
            last_was_operand = True
            i += 1
    
    # Pop remaining operators
    while ops:
        if ops[-1] == '(':
            raise ValueError("Mismatched parentheses")
        output.append(ops.pop())
    
    return ''.join(output)


def validate_regex(regex):
    """Valida la expresión regular antes de ser procesada"""
    stack = []
    escape = False
    
    for i, char in enumerate(regex):
        if escape:
            escape = False
            continue
        
        if char == '\\':
            escape = True
            if i == len(regex) - 1:
                raise ValueError("Invalid escape at end of input")
            continue
        
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack or stack[-1] != '(':
                raise ValueError("Mismatched parentheses")
            stack.pop()
    
    if escape:
        raise ValueError("Incomplete escape sequence")
    
    if stack:
        raise ValueError("Mismatched parentheses")
    
    for i in range(len(regex) - 1):
        curr = regex[i]
        next_char = regex[i+1]
        
        if curr in ('*', '+', '?') and next_char in ('*', '+', '?'):
            raise ValueError(f"Consecutive operators at position {i}")
        
        if curr == '|' and next_char == '|':
            raise ValueError(f"Empty alternative at position {i}")
    
    return True

def process_regex(filename):
    """Procesa la expresión regular"""
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
                    except ValueError as e:
                        print(f"Expresión regular inválida: {e}")
                        return None
                    print("="*30)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    

# Example usage
if __name__ == "__main__":
    filename = input("Nombre del archivo: ")
    process_regex(filename)