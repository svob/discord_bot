import discord
import asyncio
from discord.ext import commands
import urllib.request
from bs4 import BeautifulSoup
import requests
import datetime
from datetime import timezone

client = discord.Client()
bot = commands.Bot(command_prefix='!', description='description')

@bot.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
@asyncio.coroutine
def nasrat():
    yield from bot.say(':poop:')

@bot.command(pass_context=True)
@asyncio.coroutine
def fak(ctx, name : str):
    member = discord.utils.find(lambda m: m.name == name, ctx.message.server.members)
    yield from bot.say('<@{0}> :middle_finger:'.format(member.id))

@bot.command()
@asyncio.coroutine
def metin():
    output = yield from get_metin_status()
    yield from bot.say(output)

@asyncio.coroutine
def get_metin_status():
    html = urllib.request.urlopen("https://fsvoboda.cz/metin_server_check.php").read()
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.table.tbody.find_all('tr')
    output = "```"
    for index, value in enumerate(rows):
        output += 'channel ' + str(index) + ': ' + value.find_all('td')[1].text + '\n'
    output += '```'
    return output

@bot.command()
@asyncio.coroutine
def weather(*, location : str):
    response = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&APPID=7548ef8367fa5bc386a6cf12f580b4fd'.format(location))
    if response.status_code != 200:
        raise BaseException("nejde to")
    json = response.json()
    sunrise = datetime.datetime.utcfromtimestamp(int(json['sys']['sunrise']))
    sunset = datetime.datetime.utcfromtimestamp(int(json['sys']['sunset']))
    sunrise = sunrise.replace(tzinfo=timezone.utc).astimezone(tz=None)
    sunset = sunset.replace(tzinfo=timezone.utc).astimezone(tz=None)
    yield from bot.say('{}, {}: {}, temperature: {:.2f}, sunrise: {}, sunset: {}'.format(json['name'], json['sys']['country'], json['weather'][0]['description'], json['main']['temp'] - 273.15, sunrise.strftime('%H:%M:%S'), sunset.strftime('%H:%M:%S')))


bot.run('MjExMTg2MjM1MTM2NDA5NjAy.CoZqcw.OqHdofazkXjcLUzzDGmcXNI2tg4')