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
    dicts = {1:'keywords', 2:'int', 3:'float', 4:'operators', 5:'separators', 6:'num', 7:'annotation', 8:'wrong_float', 9:'IDN'}

    keywords = {'int':1, 'float':2, 'bool':3, 'main':4,'return':5, 'if':6, 'else':7, 'do':8, 'while':9}
    operators = {'+':1, '++':2, '--':3, '-':4, '*':5, '/':6, '^':7, '<':8, '>':9, '!':10, '!=':11}
    separators = {'[':1, ']':2, ',':3, '{':4, '}':5, '=':6, ';':7, '(':8, ')':9}
    symbols = {}
    lines = read_file(path)

    output, annotation = '', ''
    length = len(lines)
    find_annotation = False

    # pdb.set_trace()
    for i in range(length):
        # 寻找 */ 前的部分
        if find_annotation:
            annotation += ' '
            is_found = lines[i].find('*/')
            if is_found == -1:
                annotation += lines[i]
                continue
            else:
                find_annotation = False
                tmp = lines[i].split('*/')
                if len(tmp) == 1:
                    output += annotation + lines[i] + '\t<Annotation,_>\n'
                    continue
                else:
                    lines[i] = tmp[1]
                    output += annotation + tmp[0] + '\t<Annotation,_>\n'

        # pdb.set_trace()
        is_found = lines[i].find('/*')
        if is_found > -1:
            # print(is_found)
            # annotation = dicts[6] + '\t' + lines[i][is_found+2:]
            is_found_1 = lines[i].find('*/')
            if is_found_1 > -1:
                annotation = lines[i][is_found+2:is_found_1]
                output += annotation + '\t<Annotation,_>\n'
                continue
            else:
                annotation = lines[i][is_found+2:]
                lines[i] = lines[i][0:is_found]
                find_annotation = True

        if len(lines[i]) == 0:
            is_found = annotation.find('*/')
            if is_found > -1:
                find_annotation = False
                output += annotation[0:is_found] + '\n'
                # annotation = ''
            continue
        # 头文件
        if lines[i][0] == '#':
            continue

        cnt = 0
        find_sym, find_num = False, False
        tmp = ''
        # pdb.set_trace()
        while cnt < len(lines[i]):
            s = '_'
            out = scan(lines[i], cnt)
            # print(dicts[out[0]], line[out[1]: out[2]])
            symbol = lines[i][out[1]: out[2]].strip()

            # 属性值
            if out[0] == 1:
                s = str(keywords[symbol])
            if out[0] == 4:
                s = str(operators[symbol])
            if out[0] == 5:
                s = str(separators[symbol])
            if out[0] == 2 or out[0] == 3 or out[0] == 9:
                s = symbol

            # true
            if symbol == 'true':
                out[0] = 2
                s = '1'

            output += symbol + '\t<' + dicts[out[0]] + ',' + s +'>\n'
            # 构建字符表
            if (out[0] == 2 or out[0] == 3) and find_num:
                symbols[tmp] = s
                find_num = False
                find_sym = False
            if symbol == '=' and find_sym:
                find_num = True
            if out[0] == 9:
                tmp = symbol
                find_sym = True

            cnt = out[2]

    return output, symbols

if __name__ == '__main__':
    output, symbols = lexical('test.cpp')
    print(output)
    print(symbols)
