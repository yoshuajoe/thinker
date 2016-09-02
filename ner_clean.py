import re
import string, sys
import string
from viterbi import Viterbi
from concluder import Concluder

class NER(object):
	def __init__(self, observ_file="ori_corp.txt", dictio_file="anno_corp.txt"):
		self.dictio = []
		self.state = []
		self.startProb = []
		self.occurencesSt = []
		self.bow = []
		self.transSt = []
		self.emission = []
		
	def tupling(self, filename):
		lines = open(filename, "r")
		sentence = []
		lineCount = 0

		# Read line by line
		# Append it to sentence
		# tupling sentence into token and type (dictionary based)
		for line in lines:
			dict = []
			for sen in line.strip("\n").split(" "):
				tmp = sen.split("=")
				dict.append({"token":tmp[0], "type":tmp[1]})
			lineCount = lineCount+1
			sentence.append({"sentence":lineCount, "content":dict})
		return sentence

	def extractState(self):
		states = []
		for sen in self.dictio:
			for cont in sen['content']:
				if cont['type'] not in states:
					states.append(cont['type'])
		return states

	def countStartProb(self):
		result = []
		for st in self.state:
			counter = 0
			for sen in self.dictio:
				if sen['content'][0]['type'] == st:
					counter = counter + 1
			result.append({"state":st, "prob":(counter*1.00/len(self.dictio))})
		return result

	def occurencesState(self):
		occurences = []
		for st in self.state:
			wholeoccurence = 0
			for sen in self.dictio:
				for ct in sen['content']:
					if ct['type'] == st:
						wholeoccurence = wholeoccurence + 1
			occurences.append({"state":st, "occurences":wholeoccurence})
		return occurences

	def coocurrences(self):
		stOccur = []
		result = []
		tmp = []
		# map 
		for sen in self.dictio:
			for a in range(0, len(sen['content'])):
				if(a < (len(sen['content'])-1)):
						stOccur.append({"state_x":sen['content'][a]['type'], "state_y":sen['content'][a+1]['type']})
		# reduce
		for di in stOccur:
			count = 0
			flag = True
			if len(tmp) > 0:
				for x in tmp:
					if (di["state_x"] == x["state_x"]) and (di["state_y"] == x["state_y"]):
						flag = False
						break;
			
			if flag == True:
				for din in stOccur:
					if di == din:
						count = count + 1
				for ost in self.occurencesSt:
					if ost["state"] == di["state_x"]:
						azt = ost["occurences"]
				
				result.append({"pair":di, "count":(count*1.00/azt)})
				tmp.append(di)
		
		sementara = []
		for st in self.state:
			for st2 in self.state:
				sementara.append({"pair":{"state_x":st, "state_y":st2}, "count":0})
		
		for res in result:
			for sem in sementara:
				if (sem["pair"]["state_x"] == res["pair"]["state_x"]) and (sem["pair"]["state_y"] == res["pair"]["state_y"]):
					sementara.remove(sem)

		for sem in sementara:
			result.append(sem)
		
		return result

	def bagOfWord(self):
		tmp = []
		for sen in self.dictio:
			for w in sen["content"]:
				if w["token"] not in tmp:
					tmp.append(w["token"])
		return tmp
		
	def countEmission(self):
		result = []
		for b in self.bow:
			tmp = []
			for st in self.state:
				count = 0
				azt = 0;
				for sen in self.dictio:
					for d in sen["content"]:
						if b == d["token"] and st == d["type"]:
							count = count + 1
				for ost in self.occurencesSt:
					if ost["state"] == st:
						azt = ost["occurences"]
				tmp.append({"state":st, "prob":(count*1.00/azt)})
			result.append({"word":b, "content":tmp})
		return result

	def extractObs(self, sentence):
		gl = []
		for ty in sentence.split(" "):
			ty = ty.replace(",","")
			ty = ty.replace(".","")
			ty = ty.strip()
			gl.append(ty)
		return tuple(gl)
	
	def callViterbi(self, observations):
		vit = Viterbi()
		tvit = vit.execute(observations, self.state, self.startProb, self.transSt, self.emission)
		probs = tvit[0]
		state_res = tvit[1]
		return (probs, state_res)
	
	def loadSentence(self, filename):
		asdf = open(filename, "r").read()
		hasil = re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", asdf)
		res = []
		temps = ""
		for has in hasil:
			has = has.replace('\n', ' ').replace('.','').strip()
			if len(has.split(" ")) < 2:
				print(temps)
				if not temps:
					temps = temps + has
				else:
					temps = temps + " " + has	
			else:
				if not temps:
					has = temps + has
				else:
					has = temps + " " +has
				temps = ""
				res.append(has)
		print(res)
		return res	
		
	def train(self, dictio_file):
		self.dictio = self.tupling(dictio_file)
		self.state = self.extractState()
		self.startProb = self.countStartProb()
		self.occurencesSt = self.occurencesState()
		self.bow = self.bagOfWord()
		self.transSt = self.coocurrences()
		self.emission = self.countEmission()
		return {'dictionary':self.dictio, 'state':self.state, 'start_probability':self.startProb, 'transition': self.transSt, 'emission':self.emission}
	
	def recall(self, observe_file):
		raw_observations = self.loadSentence(observe_file)
		result = []
		for sentence in raw_observations:
			observations =  self.extractObs(sentence)
			#print(observations)
			(probs, state_res) = self.callViterbi(observations)
			concluder = Concluder()
			conc = concluder.conc(self.state, state_res, observations)
			result.append(conc)
		return result