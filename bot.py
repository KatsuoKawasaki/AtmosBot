import asyncio
import disnake, config
from disnake.ext import commands
import os



# путь к токену
try:
    with open('token.txt', 'r') as f:
        token = f.read()
except:
    with open('token.txt', 'w+') as f:
        print('Токен дай!')
        input()
else:
    print('Соединение')

administrators = [630312643504373771]
prefix = '%'
bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')

bot.load_extension("cogs.moderation")
bot.load_extension("cogs.events")
bot.load_extension("cogs.Moderations")
bot.load_extension("cogs.Owner")
bot.load_extension("cogs.General")
bot.load_extension("cogs.Template")


# сообщение о вкл. и статус.
@bot.event
async def on_ready():
    print('Саламалейкум')
    await bot.change_presence(status = disnake.Status.dnd, activity = disnake.Game('prefix - %'))

# Для проверки
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f'{ctx.author.mention} Правила знаешь? Выбрось его!')



bot.run(token)