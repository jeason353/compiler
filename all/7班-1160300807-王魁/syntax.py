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
	follow = json.load(open('syntax/follow.json'))
	action = json.load(open('syntax/action.json'))
	goto = json.load(open('syntax/goto.json'))
	grammars = json.load(open('syntax/grammar.json'))

	# print_table(N, T, action, goto)
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

	out = ''
	while len(token) > 0:
		symbol = token[0]
		tmp = action[state[-1]][T[symbol]]

		if tmp[0] == 'S':
			state.append(tmp[1])
			sign.append(symbol)
			token = token[3:]
		elif tmp[0] == 'R':
			g = grammars[tmp[1]]
			# print(g[0] + '->' + str(g[1:]))
			out += g[0] + '->' + str(g[1:]) + '\n'
			for i in range(len(g)-1):
				state.pop()
				sign.pop()
			state.append(goto[state[-1]][N[g[0]]])
			sign.append(g[0])
		elif tmp[0] == 'N':
			out += 'Error at Line %d'%(int(token[2]))
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
			out += 'acc'
			break

	return out

# syntax_analysis()
