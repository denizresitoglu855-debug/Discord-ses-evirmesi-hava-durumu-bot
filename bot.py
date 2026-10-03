import discord
from discord.ext import commands
import requests
import pyttx3



intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)
engine = pyttx3.init()



def get_weather(city: str) -> str:
    base_url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(base_url)
    if response.status_code == 200:
        return response.text.script()
    else:
        return "hava durumu bilgisi alınamadı Şehir bilgisi girmeyi deneyebilirsiniz.."





@bot.command()
async def start(ctx):
    await ctx.send("Merhaba, Ben hava durumu tahminini sesli olarak söyleyen bir botum.")


@bot.command()
async def weather(ctx, *,city:str):
    weather_info = get_weather(city)
    await ctx.send(f"{city} hava durumu: {weather_info}")
    speak(weather_info)


def speak(text: str):
    engine.say(text)
    engine.runAndWait()
    



bot.run("HEY İNSERT YOUR BİG TOKEN HERE :) -")
