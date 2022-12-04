import readline

class Completer:
	def __init__(self, tree):
		self.tree = tree
		self.cur = None

	def complete(self, cur, index):
		buffer = readline.get_line_buffer()
		if buffer.endswith(' '):
			buffer = buffer.split()
		else:
			buffer = buffer.split()[:-1]

		tree = self.tree
		for w in buffer:
			tree = tree.get(w, None)

		if tree == None:
			return None

		if cur != self.cur:
			# we have a new prefix!
			# find all words that start with this prefix
			self.matching_words = [w for w in tree.keys() if w.startswith(cur)]
			self.cur = cur
		try:
			return self.matching_words[index] + ' '
		except IndexError:
			return None


if __name__ == '__main__':
	import readline

	tree = {
		'bash': {
			'bash_1': None
		},
		'perl': {
			'perl_1': {
				'perl_1_1': None,
				'perl_1_2': None,
				'perl_1_3': None,

			},
			'perl_2': None,
			'perl_3': None
		},
		'pyjamas':{
			'pyjamas_1': None,
			'pyjamas_2': None
		},
		'python': {
			'python_1': None,
			'python_2': None,
		}
	}

	# a set of more or less interesting words
	# words = "perl", "pyjamas", "python", "pythagoras"


	completer = Completer(tree)

	readline.parse_and_bind("tab: complete")
	readline.set_completer(completer.complete)

	# try it out!
	while 1:
		print(repr(input(">>> ")))