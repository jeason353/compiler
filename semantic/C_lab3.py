import json
import copy
OO = open('action.json', 'r')
ACTION_TABLE = json.loads(OO.read())
OO.close()
OO = open('goto.json', 'r')
GOTO_TABLE = json.loads(OO.read())
OO.close()
OO = open('N.json', 'r')
GET_NTEM = json.loads(OO.read())
OO.close()
OO = open('T.json', 'r')
GET_TEM = json.loads(OO.read())
OO.close()

LISTOFN = list(GET_NTEM.keys())
LISTOFT = list(GET_TEM.keys())

LINEOFCODE = 0
TABLE = {}

class label:
    def __init__(self):
        self.line = 0

    def inc(self):
        global LINEOFCODE
        LINEOFCODE += 1
        self.line = LINEOFCODE

    def get(self):
        global LINEOFCODE
        self.line = LINEOFCODE


class node:
    def __init__(self, type='', code=[], this=None, next=None):
        self.type = type
        self.addr = 0
        self.code = code
        self.this = this
        self.next = next


RULE_SET = [] #规则集合
f = open('grammar.txt', 'r')
lines = f.readlines()
for i in lines:
    line = i.split(':')
    ll = line[0].strip()
    rr = (line[1].strip()).split()
    RULE_SET.append([ll, rr])

def ERROR(command):
    if len(CHAR_STACK) > 0:
        while len(command) > 0:
            cmd = ACTION_TABLE[STATE_STACK[-1]][GET_TEM[command[0]]]
            if cmd[0] == 'N':
                command = command[1:]
                global ccmand
                ccmand = ccmand[1:]
            else:
                break
    return command


OO = open('out.txt', 'r')
lines = OO.readlines()
command = []
ccmand = []
for i in lines:
    ccmand.append(i)
    command.append(((i.split())[1]).strip())

command.append('$')
ccmand.append('$')
# GET_TEM = {}
# GET_NTEM = {}

# for i in range(len(LISTOFT)):
#     GET_TEM[LISTOFT[i]] = i
# for i in range(len(LISTOFN)):
#     GET_NTEM[LISTOFN[i]] = i
STATE_STACK = []
CHAR_STACK = []
NODE_STACK = []
STATE_STACK.append(0)
CHAR_STACK.append('#')

T = 0
TMP = 0

