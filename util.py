import signal
import sys
import subprocess as sub

class Alarm(Exception):
	pass

def alarmHandler(signum, frame):
	raise Alarm

def cmdRun(cmd):
	signal.signal(signal.SIGALRM, alarmHandler)
	signal.alarm(3) # 3 second
	try:
		p = sub.Popen(cmd, stdout=sub.PIPE,stderr=sub.PIPE, shell=True)
		output, errors = p.communicate()
		return output
	except Alarm:
		print ' - Timeout:\"%s\"' % (cmd)
		return ''
