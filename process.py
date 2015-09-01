#!/usr/bin/env python

#--- const
# author: zunc
# 2015/08

import util

class Process:

	def __init__(self):
		self._process = { } # map process
		self._conFilter = ['USER']

	def isIgnore(self, line):
		for word in self._conFilter:
			if line.startswith(word):
				return True
		return False

	def removeEmpty(self, array):
		return [x for x in array if x !='']

	def getStat(self, stats):
		cnt = 1
		for line in stats.splitlines():
			if self.isIgnore(line):
				continue
			line = ' '.join(line.split())
			elements = line.split(' ', 11)
			# print elements
			if len(elements) < 11:
				print elements
				continue

			pid = int(elements[1])
			user = elements[0]
			cpu = elements[2]
			mem = elements[3]
			start = elements[8]
			time = elements[9]
			cmd = elements[10]
			param = None
			if len(elements) > 11:
				param = elements[11]

			if pid not in self._process:
				self._process[pid] = {'pid': pid, 'cpu': cpu, 'mem': mem,
				'start': start, 'time': time, 'cmd': cmd, 'param': param}
			else:
				print 'WTF. Duplicate pid: ' + pid

	def printStat(self):
		for pid in self._process.keys():
		 	print ' - %s' % (self._process[pid])

	def getByPid(self, pid):
		if pid in self._process:
			return self._process[pid]
		else:
			return None

	def refresh(self):
		self._process.clear()
		out = util.cmdRun('ps aux')
		self.getStat(out)
		# self.printStat()
