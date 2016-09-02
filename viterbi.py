import re
import string, sys
import string

class Viterbi(object):
	def execute(self, obs, states, start_p, trans_p, emit_p):
		V = [{}]
		path = {}
    
		# Initialize base cases (t == 0)
		for y in states:
			V[0][y] = self.getStartProbVal(y, start_p) * self.getEmitVal(obs[0], y, emit_p)
			path[y] = [y]
    
		# Run Viterbi for t > 0
		for t in range(1, len(obs)):
			V.append({})
			newpath = {}
			for y in states:
				(prob, state) = max((V[t-1][y0] * self.getTransVal(y0, y, trans_p) * self.getEmitVal(obs[t], y, emit_p), y0) for y0 in states)
				V[t][y] = prob
				newpath[y] = path[state] + [y]

			# Don't need to remember the old paths
			path = newpath
		n = 0           # if only one element is observed max is sought in the initialization values
		if len(obs) != 1:
			n = t
		#print_dptable(V)
		(prob, state) = max((V[n][y], y) for y in states)
		return (prob, path[state])

	# Don't study this, it just prints a table of the steps.
	def print_dptable(self, V):
		s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
		for y in V[0]:
			s += "%.5s: " % y
			s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
			s += "\n"
		print(s)
		
	def getStartProbVal(self, keys, list):
		for str in list:
			if str["state"] == keys:
				return str["prob"]

	def getEmitVal(self, obs, stat, emit):
		for ob in emit:
			if ob["word"] == obs:
				for st in ob["content"]:
					if st["state"] == stat:
						return st["prob"]

	def getTransVal(self, statx, staty, trans):
		for tr in trans:
			if tr["pair"]["state_x"] == statx and tr["pair"]["state_y"] == staty:
				return tr["count"]


