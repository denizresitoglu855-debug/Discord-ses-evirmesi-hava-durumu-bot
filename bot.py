import discord
from discord.ext import commands
import requests
import pyttsx3
import random
import time


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix='?',
    intents=intents
)

engine = pyttsx3.init()

BOT_START_TIME = time.time()

user_memory = {}


def get_weather(city: str) -> str:

    base_url = "https://wttr.in/{}?format=%C+%t".format(city)

    response = requests.get(
        base_url
    )

    if response.status_code == 200:

        return response.text.strip()

    else:

        return (
            "hava durumu bilgisi alınamadı "
            "Şehir bilgisi girmeyi deneyebilirsiniz.."
        )


@bot.command()
async def start(ctx):

    await ctx.send(
        "Merhaba, Ben hava durumu tahminini "
        "sesli olarak söyleyen bir botum."
    )


@bot.command()
async def weather(
    ctx,
    *,
    city: str
):

    weather_info = get_weather(city)

    await ctx.send(
        "{} hava durumu: {}".format(
            city,
            weather_info
        )
    )

    speak(weather_info)


def speak(text: str):

    engine.say(text)

    engine.runAndWait()


@bot.event
async def on_ready():

    print("=" * 50)
    print("BOT ONLINE")
    print("Bot: {}".format(bot.user))
    print("ID: {}".format(bot.user.id))
    print("Sunucular: {}".format(len(bot.guilds)))
    print("=" * 50)

    await bot.change_presence(
        activity=discord.Game(
            name="?help | Bot"
        )
    )


@bot.command(name="help")
async def help_command(ctx):

    embed = discord.Embed(
        title="Bot - Komutlar",
        description="Kullanabileceğin komutlar:",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="Hava Durumu",
        value=(
            "`?weather şehir`\n"
            "`?start`"
        ),
        inline=False
    )

    embed.add_field(
        name="Asistan",
        value=(
            "`?ask mesaj`\n"
            "`?memory`"
        ),
        inline=False
    )

    embed.add_field(
        name="Sistem",
        value=(
            "`?ping`\n"
            "`?uptime`\n"
            "`?status`\n"
            "`?serverinfo`\n"
            "`?userinfo`"
        ),
        inline=False
    )

    embed.add_field(
        name="Eğlence",
        value=(
            "`?roll`\n"
            "`?coinflip`"
        ),
        inline=False
    )

    embed.add_field(
        name="Moderasyon",
        value=(
            "`?clear miktar`\n"
            "`?poll soru`"
        ),
        inline=False
    )

    embed.add_field(
        name="Ses",
        value="`?speak_command mesaj`",
        inline=False
    )

    await ctx.send(
        embed=embed
    )


@bot.command()
async def ask(
    ctx,
    *,
    message: str
):

    user_id = ctx.author.id

    if user_id not in user_memory:

        user_memory[user_id] = []

    user_memory[user_id].append(
        message
    )

    if len(user_memory[user_id]) > 10:

        user_memory[user_id] = (
            user_memory[user_id][-10:]
        )

    text = message.lower()

    if any(
        word in text
        for word in [
            "merhaba",
            "selam",
            "hello",
            "hey"
        ]
    ):

        response = "Selam {}.".format(
            ctx.author.display_name
        )

    elif (
        "nasılsın" in text
        or "nasilsin" in text
    ):

        response = (
            "Sistemler stabil.\n"
            "Discord bağlantısı: ONLINE\n"
            "Bot: ONLINE"
        )

    elif "kod" in text:

        response = "Kod modu aktif."

    elif "discord" in text:

        response = "Discord modülü aktif."

    elif (
        "teşekkür" in text
        or "tesekkur" in text
    ):

        response = "Rica ederim."

    else:

        responses = [
            "İlginç. Bunu biraz daha açar mısın?",
            "Bunu anladım. Devam edelim.",
            "İşlem yapıyorum.",
            "Tamam. Yeni komutunu bekliyorum.",
            "Sistem not aldı."
        ]

        response = random.choice(
            responses
        )

    await ctx.send(
        response
    )


@bot.command()
async def memory(ctx):

    user_id = ctx.author.id

    if user_id not in user_memory:

        await ctx.send(
            "Henüz kayıtlı bir konuşman yok."
        )

        return

    memories = user_memory[user_id]

    text = "\n".join(
        "- {}".format(item)
        for item in memories
    )

    embed = discord.Embed(
        title="Bot - Hafıza",
        description=text,
        color=discord.Color.blue()
    )

    await ctx.send(
        embed=embed
    )


