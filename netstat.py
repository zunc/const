#!/usr/bin/env python

#--- const
# author: zunc
# 2015/08

import util
import process

class Netstat:

	def __init__(self):
		self._map_proto = { } # map protocol
		self._conFilter = ['Active', 'Proto']
		self._process = process.Process()

	def isIgnore(self, line):
		for word in self._conFilter:
			if line.startswith(word):
				return True
		return False

	def removeEmpty(self, array):
		return [x for x in array if x !='']

	def getHostPort(self, dest):
		comm = dest.split(':')
		if len(comm) < 2:
			print 'getHostPort: Parser fail on:', dest
			quit()
		host = comm[0]
		port = comm[-1]
		return {'host': host, 'port': port}

	def getStat(self, stats):
		cnt = 1
		for line in stats.splitlines():
			if self.isIgnore(line):
				continue
			elements = self.removeEmpty(line.split(' '))
			proto_name = elements[0]
			if proto_name not in self._map_proto:
				self._map_proto[proto_name] = []

			proto = self._map_proto[proto_name]
			local = self.getHostPort(elements[3])
			foreign = self.getHostPort(elements[4])

			pid = 0
			prog = None

			if len(elements) == 7:
				state = elements[5]
				pid_prog = elements[6]
			else:
				state = None
				pid_prog = elements[5]

			if pid_prog.find('/') > 0:
				pid_prog_spt = pid_prog.split('/')
				pid = int(pid_prog_spt[0])
				prog = pid_prog_spt[1]

			cmd = None
			if pid > 0:
				proc = self._process.getByPid(pid)
				if proc != None:
					cmd = proc['cmd']

			proto.append({'local': local, 'foreign': foreign,
				'state': state, 'pid': pid, 'prog': prog, 'cmd': cmd})

	def printStat(self):
		table = []
		table.append(['Protocol', 'Local', 'Foreign', 'State', 'Command'])
		for proto in self._map_proto.keys():
			# print '%s -> %s' % (proto, self._map_proto[proto])
		 	proto_detail = self._map_proto[proto]
		 	for conn in proto_detail:
		 		local = conn['local']
		 		foreign = conn['foreign']
		 		row = [proto,
		 		self.toStr('%s:%s' % (local['host'], local['port'])),
		 		self.toStr('%s:%s' % (foreign['host'], foreign['port'])),
		 		self.toStr(conn['state']),
		 		self.toStr(conn['cmd'])]
		 		table.append(row)

		for row in table:
			print("{: <8} {: <24} {: <24} {: <12} {: <24}".format(*row))

	def toStr(self, stat):
		if stat is None:
			return ''
		return stat

	def refresh(self):
		self._process.refresh()
		self._map_proto = { }
		out = util.cmdRun('netstat -patun')
		self.getStat(out)
		self.printStat()
