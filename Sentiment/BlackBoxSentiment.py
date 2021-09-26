import argparse
import re
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import sys
import irc.bot
import requests
from threading import Thread
from twitchio.ext import commands
import asyncio

class BlackBoxSentiment:
    def __init__(self):
        self.inLoop = False
        #https://www.youtube.com/watch?v=5Kv3_V5wFgg

        self.wordRanking = {}
        self.client = language.LanguageServiceClient()
    def missing (self,text):
        client = language.LanguageServiceClient()
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)
        annotation = client.analyze_sentiment(document=document)
        score = annotation.document_sentiment.score
        return score
    def calculate(self,text):
        encoding_type = enums.EncodingType.UTF8
        document = types.Document(content=text ,type=enums.Document.Type.PLAIN_TEXT)
        response = self.client.analyze_entities(document, encoding_type=encoding_type)
        score = 0
        textSize = 0
        for word in re.split(r'\W+', text):
            if word not in self.wordRanking:
                wordScore = self.missing(word)
                if wordScore != 0:
                    self.wordRanking[word] = [1,wordScore]
                else:
                    continue
            textSize += 1
            res = self.wordRanking[word][1]/self.wordRanking[word][0]
            score += res
        if textSize == 0:
            return 0
        return score/textSize
    def train(self,text):
        """Run a sentiment analysis request on text within a passed filename."""
        document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
        annotation = self.client.analyze_sentiment(document=document)
        for sentence in annotation.sentences:
            score = sentence.sentiment.score
            #print(score)
            sentenceTxt = sentence.text.content
            sentenceAnalize = types.Document(content=sentenceTxt,type=enums.Document.Type.PLAIN_TEXT)
            #esponse = self.client.analyze_entities(document=sentenceAnalize)
        #print(response)
            for word in re.split(r'\W+', sentenceTxt):
                if word not in self.wordRanking:
                    self.wordRanking[word] = [1,score]
                else:
                    self.wordRanking[word][0] += 1
                    self.wordRanking[word][1] += score
def getInput(brain):
    while 1:
        userInput = input(">")
        print(brain.calculate(userInput))
class Bot(commands.Bot):

    def __init__(self,brain):
        self.brain = brain
        super().__init__(irc_token='oauth:1rq89fbmrczxg87fwtwjxla7mc8m1f', nick='overkilledit', prefix='!',
                         initial_channels=['overkilledit'])

    # Events don't need decorators when subclassed
    async def event_ready(self):
        return

    async def event_message(self, message):
        self.brain.train(message.content)



if __name__ == '__main__':
    brain = BlackBoxSentiment()
    bot = Bot(brain)
    t1 = Thread(target=getInput,args=(brain,))
    t1.start()
    bot.run()
