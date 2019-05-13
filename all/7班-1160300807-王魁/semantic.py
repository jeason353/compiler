import json
import pdb

class Symbol_Table:
    def __init__(self):
        self.symbols = {}
        self.offset = 0

    def add_symbol(self, id, typ, size):
        self.symbols[id] = (typ, size, self.offset)
        self.offset += size

class Node:
    def __init__(self, typ='',value=0, name='', child=[]):
        self.type = typ
        self.addr = value
        self.code = []
        self.attrs = {}
        self.child = child
        if len(name) == 0:
            self.attrs['name'] = str(self.addr)
        else:
            self.attrs['name'] = name

    def set_attr(self, attr, val):
        self.attrs[attr] = val

class Helper:
    def __init__(self):
        self.temp_num = 0

    def newTemp(self):
        res = 't'+str(self.temp_num)
        self.temp_num += 1
        return res

class Semantic:
    def __init__(self):
        pass

    def action1(self):
        father.code = father.child[0].code.copy()

    def action_2(self, father):
        father.code = father.child[0].code.copy()

    def action_3(self, father):
        father.code = father.child[0].code.copy()

    def action_4(self, father):
        father.code = father.child[1].code.copy()

    def action_5(self, father):
        father.code = father.child[0].code + father.child[1].code

    def action_6(self, father):
        # print(father.child[2].type)
        if father.child[1].attrs['name'] in symbol_table.symbols:
            raise Exception('变量' + father.child[1].attrs['name'] + '已定义！')
        symbol_table.add_symbol(father.child[1].attrs['name'], father.child[0].type, 4)

    def action_7(self, father):
        if father.child[1].attrs['name'] in symbol_table.symbols:
            raise Exception('变量' + father.child[1].attrs['name'] + '已定义！')
        symbol_table.add_symbol(father.child[1].attrs['name'], father.child[0].type, father.child[3].addr * 4)

    def action_8(self, father):
        father.addr = father.child[0].addr
        father.attrs['name'] = str(father.addr)

    def action_9(self, father):
        # symbol_table.add_symbol(father.child[1].attrs['name'], 'int', 4)
        father.type = 'int'
        father.attrs['name'] = father.child[0].attrs['name']

    def action_10(self, father):
        # father.addr = father.child[0].addr
        father.type = 'float'
        # symbol_table.add_symbol(father.child[1].attrs['name'], 'float', 4)
        father.attrs['name'] = father.child[0].attrs['name']

    def action_11(self, father):
        if father.child[0].attrs['name'] not in symbol_table.symbols:
            # print('变量' + father.child[0].attrs['name'] + '未声明！')
            raise Exception('变量' + father.child[0].attrs['name'] + '未声明！')
        if symbol_table.symbols[father.child[0].attrs['name']][0] == 'int' and str(father.child[2].addr).find('.') > -1:
            raise Exception('把浮点数赋值给整型变量！')
        code = '=, ' + father.child[2].attrs['name'] + ', -, ' + father.child[0].attrs['name']
        father.code.append(code)

    def action_12(self, father):
        tmp = helper.newTemp()
        code = '+, ' + father.child[0].attrs['name'] + ', ' + father.child[2].attrs['name'] + ', ' + tmp
        father.code = father.child[0].code + father.child[1].code + [code]
        father.attrs['name'] = tmp
        father.addr = father.child[0].addr + father.child[1].addr

    def action_13(self, father):
        tmp = helper.newTemp()
        code = '*, ' + father.child[0].attrs['name'] + ', ' + father.child[2].attrs['name'] + ', ' + tmp
        father.code = father.child[0].code + father.child[1].code + [code]
        father.attrs['name'] = tmp
        father.addr = father.child[0].addr * father.child[1].addr

    def action_14(self, father):
        tmp = helper.newTemp()
        code = '-, ' + father.child[0].attrs['name'] + ', ' + father.child[2].attrs['name'] + ', ' + tmp
        father.code = father.child[0].code + father.child[1].code + [code]
        father.attrs['name'] = tmp
        father.addr = father.child[0].addr - father.child[1].addr

    def action_15(self, father):
        code = '-, 1, ' + father.child[0].attrs['name'] + ', ' + father.child[0].attrs['name']
        father.code = father.child[0].code + [code]
        father.attrs['name'] = father.attrs['name']
        father.addr = father.addr - 1

    def action_16(self, father):
        code = '+, 1, ' + father.child[0].attrs['name'] +', ' + father.child[0].attrs['name']
        father.code = father.child[0].code + [code]
        father.attrs['name'] = father.attrs['name']
        father.addr = father.addr + 1

    def action_17(self, father):
        father = father.child[1]

    def action_18(self, father):
        if father.child[0].attrs['name'] not in symbol_table.symbols:
            raise Exception('变量' + father.child[0].attrs['name'] + '未声明！')
        father.addr = father.child[0].addr
        father.attrs['name'] = father.child[0].attrs['name']

    def action_19(self, father):
        father.addr = father.child[0].addr
        father.attrs['name'] = str(father.child[0].addr)

    def action_20(self, father):
        ope = father.child[1].attrs['operate'] if 'operate' in father.child[1].attrs else ''
        jmp = 'j' + opposite[ope] + ', ' + father.child[1].child[0].attrs['name'] + ', ' + father.child[1].child[2].attrs['name'] + ',+' + str(len(father.child[3].code) + 1)
        father.code = father.child[1].code + [jmp] + father.child[3].code

    def action_21(self, father):
        ope = father.child[1].attrs['operate'] if 'operate' in father.child[1].attrs else ''
        jmp = 'j' + opposite[ope] + ', ' + father.child[1].child[0].attrs['name'] + ', ' + father.child[1].child[2].attrs['name'] + ',+' + str(len(father.child[3].code) + 2)
        goto = 'j, -, -,+' + str(len(father.child[7].code) + 1)
        father.code = father.child[1].code + [jmp] + father.child[3].code + [goto] + father.child[7].code

    def action_22(self, father):
        ope = father.child[1].attrs['operate'] if 'operate' in father.child[1].attrs else ''
        jmp = 'j' + opposite[ope] + ', ' + father.child[1].child[0].attrs['name'] + ', ' + father.child[1].child[2].attrs['name'] + ',+' + str(len(father.child[3].code) + 2)
        goto = 'j, -, -,-' + str(len(father.child[3].code) + 1)
        father.code = father.child[1].code.copy() + [jmp] + father.child[3].code + [goto]

    def action_23(self, father):
        # print(father.child[1].code)
        father.attrs['operate'] = father.child[1].attrs['operate']
        father.child = father.child[1].child

    def action_24(self, father):
        father.attrs['operate'] = '>'

    def action_25(self, father):
        father.attrs['operate'] = '<'

    def action_26(self, father):
        father.attrs['operate'] = '>='

    def action_27(self, father):
        father.attrs['operate'] = '<='

    def action_28(self, father):
        father.attrs['operate'] = '=='
        # print(father.child[2].attrs['name'])

    def action_29(self, father):
        father.attrs['operate'] = '!='

    def action_30(self, father):
        father.addr = father.child[0].addr

    def action_31(self, father):
        if father.child[0].attrs['name'] not in symbol_table.symbols:
            # print('变量' + father.child[0].attrs['name'] + '未声明！')
            raise Exception('变量' + father.child[0].attrs['name'] + '未声明！')
        if father.child[2].attrs['name'].find('.') > -1:
            raise Exception('数组下标出现非整数！')
        if father.child[2].addr >= symbol_table[father.child[0].attrs[name]][1] / 4:
            raise Exception('数组越界')
        code = '=, ' + father.child[2].attrs['name'] + ', -, ' + father.child[0].attrs['name'] + '[' + father.child[2].attrs['name'] + ']'
        father.code.append(code)

