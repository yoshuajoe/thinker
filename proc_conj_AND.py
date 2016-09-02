import itertools

class ProcAND(object):

	def capture_AND(self, chunkNER):
		capture = []
		# capture all composed sentence
		for bg in chunkNER:
			for b in bg:
				if b[0] == "AND":
					capture.append(bg)
					break
		return capture
	
	def proceed(self, chunkNER):
		capture = self.capture_AND(chunkNER)
		# process AND
		for capt in capture:
			index = []
			restofword = []
			newsen = []
			lst = []
			s_and = []
		
			for rst in range(len(capt)):
				restofword.append(rst)
		
			for c in range(len(capt)):
				if capt[c][0] == "AND":
					index.append(c)
		
			for ind in index:
				s_and.append([ind-1,ind+1])
				restofword.remove(ind-1)
				restofword.remove(ind+1)
				restofword.remove(ind)
			res_and = []
		
			if len(s_and) > 1:
				for hg in range(len(s_and)-1):
					s_and[hg+1] = list(itertools.product(s_and[hg], s_and[hg+1]))
					s_and.remove(s_and[hg])		

				for s_a in s_and:
					for sa in s_a:
						sa = list(sa)
						for rsr in restofword:
							sa.append(rsr)
						newsen.append(sa)
			else:
				for s_a in s_and:
					for sa in s_a:
						temp_list = []
						temp_list.append(sa)
						for rsr in restofword:
							temp_list.append(rsr)
						newsen.append(temp_list)	
						
			for d in newsen:
				newsen2bg = []
				for n in sorted(d, reverse=False):
					newsen2bg.append(capt[n])
				chunkNER.append(newsen2bg)
		
			chunkNER.remove(capt)
		return chunkNER