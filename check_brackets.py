def check_brackets(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    stack = []
    line_num = 1
    for i, char in enumerate(content):
        if char == '\n':
            line_num += 1
        elif char in '{[(':
            stack.append((char, line_num))
        elif char in '}])':
            if not stack:
                print(f"Error: Unmatched closing bracket '{char}' at line {line_num}")
                return
            last_char, last_line = stack.pop()
            matches = {'}': '{', ']': '[', ')': '('}
            if matches[char] != last_char:
                print(f"Error: Mismatched closing bracket '{char}' at line {line_num}. Expected match for '{last_char}' from line {last_line}")
                return
                
    if stack:
        print("Error: Unclosed brackets:")
        for char, line in stack[-5:]:
            print(f"  {char} at line {line}")
    else:
        print("All brackets match!")

check_brackets('test_script.js')
