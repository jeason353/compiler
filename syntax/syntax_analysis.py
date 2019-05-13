import json
from prettytable import PrettyTable

def print_table(N, T, action, goto):
	x = ['项目集'] + list(T.keys()) + list(N.keys())
	table = PrettyTable(x)
	for i in range(len(action)):
		table.add_row([i] + action[i] + goto[i])
	with open('syntax/table.txt', 'w') as f:
		f.write(str(table))

def syntax_analysis():
	N = json.load(open('syntax/N.json'))
	T = json.load(open('syntax/T.json'))
	action = json.load(open('syntax/action.json'))
	goto = json.load(open('syntax/goto.json'))
	grammars = json.load(open('syntax/grammar.json'))

	# print_table(N, T, action, goto)
	token = []
	with open('out.txt', 'r') as f:
		lines = f.readlines()
		for line in lines:
			tmp = line.split()
			token.append(tmp[0])
			token.append(tmp[1])
	token.append('$')
	state = [0]
	sign = ['$']

	while len(token) > 0:
		symbol = token[0]
		tmp = action[state[-1]][T[symbol]]

		if tmp[0] == 'S':
			state.append(tmp[1])
			sign.append(symbol)
			token = token[2:]
		elif tmp[0] == 'R':
			g = grammars[tmp[1]]
			print(g[0] + '->' + str(g[1:]))
			for i in range(len(g)-1):
				state.pop()
				sign.pop()
			state.append(goto[state[-1]][N[g[0]]])
			sign.append(g[0])
		elif tmp[0] == 'N':
			print('Error at Line %d'%(int(token[1])))
			break
		else:
			print('acc')
			break

syntax_analysis()

