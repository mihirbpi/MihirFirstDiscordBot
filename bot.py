# bot.py
import os
import random
import discord
import geocoder
from yelpapi import YelpAPI
from discord.ext import commands
from dotenv import load_dotenv

# Load API keys from environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
YELP_API_KEY = os.getenv("YELP_API_KEY")

# Initialize bot and yelp API
bot = commands.Bot(command_prefix='$')
yelp_api = YelpAPI(YELP_API_KEY)

# Define commands:

# $roll_dice command
@bot.command(name='roll_dice', help='Simulates rolling dice.')

async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

# $yelp command
@bot.command(name='yelp', help="""Searches Yelp. Required parameters:\n
                                search_text: text to search (put inside "" quotes if it has spaces),\n
                                location: location (put inside "" quotes if it has spaces),\n
                                n: Which result to return (returns nth result).""")

async def yelp_query(ctx, search_text: str, location: str, n: int):
    search_results = yelp_api.search_query(term=search_text, location=location)

    if(int(n) > search_results['total']):
        await ctx.send("not enough results")

    else:
        place = search_results['businesses'][int(n)-1]['url']
        await ctx.send(place)

# Run the bot
bot.run(DISCORD_TOKEN)
