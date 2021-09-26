from twitchio.ext import commands


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token='', #removed due to security reasons
                         nick='', #removed due to security reasons
                         prefix='!',
                         initial_channels=[''])

    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        print(message.content)


bot = Bot()
bot.run()
