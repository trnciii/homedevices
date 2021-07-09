import sys
from .home import clean

print(sys.argv)

if len(sys.argv)>1:

	if sys.argv[1] == "clean":
		clean()
		exit()

s = "Command:\n\
  clean	        remove all local data (use this before uninstall)"

print(s)