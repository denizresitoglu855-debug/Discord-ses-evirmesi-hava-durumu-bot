import asyncio
import os
from urllib.parse import quote

import discord
import pyttsx3
import requests
from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="?", intents=intents)
engine = pyttsx3.init()


def get_weather_data(city: str) -> dict:
    city_path = quote(city, safe="")
    response = requests.get(
        f"https://wttr.in/{city_path}?format=j1",
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def current_weather_text(data: dict) -> str:
    current = data["current_condition"][0]
    description = current["weatherDesc"][0]["value"]
    return (
        f"{description}, {current['temp_C']}°C "
        f"(hissedilen {current['FeelsLikeC']}°C), "
        f"nem %{current['humidity']}, "
        f"rüzgâr {current['windspeedKmph']} km/sa"
    )


@bot.command()
async def start(ctx):
    await ctx.send(
        "Merhaba! `?weather şehir` ile anlık hava durumunu, "
        "`?forecast şehir` ile 3 günlük tahmini öğrenebilirsin."
    )


@bot.command()
async def weather(ctx, *, city: str):
    try:
        data = await asyncio.to_thread(get_weather_data, city)
        weather_info = current_weather_text(data)
    except (requests.RequestException, ValueError, KeyError, IndexError) as error:
        await ctx.send(f"{city} için hava durumu alınamadı: {error}")
        return

    await ctx.send(f"{city} hava durumu: {weather_info}")
    speak(weather_info)


@bot.command()
async def forecast(ctx, *, city: str):
    try:
        data = await asyncio.to_thread(get_weather_data, city)
        days = data["weather"][:3]
        if not days:
            raise ValueError("Tahmin verisi bulunamadı.")

        embed = discord.Embed(
            title=f"{city} — 3 günlük hava tahmini",
            color=discord.Color.blue(),
        )
        for day in days:
            description = day["hourly"][4]["weatherDesc"][0]["value"]
            embed.add_field(
                name=day["date"],
                value=(
                    f"{description}\n"
                    f"En yüksek: {day['maxtempC']}°C · "
                    f"En düşük: {day['mintempC']}°C"
                ),
                inline=False,
            )
    except (requests.RequestException, ValueError, KeyError, IndexError) as error:
        await ctx.send(f"{city} için tahmin alınamadı: {error}")
        return

    await ctx.send(embed=embed)


def speak(text: str):
    engine.say(text)
    engine.runAndWait()


token = os.getenv("DISCORD_BOT_TOKEN")
if not token:
    raise RuntimeError(
        "Botu çalıştırmadan önce DISCORD_BOT_TOKEN ortam değişkenini ayarlayın."
    )

bot.run(token)