@bot.command()
async def ping(ctx):

    latency = round(
        bot.latency * 1000
    )

    await ctx.send(
        "Pong! {} ms".format(
            latency
        )
    )


@bot.command()
async def uptime(ctx):

    total_seconds = int(
        time.time() - BOT_START_TIME
    )

    hours = total_seconds // 3600

    minutes = (
        total_seconds % 3600
    ) // 60

    seconds = (
        total_seconds % 60
    )

    await ctx.send(
        "Uptime: {} saat {} dakika {} saniye"
        .format(
            hours,
            minutes,
            seconds
        )
    )


@bot.command()
async def serverinfo(ctx):

    guild = ctx.guild

    embed = discord.Embed(
        title="Bot - Sunucu Bilgileri",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="Sunucu",
        value=guild.name,
        inline=True
    )

    embed.add_field(
        name="ID",
        value=guild.id,
        inline=True
    )

    embed.add_field(
        name="Üye",
        value=guild.member_count,
        inline=True
    )

    embed.add_field(
        name="Kanal",
        value=len(guild.channels),
        inline=True
    )

    embed.add_field(
        name="Rol",
        value=len(guild.roles),
        inline=True
    )

    await ctx.send(
        embed=embed
    )


@bot.command()
async def userinfo(
    ctx,
    member: discord.Member = None
):

    if member is None:

        member = ctx.author

    embed = discord.Embed(
        title="Bot - Kullanıcı Bilgileri",
        color=discord.Color.blue()
    )

    embed.set_thumbnail(
        url=member.display_avatar.url
    )

    embed.add_field(
        name="Kullanıcı",
        value=member.name,
        inline=True
    )

    embed.add_field(
        name="ID",
        value=member.id,
        inline=True
    )

    await ctx.send(
        embed=embed
    )


@bot.command()
async def roll(
    ctx,
    maximum: int = 100
):

    if maximum < 1:

        await ctx.send(
            "Sayı 1 veya daha büyük olmalı."
        )

        return

    if maximum > 1000000:

        await ctx.send(
            "Maksimum değer 1.000.000."
        )

        return

    number = random.randint(
        1,
        maximum
    )

    await ctx.send(
        "{} attın: {}".format(
            ctx.author.display_name,
            number
        )
    )


@bot.command()
async def coinflip(ctx):

    result = random.choice(
        [
            "Yazı",
            "Tura"
        ]
    )

    await ctx.send(
        "Sonuç: {}".format(
            result
        )
    )


@bot.command()
@commands.has_permissions(
    manage_messages=True
)
async def clear(
    ctx,
    amount: int = 10
):

    if amount < 1:

        await ctx.send(
            "Miktar en az 1 olmalı."
        )

        return

    if amount > 100:

        await ctx.send(
            "En fazla 100 mesaj silebilirim."
        )

        return

    deleted = await ctx.channel.purge(
        limit=amount + 1
    )

    message = await ctx.send(
        "{} mesaj temizlendi."
        .format(
            len(deleted) - 1
        )
    )

    await discord.utils.sleep_until(
        discord.utils.utcnow()
        + __import__("datetime").timedelta(
            seconds=3
        )
    )

    try:

        await message.delete()

    except discord.HTTPException:

        pass


@bot.command()
async def poll(
    ctx,
    *,
    question: str
):

    embed = discord.Embed(
        title="Bot - Anket",
        description=question,
        color=discord.Color.blue()
    )

    message = await ctx.send(
        embed=embed
    )

    await message.add_reaction("👍")
    await message.add_reaction("👎")


@bot.command()
async def say(
    ctx,
    *,
    text: str
):

    await ctx.send(
        text
    )


@bot.command()
async def speak_command(
    ctx,
    *,
    text: str
):

    await ctx.send(
        "Bot konuşuyor..."
    )

    speak(text)


@bot.command()
async def status(ctx):

    latency = round(
        bot.latency * 1000
    )

    embed = discord.Embed(
        title="Bot - Durum",
        color=discord.Color.green()
    )

    embed.add_field(
        name="Discord",
        value="ONLINE",
        inline=True
    )

    embed.add_field(
        name="Latency",
        value="{} ms".format(
            latency
        ),
        inline=True
    )

    embed.add_field(
        name="Sunucular",
        value=str(
            len(bot.guilds)
        ),
        inline=True
    )

    embed.add_field(
        name="Kullanıcı",
        value=str(
            len(bot.users)
        ),
        inline=True
    )

    await ctx.send(
        embed=embed
    )


bot.run(
    "token"
)
