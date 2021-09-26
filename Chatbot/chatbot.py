from Chat import Chat, reflections
import urllib
import json
import requests
import editdistance
import re
import sys
myDic = set()
CovidJson = None
uh = urllib.request.urlopen("https://api.covid19api.com/summary")
data = uh.read()
js = json.loads(data.decode("utf-8"))

userInput = ""
chat = Chat(reflections)
def buildJson(js):
    Countries = {}
    countryList = js["Countries"]
    for country in countryList:

        Countries[country["Country"]] = country
    return Countries
CountryList = buildJson(js)
def buildDictionary():
    #file = open('words.txt','r')
    #text = file.read()
    text = "my name is what is your name how are you sorry want created hi hello hey age location city how is weather in i work in raining in health sportsperson sports moviestar actor quit  Covid19  died die death  Trump"
    for word in re.split(r'\W',text):
        myDic.add(word)
        myDic.add(word.lower())
def autoCorrect(sentence):
    wordList = []
    for word in re.split(r'\W',sentence):
        wordList.append(word)
    for wordIndex, word in enumerate(wordList):
        if word not in myDic:
            minDistance = sys.maxsize
            minDistanceWord = ""
            for dicWord in myDic:
                res = editdistance.eval(word,dicWord)
                if res < minDistance:
                    minDistanceWord = dicWord
                    minDistance = res
            wordList[wordIndex] = minDistanceWord
    newSentence = ""
    for word in wordList:
        newSentence += "word" + " "
    newSentence = newSentence[:-1]
    if sentence[len(sentence)-1:] == '?' or sentence[len(sentence)-1:] == '.':
        newSentence += sentence[len(sentence)-1:]
    return newSentence


def trumpMsg():
    response = requests.get("https://api.whatdoestrumpthink.com/api/v1/quotes/random")
    apiResponse = (response.json())
    return apiResponse["message"]
def correctCountry(invalidCountry,CountryList):
    minDistance = sys.maxsize
    minDistanceWord = ""
    for country in CountryList:
        res = editdistance.eval(country,invalidCountry)
        if res < minDistance:
            minDistance = res
            minDistanceWord = country
    return minDistanceWord
def covidCountry(country):
    #print(country)

    #print(CountryList)
    if country not in CountryList:
        country = correctCountry(country,CountryList)
    newStr = "There are " + str(CountryList[country]['TotalConfirmed']) + " cases and " + str(CountryList[country]['TotalDeaths']) + " deaths in " + country
    return newStr
def covid19(header = "TotalDeaths"):


    return str(js["Global"][header])


pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, How are you today ?",]
    ],
     [
        r"what is your name ?",
        ["My name is Chatty and I'm a chatbot ?",]
    ],
    [
        r"how are you ?",
        ["I'm doing good\nHow about You ?",]
    ],
    [
        r"sorry (.*)",
        ["Its alright","Its OK, never mind",]
    ],
    [
        r"i'm (.*) doing good",
        ["Nice to hear that","Alright :)",]
    ],
    [
        r"hi|hey|hello",
        ["Hello", "Hey there",]
    ],
    [
        r"(.*) age ?",
        ["I'm a computer program dude\nSeriously you are asking me this?",]

    ],
    [
        r"what (.*) want ?",
        ["Make me an offer I can't refuse",]

    ],
    [
        r"(.*) created ?",
        ["Nagesh created me using Python's NLTK library ","top secret ;)",]
    ],
    [
        r"(.*) (location|city) ?",
        ['Chennai, Tamil Nadu',]
    ],
    [
        r"how is weather in (.*)?",
        ["Weather in %1 is awesome like always","Too hot man here in %1","Too cold man here in %1","Never even heard about %1"]
    ],
    [
        r"i work in (.*)?",
        ["%1 is an Amazing company, I have heard about it. But they are in huge loss these days.",]
    ],
[
        r"(.*)raining in (.*)",
        ["No rain since last week here in %2","Damn its raining too much here in %2"]
    ],
    [
        r"how (.*) health(.*)",
        ["I'm a computer program, so I'm always healthy ",]
    ],
    [
        r"(.*) (sports|game) ?",
        ["I'm a very big fan of Football",]
    ],
    [
        r"who (.*) sportsperson ?",
        ["Messy","Ronaldo","Roony"]
],
    [
        r"who (.*) (moviestar|actor)?",
        ["Brad Pitt"]
],
    [
        r"quit",
        ["BBye take care. See you soon :) ","It was nice talking to you. See you soon :)"]
],
    [
        r"(.*)Trump(.*)",
        [trumpMsg()]
],
    [
        r"(.*)(death|died|die)(.*)Covid19(.*)",
        [covid19("TotalDeaths") + " have died in the world"]

    ],
    [
        r"(.*)(cases|case)(.*)Covid19(.*)",
        [covid19("TotalConfirmed")+ " cases of Covid19"]
    ],
    [
        r"(.*)Covid19 in (.*)",
        ["Covid19 %2"]
    ]
]

def chatty():
    chat.buildPair(pairs)
    print("Hi, I'm Chatty and I chat alot ;)\nPlease type lowercase English language to start a conversation. Type quit to leave ") #default message at the start

    userInput = ""
    while userInput != "quit":
        try:
            userInput = input(">")
        except EOFError:
            print(userInput)
        if userInput:
            while userInput[-1] in "!. ":
                userInput = userInput[:-1]
            chatResponse = chat.respond(userInput)
            if chatResponse == None:
                newSentence = autoCorrect(userInput)
                chatResponse = chat.respond(newSentence)
            if re.split(r'\W+', chatResponse)[0] == "Covid19":
                #print(re.split(r'\W+', chatResponse)[1])
                print(covidCountry(re.split(r'\W+', chatResponse)[1]))
            else:
                print(chatResponse)
        if userInput == "quit":
            exit()

if __name__ == "__main__":

    buildDictionary()
    chatty()
    #print(covid19("TotalDeaths"))
