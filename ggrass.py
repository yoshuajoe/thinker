from ner_clean import NER
from concluder import Concluder
from difflib import SequenceMatcher
from proc_conj_AND import ProcAND
import itertools
import re

ner = NER()
asdfgh = ner.train("anno_corp.txt")
sun = ner.recall("ori_corp.txt")

newsen = ner.loadSentence("ori_corp.txt")
bigres = []

def similar(a, b):
	return SequenceMatcher(None, a, b).ratio()

for i in range(len(newsen)):
	res = []
	for j in newsen[i].split(" "):
		for k in sun[i]:
			if j==k[1]:
				res.append((k[0], j))
				break
	bigres.append(res)

bigres2 = []
for g in bigres:
	res = []
	indexer=[]
	for d in range(len(g)-1):
		if g[d][0] == g[d+1][0]:
			cat = g[d][1]+" "+g[d+1][1]
			g[d+1]=(g[d][0],cat)
			#del g[d]
			g[d] = (None,None)
			indexer.append(g[d])
	for o in indexer:
		g.remove(o)
	bigres2.append(g)

#print(bigres2)
#entity resolution
enres = []
for bg in bigres2:
	for cbg in bg:
		if cbg[0] == "PER":
			enres.append(cbg)

memo_enres = []
for name_a in enres:
	count = 0
	for name in enres:
		count  = count + 1
		if similar(name_a[1], name[1]) >= 0.5:
			if(len(name_a[1]) >= len(name[1])):
				memo_enres.append((enres[count-1], name_a))
				enres[count-1] = name_a
			else:
				memo_enres.append((enres[count-1], name))
				enres[count-1] = name

for memo in memo_enres:
	ct = 0
	for bgr in bigres2:
		count = 0
		for bg in bgr:
			#print(memo[0])
			if bg[1] == memo[0][1]:
				#print(bigres2[ct][count][1])
				#print(memo[1])
				bigres2[ct][count] = memo[1]
			count = count +1
		ct = ct+1

str = ""
for bg in bigres2:
	for b in bg:
		str = str+b[1]+" "
	str = str[0:len(str)-1]
	str = str +". "

pAND = ProcAND()
#print(pAND.proceed(bigres2))

#print(str)
#coreference matcher
#sorry i skip this due to laziness in reading paper

#print(bigres2)
#print sun

prevState = ""
prevWord = ""
sentence = []
#if prevState == "":
	#prevState = sun[0][0][0]
#rint prevState
	
for i in range(0, len(sun[0])):
	print sun[0][i]
	if prevState == sun[0][i][0]:
		str = '%s %s'%(sun[0][i-1][1], sun[0][i][1])
		sentence.append((sun[0][i][0], str))
		sentence[i-1] = None
	else:
		sentence.append((sun[0][i][0], sun[0][i][1]))
	prevState = sun[0][i][0]
	prevWord = sun[0][i][1]

new_sen = [sd for sd in sentence if sd is not None]
print new_sen