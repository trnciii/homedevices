import re

def justzen(s, w):
	len_displayed = len(re.sub(r'\033\[.*?m', '', s))
	if w>len_displayed:
		return s + '　'*(w-len_displayed)
	else:
		return s

def rgb(r, g, b, bg='f'):
	if bg in ['b', 'bg', 'background']:
		return f'48;2;{r};{g};{b}'
	else:
		return f'38;2;{r};{g};{b}'

def color(name, k='f'):
	table = {
		'black': 0,
		'red': 1,
		'green': 2,
		'yellow': 3,
		'blue': 4,
		'magenta': 5,
		'cyan': 6,
		'white': 7
	}

	kind = {
		'f': 3,
		'b': 4,
		'fl': 9,
		'bl': 10
	}

	assert name in table.keys()
	assert k in kind.keys()

	return str(kind[k]) + str(table[name])


def reset_all():
	return ''

def reset_color():
	return '0'

def bold():
	return '1'

def dim():
	return '2'

def italic():
	return '3'

def underline():
	return '4'

def blink():
	return '5'

def inv():
	return '7'

def hide():
	return '8'

def strikeline():
	return '9'

def mod(s, cc):
	return '\033[{}m'.format(';'.join(cc)) + s + '\033[{}m'.format(reset_all())