def analyse():
    global helper, symbol_table
    helper = Helper()
    symbol_table = Symbol_Table()

    N = json.load(open('syntax/N.json'))
    T = json.load(open('syntax/T.json'))
    follow = json.load(open('syntax/follow.json'))
    action = json.load(open('syntax/action.json'))
    goto = json.load(open('syntax/goto.json'))
    grammars = json.load(open('syntax/grammar.json'))

    token = []
    with open('out_1.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            tmp = line.split()
            token.append(tmp[0])
            token.append(tmp[1])
            token.append(tmp[2])
    token.append('$')
    state = [0]
    sign = ['$']

    nodes = []

    semantic = Semantic()
    output_code = ''

    while len(token) > 0:
        symbol = token[0]
        tmp = action[state[-1]][T[symbol]]

        # 生成节点
        if len(token) > 2:
            if token[1] == 'None':
                node = Node(typ=symbol)
            elif symbol == 'IDN':
                node = Node(typ=symbol, name=token[1])
            elif symbol == 'CONST':
                try:
                    node = Node(typ=symbol, value=int(token[1]))
                except ValueError:
                    node = Node(typ=symbol, value=float(token[1]))

        if tmp[0] == 'S':
            state.append(tmp[1])
            sign.append(symbol)
            nodes.append(node)
            token = token[3:]
        elif tmp[0] == 'R':
            g = grammars[tmp[1]]
            childs = []

            # print(g[0] + '->' + str(g[1:]))
            for i in range(len(g)-1):
                childs.append(nodes.pop())
                state.pop()
                sign.pop()

            childs.reverse()
            father = Node(child=childs)
            try:
                getattr(semantic, 'action_'+str(tmp[1] + 1))(father)
            except Exception as e:
                print('Error at line ' + token[2] + ' : ' + str(e))
            nodes.append(father)

            state.append(goto[state[-1]][N[g[0]]])
            sign.append(g[0])
        elif tmp[0] == 'N':
            # print('Error at Line %d'%(int(token[2])))
            while sign[-1] not in N:
                state.pop()
                sign.pop()
            state.pop()
            follo = follow[sign[-1]]
            while token[0] not in follo:
                token = token[3:]
            state.append(goto[state[-1]][N[sign[-1]]])
        else:
            # print('acc')
            for i, code in enumerate(nodes[0].code):
                if code.startswith('j'):
                    found = code.find(',+')
                    if found > 0:
                        num = i + 1 + int(code[found+2:])
                    else:
                        found = code.find(',-')
                        num = i + 1 - int(code[found+2:])
                    code = code[0:found+1] + ' ' + str(num)

                # print(str(i+1) + '   (' + code + ')')
                output_code += str(i+1) + '   (' + code + ')\n'
            output_code += str(i+2)
            symbol_table.symbols
            break
    return output_code, symbol_table.symbols

opposite = {'>':'<=', '<':'>=', '>=':'<', '<=':'>', '==':'!=', '!=':'==', '':''}

if __name__ == '__main__':
    analyse()
