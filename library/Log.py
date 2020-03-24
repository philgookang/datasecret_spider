from datetime import datetime

def LOG(*args):
	args = list(args)
	args.insert(0, "[{0}]".format(datetime.now().strftime("%y-%m-%d %H:%M:%S")) )
	args[1] = "<{0}>".format(args[1])
	print(*args, sep=' ')
