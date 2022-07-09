from .main import oneliner, run
import sys

if len(sys.argv)>1:
	oneliner()
	# execute(Home(), sys.argv[1:])
else:
	run()
