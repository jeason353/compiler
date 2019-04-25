import numpy as np

first = np.zeros((300, 300), dtype=bool) # frist集合

# 项目集,(i,j,k)表示第i个文法，点在j位置，k是展望符
project_set = []

table = np.zeros((300, 3)) # 分析表

Vt = np.zeros((128), dtype=bool) # 终结符

state_stack = []
sign_stack = []


# 读取文法, @表示空
def get_grammar(path):
	grammar = []	# 文法
	grammar.append('S')
	with open(path, 'r') as f:
		lines = f.readlines()
		for line in lines:
			line = line[0] + line[3:]
			grammar.append(line.strip())
	grammar[0] += grammar[0] + grammar[1][0]
	return grammar

# 判断是否为终结符
def get_Vt(grammars):
	Vt = np.zeros((128), dtype=bool)
	Vn = np.zeros((128), dtype=bool)
	for gram in grammars:
		for i in range(len(gram)):
			if ord(gram[i]) <= ord('A') or ord(gram[i]) >= ord('Z'):
				Vt[ord(gram[i])] = True
			else:
				Vn[ord(gram[i])] = True
	return Vt, Vn

def calculate_first(grammars):
	global Vn,Vt
	first = np.zeros((128, 128), dtype=bool)
	done = True
	while done:
		done = False
		for i, grammar in enumerate(grammars):
			j, is_empty = 1, True
			while j < len(grammar) and is_empty:
				is_empty = False
				if Vn[ord(grammar[j])] :
					for k in range(64):
						if first[ord(grammar[j]), k] and not first[ord(grammar[0]), k]:
							first[ord(grammar[0]), k] = True
							done = True
					if first[ord(grammar[j]), 64]:
						is_empty = True
						j += 1
					for k in range(91, 128):
						if first[ord(grammar[j]), k] and not first[ord(grammar[0]), k]:
							done = True
							first[ord(grammar[0]), k] = True
				elif first[ord(grammar[0]), ord(grammar[j])] == False:
					done = True
					first[ord(grammar[0]), ord(grammar[j])] = True

			if len(grammar) == j:
				first[ord(grammar[0]), 36] = True
	return first

def get_search(project):
	global Vt, Vn, first
	size, flag = 0, True
	buf = ''
	now = project[1]
	while flag:
		flag = False
		tmp = grammars[project[0]][now + 1]
		if now + 1 >= len(grammars[project[0]]):
			buf += chr(project[2])
			break
		elif Vt[tmp]:
			buf += tmp
			break
		elif Vn[tmp]:
			for i in range(64):
				if first[ord(tmp),i]:
					buf += chr(i)
			for i in range(91, 128):
				if first[ord(tmp),i]:
					buf += chr(i)
			if first[ord(tmp),64]:
				now += 1
				flag = True
	return buf

def is_in(project, T):
	global project_set
	judge = False
	for i, p in enumerate(project[T]):
		if p == project:
			judge = True
	return judge

def e_closure(grammars, T):
	global Vn, Vt, project_set
	for i in range(project_set[T]):
		tmp = grammars[project_set[T][i][0]][project_set[T][i][1]]
		if Vn[tmp]:
			for j, grammar in enumerate(grammars):
				if grammar[0] == tmp:
					buf = get_search(project_set[T][i])
					for k in range(len(buf)):
						temp = (j, 1, buf[k])
						if not is_in(temp, T):
							project_set[T].append(temp)

def make_project_set(grammars):
	global project_set
	project_set[].append([])
	project_set[0].append((0,1,'#'))
	e_closure(grammars, 0)
	count, i = 1, 0
	buf = []
	while i < count + 1:


def LR1(path):
	global Vt, Vn, project_set, first
	project_set = []
	grammars = get_grammar(path)
	Vt, Vn = get_Vt(grammars)
	first = calculate_first(grammars, Vn)
	# s = ''
	# for i in range(65, 91):
	# 	flag = False
	# 	for j in range(128):
	# 		if first[i,j]:
	# 			if not flag:
	# 				flag = True
	# 				s += '\n' + chr(i) + ' ' + chr(j) + ','
	# 			else:
	# 				s += chr(j) + ','
	# 	flag = False
	# print(s)

LR1('grammar.txt')