def process(arg, number, idn, cst):
    global T
    global TMP
    ans = node()
    if number >= 0 and number <= 2:
        ans = copy.copy(arg[0])
    elif number >= 3 and number <= 5:
        ans.this = arg[0].this
        ans.next = arg[1].next
        ans.code = arg[0].code + arg[1].code
    elif number == 6:
        ans.this = label()
        ans.this.get()
        ans.next = label()
        ans.next.get()
        ans.code = []
        if idn in TABLE.keys():
            print('error')
        else:
            TABLE[idn] = [arg[0].type, 0]
    elif number == 7:
        ans.type = 'INT'
    elif number == 8:
        ans.type == 'FLOAT'
    elif number == 9:
        ans.this = arg[0].this
        ans.next = label()
        ans.next.inc()
        if idn not in TABLE.keys():
            print('error')
        else:
            if TABLE[idn][0] != arg[0].type:
                print('error')
            else:
                ans.code = arg[0].code + [('assign', 't' + str(arg[0].addr), '_', idn)]
                while T > 0:
                    TABLE.pop('t' + str(T))
                    T -= 1
    elif number == 10:
        ans.this = arg[0].this
        ans.next = label()
        ans.next.inc()
        ans.type = arg[0].type
        T += 1
        ans.addr = T
        TABLE['t' + str(T)] = [arg[0].type, TABLE['t' + str(arg[0].addr)][1] + TABLE['t' + str(arg[1].addr)][1]]
        ans.code = arg[0].code + arg[1].code + [('+', 't' + str(arg[0].addr), 't' + str(arg[1].addr), 't' + str(T))]
    elif number == 11:
        ans.this = arg[0].this
        ans.next = label()
        ans.next.inc()
        ans.type = arg[0].type
        T += 1
        ans.addr = T
        TABLE['t' + str(T)] = [arg[0].type, TABLE['t' + str(arg[0].addr)][1] * TABLE['t' + str(arg[1].addr)][1]]
        ans.code = arg[0].code + arg[1].code + [('*', 't' + str(arg[0].addr), 't' + str(arg[1].addr), 't' + str(T))]
    elif number == 12:
        ans.this = arg[0].this
        ans.next = label()
        ans.next.inc()
        ans.type = arg[0].type
        T += 1
        ans.addr = T
        TABLE['t' + str(T)] = [arg[0].type, TABLE['t' + str(arg[0].addr)][1] - TABLE['t' + str(arg[1].addr)][1]]
        ans.code = arg[0].code + arg[1].code + [('-', 't' + str(arg[0].addr), 't' + str(arg[1].addr), 't' + str(T))]
    elif number == 13:
        ans.this = arg[0].this
        ans.next = label()
        ans.next.inc()
        ans.type = arg[0].type
        ans.addr = arg[0].addr
        TABLE['t' + str(ans.addr)] = [ans.type, TABLE['t' + str(arg[0].addr)][1] + 1]
        ans.code = arg[0].code + [('+', 't' + str(arg[0].addr), '1', 't' + str(ans.addr))]
    elif number == 14:
        ans.this = arg[0].this
        ans.next = label()
        ans.next.inc()
        ans.type = arg[0].type
        ans.addr = arg[0].addr
        TABLE['t' + str(ans.addr)] = [ans.type, TABLE['t' + str(arg[0].addr)][1] - 1]
        ans.code = arg[0].code + [('-', 't' + str(arg[0].addr), '1', 't' + str(ans.addr))]
    elif number == 15:
        ans = copy.copy(arg[0])
    elif number == 16:
        ans.this = label()
        ans.this.get()
        ans.next = label()
        ans.next.inc()
        T += 1
        ans.addr = T
        if idn not in TABLE.keys():
            print('error')
        else:
            ans.type = TABLE[idn][0]
            TABLE['t' + str(T)] = TABLE[idn]
            ans.code = [('assign', idn, '_', 't' + str(T))]
    elif number == 17:
        ans.this = label()
        ans.this.get()
        ans.next = label()
        ans.next.inc()
        T += 1
        ans.addr = T
        if isinstance(cst, int):
            ans.type = 'INT'
        else:
            ans.type = 'FLOAT'
        TABLE['t' + str(T)] = [ans.type, cst]
        ans.code = [('assign', cst, '_', 't' + str(T))]
    elif number == 18: #if
        ans.this = arg[0].this
        ans.next = arg[1].next
        ans.code = []
        for i in range(len(arg[0].code)):
            if i < len(arg[0].code) - 1:
                ans.code.append(arg[0].code[i])
            else:
                op, arg1, arg2, la = arg[0].code[i]
                if op[0] == 'a':
                    if arg1 == 'False':
                        ans.code.append(('J', '_', '_', arg[1].next.line))
                    else:
                        ans.code.append(('J', '_', '_', arg[1].this.line))
                else:
                    if op[0] == 'N':
                        op = 'J' + op[1:]
                    else:
                        op = 'JN' + op
                    ans.code.append((op, arg1, arg2, arg[1].next.line))
        ans.code = ans.code + arg[1].code
        while TMP > 0:
            TABLE.pop('tmp' + str(TMP))
            TMP -= 1
    elif number == 19: #if_else
        ans.this = arg[0].this
        ans.next = arg[2].next
        ans.code = []
        for i in range(len(arg[0].code)):
            if i < len(arg[0].code) - 1:
                ans.code.append(arg[0].code[i])
            else:
                op, arg1, arg2, la = arg[0].code[i]
                if op[0] == 'a':
                    if arg1 == 'False':
                        ans.code.append(('J', '_', '_', arg[2].this.line))
                    else:
                        ans.code.append(('J', '_', '_', arg[1].this.line))
                else:
                    if op[0] == 'N':
                        op = 'J' + op[1:]
                    else:
                        op = 'JN' + op
                    ans.code.append((op, arg1, arg2, arg[2].this.line))
        ans.code = ans.code + arg[1].code + arg[2].code
        while TMP > 0:
            TABLE.pop('tmp' + str(TMP))
            TMP -= 1
    elif number == 20: #while
        ans.this = arg[0].this
        ans.next = label()
        ans.next.inc()
        for i in range(len(arg[0].code)):
            if i < len(arg[0].code) - 1:
                ans.code.append(arg[0].code[i])
            else:
                op, arg1, arg2, la = arg[0].code[i]
                if op[0] == 'a':
                    if arg1 == 'False':
                        ans.code.append(('J', '_', '_', ans.next.line))
                    else:
                        ans.code.append(('J', '_', '_', arg[1].this.line))
                else:
                    if op[0] == 'N':
                        op = 'J' + op[1:]
                    else:
                        op = 'JN' + op
                    ans.code.append((op, arg1, arg2, ans.next.line))
        ans.code = ans.code + arg[1].code + [('J', '_', '_', ans.this.line)]
        while TMP > 0:
            TABLE.pop('tmp' + str(TMP))
            TMP -= 1
    elif number == 21:
        ans.this = arg[0].this
        ans.next = label()
        ans.next.inc()
        TMP += 1
        ans.addr = TMP
        TABLE['tmp' + str(TMP)] = ['BOOLEAN', TABLE['tmp' + str(arg[0].addr)][1] or TABLE['tmp' + str(arg[1].addr)][1]]
        ans.code = arg[0].code + arg[1].code + [('OR', 'tmp' + str(arg[0].addr), 'tmp' + str(arg[1].addr), 'tmp' + str(TMP))]
    elif number == 22:
        ans.this = arg[0].this
        ans.next = label()
        ans.next.inc()
        TMP += 1
        ans.addr = TMP
        TABLE['tmp' + str(TMP)] = ['BOOLEAN', TABLE['tmp' + str(arg[0].addr)][1] and TABLE['tmp' + str(arg[1].addr)][1]]
        ans.code = arg[0].code + arg[1].code + [('AND', 'tmp' + str(arg[0].addr), 'tmp' + str(arg[1].addr), 'tmp' + str(TMP))]
    elif number == 23:
        ans = copy.copy(arg[0])
    elif number == 24:
        ans.this = arg[0].this
        ans.next = label()
        ans.next.inc()
        TMP += 1
        ans.addr = TMP
        TABLE['tmp' + str(TMP)] = ['BOOLEAN', TABLE['t' + str(arg[0].addr)][1] >= TABLE['t' + str(arg[1].addr)][1]]
        ans.code = arg[0].code + arg[1].code + [('GE', 't' + str(arg[0].addr), 't' + str(arg[1].addr), 'tmp' + str(TMP))]
        while T > 0:
            TABLE.pop('t' + str(T))
            T -= 1
    elif number == 25:
        ans.this = arg[0].this
        ans.next = label()
        ans.next.inc()
        TMP += 1
        ans.addr = TMP
        TABLE['tmp' + str(TMP)] = ['BOOLEAN', TABLE['t' + str(arg[0].addr)][1] <= TABLE['t' + str(arg[1].addr)][1]]
        ans.code = arg[0].code + arg[1].code + [('LE', 't' + str(arg[0].addr), 't' + str(arg[1].addr), 'tmp' + str(TMP))]
        while T > 0:
            TABLE.pop('t' + str(T))
            T -= 1
    elif number == 26:
        ans.this = arg[0].this
        ans.next = label()
        ans.next.inc()
        TMP += 1
        ans.addr = TMP
        TABLE['tmp' + str(TMP)] = ['BOOLEAN', TABLE['t' + str(arg[0].addr)][1] == TABLE['t' + str(arg[1].addr)][1]]
        ans.code = arg[0].code + arg[1].code + [('EQ', 't' + str(arg[0].addr), 't' + str(arg[1].addr), 'tmp' + str(TMP))]
        while T > 0:
            TABLE.pop('t' + str(T))
            T -= 1
    elif number == 27:
        ans.this = arg[0].this
        ans.next = label()
        ans.next.inc()
        TMP += 1
        ans.addr = TMP
        TABLE['tmp' + str(TMP)] = ['BOOLEAN', TABLE['t' + str(arg[0].addr)][1] != TABLE['t' + str(arg[1].addr)][1]]
        ans.code = arg[0].code + arg[1].code + [('NEQ', 't' + str(arg[0].addr), 't' + str(arg[1].addr), 'tmp' + str(TMP))]
        while T > 0:
            TABLE.pop('t' + str(T))
            T -= 1
    elif number == 28:
        ans.this = label()
        ans.this.get()
        ans.next = label()
        ans.next.inc()
        TMP += 1
        ans.addr = TMP
        if cst != 0:
            TABLE['tmp' + str(TMP)] = ['BOOLEAN', True]
            ans.code = [('assign', 'True', '_', 'tmp' + str(TMP))]
        else:
            TABLE['tmp' + str(TMP)] = ['BOOLEAN', False]
            ans.code = [('assign', 'False', '_', 'tmp' + str(TMP))]

    return ans


