import discord
from discord.ext import commands, tasks
import schedule
from pytz import timezone
import asyncio
import os
from dotenv import load_dotenv
import random

load_dotenv()

intents = discord.Intents.default()
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    schedule.every(2).weeks.friday.at("22:00", timezone('America/Mexico_City')).do(create_teams)

async def create_teams():
    message_id = 12421
    channel_id = os.getenv('CHANNEL_ID')
    team_sz = 3

    channel = bot.get_channel(channel_id)
    message = await channel.fetch_message(message_id)

    reactions = message.reactions
    users = []
    for reaction in reactions:
        async for user in reaction.users():
            users.append(user)
    random.shuffle(users)

    teams = [users[i:i + team_sz] for i in range(0, len(users), team_sz)]

    for i, team in enumerate(teams):
        team_str = ', '.join([user.name for user in team])
        await channel.send(f'Team {i + 1}: {team_str}')


async def run_schedule():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

bot.loop.create_task(run_schedule())

bot.run(os.getenv('BOT_TOKEN'))