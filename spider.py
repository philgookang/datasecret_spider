import datetime
import time
import os.path

from library.Log import LOG
from library.Parser import Parser
from library.Postman import Postman
from parsers.WonDollar import WonDollar


class Spider:


    def __init__(self):
    	
    	# name of config file
    	self.config_filename = "running.dat"

    	# list that holds parsing objects
    	self.parser_list = [ ]

    	# spider internal clock
    	self.ssn = 0


    	# database connection 
    	# by doing this, we create first connection and make it available everywhere!
    	Postman.init()


    def addParser(self, parser):
        self.parser_list.append(parser)


    def run(self):
    	
    	# programming running status variable
    	program_run = True # set default to TRUE

    	# create file that will be used to check whether to safely kill program
    	with open(self.config_filename, "w") as f:
    		f.write("run spider!")
		
    	while program_run:
    		
    		# increase ssn
    		self.ssn += 1
    		#LOG("Spider", "Running SSN: ", self.ssn)

    		# loop through parser list
		# each parser will internally check its polling status and run if nesscary
    		for parser in self.parser_list:
    			parser.run(self.ssn)

		# sleep for 1 second
    		time.sleep(1)

    		# check if file exists, if not stop program
    		program_run = os.path.isfile(self.config_filename)
    

if __name__ == "__main__" :
	s = Spider()
	s.addParser( WonDollar(name="원달러환율", interval_days=1) )
	s.run()