iidn = []
ccst = []
idn = ''
cst = 0
while 1:
    cmd = ACTION_TABLE[STATE_STACK[-1]][GET_TEM[command[0]]]
    if cmd[0] == 'N':
        print("error")
        command = ERROR(command)
        if len(command) <= 0:
            break
    elif cmd[0] == 'S':
        if command[0] == 'IDN':
            iidn.append(((ccmand[0].split())[3]).strip())
        if command[0] == 'CONST':
            ccst.append(eval(((ccmand[0].split())[3]).strip()))
        STATE_STACK.append(cmd[1])
        CHAR_STACK.append(command[0])
        command = command[1:]
        ccmand = ccmand[1:]
    elif cmd[0] == 'R':
        print(RULE_SET[cmd[1]])
        node_to_pro = []
        for i in range(len(RULE_SET[cmd[1]][1])):
            STA = CHAR_STACK.pop()
            STATE_STACK.pop()
            if STA in LISTOFN:
                node_to_pro.insert(0, NODE_STACK.pop())
            if STA == 'IDN':
                idn = iidn.pop()
            if STA == 'CONST':
                cst = ccst.pop()

        CHAR_STACK.append(RULE_SET[cmd[1]][0])
        STATE_STACK.append(GOTO_TABLE[STATE_STACK[-1]][GET_NTEM[CHAR_STACK[-1]]])
        NODE_STACK.append(process(node_to_pro, cmd[1], idn, cst))
    else:
        print('acc')
        ii = 0
        for i in NODE_STACK[0].code:
            print('line: ' + str(ii) + ' ', end='\t')
            print(i)
            ii += 1
#        print(NODE_STACK[0].this.line)
#        print(NODE_STACK[0].next.line)
        if command[0] == '$':
            break
        else:
            STATE_STACK = [0]
            CHAR_STACK = ['#']
