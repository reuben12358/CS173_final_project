import re
import editdistance
import bisect
import timeit
myDic = set()

def loadIntoDictionary(textfile):
	file = open(textfile,'r')
	text = file.read()
	for word in re.split(r'\W+', text):
		myDic.add(word)
def findKCloestWords(incorrectWords):   
    for word in myDic:
    	for incorrectWord in incorrectWords:
        	res = editdistance.eval(incorrectWord,word)
        	if res < 4:
        		bisect.insort(incorrectWords[incorrectWord],(res,word))
        		if len(incorrectWords[incorrectWord]) > len(word)/2:
        			incorrectWords[incorrectWord].pop()
    return incorrectWords
def sentenceInput(mySentence):
	errorDictionary = {}
	for word in re.split(r'\W+', mySentence):
		if word not in myDic:
			errorDictionary[word] = []
	errorDictionary = findKCloestWords(errorDictionary)
	return errorDictionary
if __name__ == "__main__":
	loadIntoDictionary('mobydick.txt')
	start = timeit.default_timer()
	result = sentenceInput("This is the test of how fast my code is and proof i do leetcode cause i am the TechLead best in Silicon Valley")
	stop = timeit.default_timer()
	print('Time: ', stop - start)
	print(result)

