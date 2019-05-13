import json

class LR1:
	def __init__(self, path):
		self.grammars = self.get_grammar(path)
		self.Vt, self.Vn = self.get_Vt()
		self.first = self.calculate_first()
		self.follow = self.calculate_follow()
		self.project_set = self.make_project_set()


	def get_grammar(self, path):
		grammar = []	# 文法
		with open(path, 'r') as f:
			lines = f.readlines()
			for line in lines:
				left = line.split(':')[0].strip()
				right = line.split(':')[1].strip().split(' ')
				grammar.append([left] + right)
		return grammar

	def get_Vt(self):
		Vt = set()
		Vn = set()
		for grammar in self.grammars:
			Vn.add(grammar[0])
		for grammar in self.grammars:
			for symbol in grammar[1:]:
				if symbol not in Vn:
					Vt.add(symbol)
		Vt.add('$')
		return list(Vt), list(Vn)

	def calculate_first(self):
		first = {}
		for symbol in self.Vt:
			first[symbol] = set([symbol])

		done = True
		while done:
			done = False
			for i, grammar in enumerate(self.grammars):
				if grammar[0] not in first:
					done = True
					first[grammar[0]] = set()
				if grammar[1] not in first:
					done = True
					first[grammar[1]] = set()
				prev = first[grammar[0]].copy()
				first[grammar[0]].update(first[grammar[1]])

				if prev != first[grammar[0]]:
					done = True

		for key, value in first.items():
			first[key] = list(value)
		return first

	def calculate_follow(self):
		follow = {}
		follow['Q'] = set(['$'])
		done = True
		while done:
			done = False
			for index, grammar in enumerate(self.grammars):
				for i in range(1, len(grammar)):
					if grammar[i] in self.Vn:
						if grammar[i] not in follow:
							follow[grammar[i]] = set()
							done = True
						prev = follow[grammar[i]].copy()

						if i+1 == len(grammar):
							follow[grammar[i]].update(follow[grammar[0]])
						else:
							follow[grammar[i]].update(self.first[grammar[i+1]])

						if prev != follow[grammar[i]]:
							done = True
		for key, value in follow.items():
			follow[key] = list(value)
		return follow

	def e_closure(self, projects):
		while True:
			done = True
			cnt = len(projects)
			for i in range(cnt):
				tmp = projects[i]
				if tmp[1] == len(self.grammars[tmp[0]]) - 1:
					continue
				symbol = self.grammars[tmp[0]][tmp[1] + 1]
				if symbol in self.Vt:
					continue
				elif symbol in self.Vn:
					tags = []
					if tmp[1] == len(self.grammars[tmp[0]]) - 2:
						tags.append(tmp[2])
					else:
						tags = [j for j in self.first[self.grammars[tmp[0]][tmp[1] + 2]]]
					for index, grammar in enumerate(self.grammars):
						if grammar[0] == symbol:
							for tag in tags:
								project = (index, 0, tag)
								if project not in projects:
									projects.append(project)
									done = False
				if not done:
					break
			if done:
				break
		return projects

	def GOTO(self, projects, symbol):
		tmp = []
		for project in projects:
			if len(self.grammars[project[0]]) > project[1] + 1:
				if self.grammars[project[0]][project[1] + 1] == symbol:
					tmp.append((project[0], project[1]+1, project[2]))

		return self.e_closure(tmp)

	def GO(self, projects, symbol):
		tmp = self.GOTO(projects, symbol)
		pos = self.project_exist(tmp, self.project_set)
		return pos

	# 判断项目集是否存在
	def project_exist(self, projects, project_set):
		pos = -1
		if len(projects) == 0:
			return -1
		for index, projs in enumerate(project_set):
			flag = True
			for proj in projs:
				# pdb.set_trace()
				if proj not in projects or len(projs) != len(projects):
					flag = False
					break
			if flag:
				pos = index
				break

		return pos

	def make_project_set(self):
		project_set = []
		tmp = (0, 0, '$')
		project_set.append(self.e_closure([tmp]))
		cnt = 0

		while cnt < len(project_set):
			symbols = []
			for i in project_set[cnt]:
				if len(self.grammars[i[0]]) > i[1] + 1:
					symbols.append(self.grammars[i[0]][i[1] + 1])
			for symbol in symbols:
				projects = self.GOTO(project_set[cnt], symbol)
				pos = self.project_exist(projects, project_set)
				if pos == -1:
					project_set.append(projects)

			cnt += 1

		return project_set

	def action_goto(self):
		T = {v:k for k,v in enumerate(self.Vt, 0)}
		N = {v:k for k,v in enumerate(self.Vn, 0)}

		goto = [[-1 for i in range(len(self.Vn))] for j in range(len(self.project_set))]
		action = [[('N', 0) for i in range(len(self.Vt))] for j in range(len(self.project_set))]

		for i, projects in enumerate(self.project_set):
			for project in projects:
				if len(self.grammars[project[0]]) == project[1] + 1:
					if self.grammars[project[0]][0] == 'Q':
						action[i][T[project[2]]] = ('acc')
					else:
						action[i][T[project[2]]] = ('R', project[0]) # 规约
			for symbol in self.Vt:
				pos = self.GO(projects, symbol)
				if pos > -1:
					action[i][T[symbol]] = ('S', pos)
			for symbol in self.Vn:
				pos = self.GO(projects, symbol)
				if pos > -1:
					if goto[i][N[symbol]] != -1:
						print('error 2')
					goto[i][N[symbol]] = pos

		return N, T, action, goto

	def write_file(self):
		json.dump(self.grammars, open('syntax/grammar.json', 'w'))
		with open('syntax/project_set.txt', 'w') as f:
			for i, projects in enumerate(self.project_set):
				f.write('I' + str(i) + ':\n')
				for project in projects:
					f.write(self.grammars[project[0]][0] +'->'+ str(self.grammars[project[0]][1:]) +' '+ str(project[1]) +' '+ project[2] + '\n')
				f.write('-'*100 + '\n')
		json.dump(self.first, open('syntax/first.json', 'w'))
		json.dump(self.follow, open('syntax/follow.json', 'w'))
		N, T, action, goto = self.action_goto()
		json.dump(N, open('syntax/N.json', 'w'))
		json.dump(T, open('syntax/T.json', 'w'))
		json.dump(action, open('syntax/action.json', 'w'))
		json.dump(goto, open('syntax/goto.json', 'w'))

L = LR1('grammar.txt')
L.write_file()
