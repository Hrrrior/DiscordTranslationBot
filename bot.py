#!python3.9
from secret import AZURE_KEY, DISCORD_KEY, AZURE_LOCATION
from discord import Game
from discord.ext import commands
import json
import uuid
import requests
import pykakasi
import wanakana

# https://github.com/Starwort/wanakana-py
# https://github.com/miurahr/pykakasi
# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot

subscription_key = AZURE_KEY
endpoint = "https://api.cognitive.microsofttranslator.com"

location = AZURE_LOCATION

path = '/translate'
constructed_url = endpoint + path

headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

kks = pykakasi.kakasi()
bot = commands.Bot(command_prefix=".")
url = "https://google-translate1.p.rapidapi.com/language/translate/v2"


def translation_request(input_text, langFrom, langTo):
    body = [{
        'text': f'{input_text}'
    }]

    params = {
        'api-version': '3.0',
        'from': f'{langFrom}',
        'to': [f'{langTo}']
    }
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    data = json.loads(request.text)
    return data[0]["translations"][0]["text"]


def romajii_convert(input_text):
    result = kks.convert(input_text)
    romajii_output = ""
    for item in result:
        romajii_output += item['hepburn']
        romajii_output += " "
    return romajii_output


@bot.event
async def on_ready():
    await bot.change_presence(activity=Game(name="マイクロソフトトランスレータ"))
    print("Botto no junbi ga dekimashita.")


@bot.command(aliases=['english'], help="Translate English to Japanese")
async def eng(ctx, *, input_text):
    if len(input_text) > 700:
        await ctx.send("I will only translate up to 700 characters.")
        return
    resp = translation_request(input_text, 'en', 'ja')
    romajii_output = romajii_convert(resp)
    await ctx.send(f":flag_gb: English to Japanese :flag_jp: : "
                   f"\n {resp} "
                   f"\n {romajii_output}")


@bot.command(aliases=['eesti'], help="Translate Estonian to Japanese")
async def est(ctx, *, input_text):
    if len(input_text) > 700:
        await ctx.send("I will only translate up to 700 characters.")
        return
    resp = translation_request(input_text, 'et', 'ja')
    romajii_output = romajii_convert(resp)
    await ctx.send(f":flag_ee: Estonian to Japanese :flag_jp: : "
                   f"\n {resp} "
                   f"\n {romajii_output}")


@bot.command(aliases=['jaapani', 'japanese'], help="Translate Japanese to Inferior Languages")
async def jap(ctx, *, input_text):
    if len(input_text) > 700:
        await ctx.send("I will only translate up to 700 characters.")
        return
    resp1 = translation_request(input_text, 'ja', 'en')
    resp2 = translation_request(input_text, 'ja', 'et')
    await ctx.send(
        f":flag_jp: Japanese to English :flag_gb: : "
        f"\n {resp1} "
        f"\n :flag_jp: Japanese to Estonian :flag_ee: : "
        f"\n {resp2}")


@bot.command(aliases=['romajii', 'weeb', 'weebanese'], help="Translate Romajii to Inferior Languages")
async def rom(ctx, *, input_text):
    if len(input_text) > 700:
        await ctx.send("I will only translate up to 700 characters.")
        return
    if wanakana.is_romaji(input_text):
        input_text = wanakana.to_kana(input_text)
        resp1 = translation_request(input_text, 'ja', 'en')
        resp2 = translation_request(input_text, 'ja', 'et')
        await ctx.send(
            f":flag_jp: Romajii to English :flag_gb: : "
            f"\n {resp1} "
            f"\n :flag_jp: Romajii to Estonian :flag_ee: : "
            f"\n {resp2}")
        return
    await ctx.send("Insert valid data loser.")


@bot.command(aliases=['d'], help="Bot description")
async def description(ctx):
    await ctx.send(
        "```\n Simple bot for translations between English, Estonian & Japanese, Romajii "
        "\n Big thanks to Azure Translation API, pykakasi & wanakana. "
        "\n Built by Herrior. \n May feature bugs and edge cases. "
        "\n .jap = Japanese Alphabet -> English, Estonian "
        "\n .eng = English -> Japanese, Romajii "
        "\n .est = Estonian -> Japanese, Romajii "
        "\n .rom = Romajii -> English, Estonian (Not perfect)```")


bot.run('DISCORD_KEY')
