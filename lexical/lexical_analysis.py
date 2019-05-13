import pdb

def read_file(filepath):
        with open(filepath, "r", encoding='utf-8') as f:
            return [line.strip() for line in f]

def scan(line: str, cnt: int) -> list:
    global keywords, operators, separators
    while line[cnt] == ' ':
        cnt += 1
    out = [0, cnt, cnt]
    if line[cnt] == '_' or line[cnt].isalpha():
        out[1] = cnt
        cnt += 1
        while line[cnt] == '_' or line[cnt].isalnum():
            cnt += 1
        out[2] = cnt
        s = line[out[1]:out[2]]
        if s.isalpha() and s in list(keywords.keys()):
            out[0] = 1
        else:
            out[0] = 9
    elif line[cnt] in list(operators.keys()):
        out[0:2] = [4, cnt]
        cnt += 1
        if line[cnt-1:cnt] in list(operators.keys()):
            cnt += 1
        out[2] = cnt
    elif line[cnt] in list(separators.keys()):
        out[0:3] = [5, cnt, cnt+1]
    elif line[cnt].isdigit():
        out[0:2] = [2, cnt]
        cnt += 1
        point_num = 0
        while line[cnt].isdigit() or line[cnt] == '.':
            if line[cnt] == '.':
                point_num += 1
            cnt += 1
        if point_num > 1:
            out[0] = 8
        if point_num == 1:
            out[0] = 3
        out[2] = cnt

    return out

def lexical(path):
    global keywords, operators, separators
    dicts = {1:'keywords', 2:'INT', 3:'FLOAT', 4:'operators', 5:'separators', 8:'wrong_float', 9:'IDN'}

    operators = {'+':1, '++':2, '--':3, '-':4, '*':5, '/':6, '^':7, '<':8, '>':9, '!':10, '!=':11}
    separators = {'[':1, ']':2, ',':3, '{':4, '}':5, '=':6, ';':7, '(':8, ')':9}
    keywords = {'int':1, 'float':2, 'bool':3, 'main':4,'return':5, 'if':6, 'else':7, 'do':8, 'while':9}
    symbols = {}
    lines = read_file(path)

    output = ''
    length = len(lines)

    for i in range(length):
        if len(lines[i]) == 0:
            continue

        cnt = 0
        found_sym, found_num = False, False
        tmp = ''

        while cnt < len(lines[i]):
            s = ''
            out = scan(lines[i], cnt)
            symbol = lines[i][out[1]: out[2]].strip()

            if out[0] == 1:
            	s = symbol.upper()
            elif out[0] == 9:
            	s = dicts[9]
            elif out[0] == 2 or out[0] == 3:
                s = 'CONST'
            else:
            	s = symbol

            output += s + '\t' + str(i+1) + '\n'

            cnt = out[2]

    return output

if __name__ == '__main__':
    output = lexical('test.cpp')
    with open('out.txt', 'w') as f:
    	f.write(output)
