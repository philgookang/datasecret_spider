from datetime import datetime, timedelta

class Parser:

	def __init__(self, **kwargs):

		# 0 means false! will not run!
		self.interval = kwargs["interval"] if "interval" in kwargs else 0
		self.interval_hours = kwargs["interval_hours"] if "interval_hours" in kwargs else 0
		self.interval_days = kwargs["interval_days"] if "interval_days" in kwargs else 0

		# name of this parser
		self.name = kwargs["name"] if "name" in kwargs else "Paser"

		# the SSN run was called!
		self.run_ssn = -1


		# PRIVATE Params
		# the last time it was called
		self.last_run_date_time = datetime.now()
		
		# backlog last run time so it will be callsed right away
		if self.interval != 0:
			self.last_run_date_time = self.last_run_date_time - timedelta(seconds=self.interval)

		# add hours
		if self.interval_hours != 0:
			self.last_run_date_time = self.last_run_date_time -  timedelta(hours=self.interval_hours)

		# add days
		if self.interval_days != 0:
			self.last_run_date_time = self.last_run_date_time -  timedelta(days=self.interval_days)



	def run(self, current_ssn = -1):
		
		# save the current snn number
		self.current_ssn = current_ssn

		# check if its already time
		if not self.check_interval():
			return;

		# run parser
		self.parse()


	def check_interval(self):
		
		# get current time
		current_time = datetime.now()

		# get last run time with interval time
		last_run_time = self.last_run_date_time

		# add seconds
		if self.interval != 0:
			last_run_time = last_run_time + timedelta(seconds=self.interval)

		# add hours
		if self.interval_hours != 0:
			last_run_time = last_run_time + timedelta(hours=self.interval_hours)

		# add days
		if self.interval_days != 0:
			last_run_time = last_run_time + timedelta(days=self.interval_days)

		# it has been long enough, lets run!
		if current_time >= last_run_time:
			# save that its has run again
			# might change this code location 
			self.last_run_date_time = datetime.now()

			# run parser!
			return True
		
		# nope! do not run!
		return False

	
	def parse(self):
		# this function should be over written by the subclassing class
		# print("parse Run!")
		pass


if __name__ == "__main__" :
	p = Parser(interval=1)
	p.run()
