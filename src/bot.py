import discord
import asyncio
import requests
import json
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import random

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='', intents=intents)
update_task = None

# Read the bot configuration from the config.json file
def read_config():
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config

# Get the bot prefix from the config.json file
def get_prefix(bot, message):
    config = read_config()
    prefix = config['PREFIX']
    return commands.when_mentioned_or(prefix)(bot, message)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.command(description='Start the weather updates.')
async def weatherstart(ctx):
    global update_task
    if update_task and not update_task.done():
        await ctx.send('Weather updates are already running.')
    else:
        update_task = bot.loop.create_task(update_weather(ctx))
        await ctx.send('Weather updates started.')

async def update_weather(ctx):
    config = read_config()
    channel_id = config['CHANNEL_ID']
    api_key = config['API_KEY']
    city_location = config['LOCATION']

    channel = bot.get_channel(int(channel_id))
    url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city_location}&days=5'
    response = requests.get(url)
    data = response.json()

    # Extract the current weather information
    current = data['current']
    current_condition = current['condition']['text']
    current_temp = current['temp_c']
    current_wind_speed = current['wind_kph']
    current_humidity = current['humidity']
    current_pressure = current['pressure_mb']

    # Extract the forecast information for the next 5 days
    forecast = data['forecast']['forecastday']
    forecast_data = []
    for day in forecast:
        date = day['date']
        max_temp = day['day']['maxtemp_c']
        min_temp = day['day']['mintemp_c']
        condition = day['day']['condition']['text']
        forecast_data.append(f"\n\n## {date}\n\n**Max Temp**: {max_temp}°C\n**Min Temp**: {min_temp}°C\n**Condition**: {condition}\n")

    # Create the weather message content
    message_content = f'# Current Weather\n\n'
    message_content += f'**Current Condition**: {current_condition}\n'
    message_content += f'**Current Temperature**: {current_temp}°C\n'
    message_content += f'**Wind Speed**: {current_wind_speed} km/h\n'
    message_content += f'**Humidity**: {current_humidity}%\n'
    message_content += f'**Pressure**: {current_pressure} mb\n\n'
    message_content += f'## 3-Day Forecast\n{"".join(forecast_data)}'

    # Send a new weather message
    message = await channel.send(message_content)

    while True:
        # Wait for 15 minutes
        await asyncio.sleep(900)

        # Fetch the latest weather data
        response = requests.get(url)
        data = response.json()

        # Extract the updated weather information
        current = data['current']
        current_condition = current['condition']['text']
        current_temp = current['temp_c']
        current_wind_speed = current['wind_kph']
        current_humidity = current['humidity']
        current_pressure = current['pressure_mb']

        # Extract the updated forecast information
        forecast = data['forecast']['forecastday']
        forecast_data = []
        for day in forecast:
            date = day['date']
            max_temp = day['day']['maxtemp_c']
            min_temp = day['day']['mintemp_c']
            condition = day['day']['condition']['text']
            forecast_data.append(f"\n\n## {date}\n\n**Max Temp**: {max_temp}°C\n**Min Temp**: {min_temp}°C\n**Condition**: {condition}\n")

        # Update the weather message content
        message_content = f'# Current Weather\n\n'
        message_content += f'**Current Condition**: {current_condition}\n'
        message_content += f'**Current Temperature**: {current_temp}°C\n'
        message_content += f'**Wind Speed**: {current_wind_speed} km/h\n'
        message_content += f'**Humidity**: {current_humidity}%\n'
        message_content += f'**Pressure**: {current_pressure} mb\n\n'
        message_content += f'## 5-Day Forecast\n{"".join(forecast_data)}'

        # Edit the weather message
        await message.edit(content=message_content)

@bot.command(description='Stop the weather updates.')
async def weatherstop(ctx):
    global update_task
    if update_task and not update_task.done():
        update_task.cancel()
        await ctx.send('Weather updates stopped.')
    else:
        await ctx.send('Weather updates are not running.')

@bot.command(description='Set a countdown in seconds.')
async def countdown(ctx, seconds: int):
    if seconds <= 0:
        await ctx.send('Countdown duration must be greater than zero.')
        return

    end_time = datetime.utcnow() + timedelta(seconds=seconds)

    countdown_message = await ctx.send(f'Remaining Time: {seconds} seconds')

    while datetime.utcnow() < end_time:
        remaining_time = end_time - datetime.utcnow()
        remaining_seconds = int(remaining_time.total_seconds())

        await countdown_message.edit(content=f'Remaining Time: {remaining_seconds} seconds')

        await asyncio.sleep(1)

    await countdown_message.edit(content='Countdown has ended.')

@bot.command(description='Clear a specified number of messages.')
async def clear(ctx, amount: int):
    if amount <= 0:
        await ctx.send('Please specify a valid number of messages to clear.')
        return

    # Delete the specified number of messages
    deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to account for the command message
    await ctx.send(f'Successfully deleted {len(deleted) - 1} messages.')

@bot.command(description='Ping the bot to check its response time.')
async def ping(ctx):
    # Calculate the bot's latency in milliseconds
    latency = round(bot.latency * 1000)

    # Send the ping response
    await ctx.send(f'Pong! Bot latency is {latency}ms.')

@bot.command()
async def serverinfo(ctx):
    server_name = ctx.guild.name
    total_members = ctx.guild.member_count
    creation_date = ctx.guild.created_at.strftime("%Y-%m-%d %H:%M:%S")

    await ctx.send(f"Server: {server_name}\nTotal members: {total_members}\nCreated at: {creation_date}")

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    # Retrieve user information
    username = member.name
    user_id = member.id
    joined_at = member.joined_at.strftime("%Y-%m-%d %H:%M:%S")

    # Send the user information as a message
    await ctx.send(f"User: {username}\nID: {user_id}\nJoined at: {joined_at}")

@bot.command()
async def roll(ctx, number: int):
    # Generate a random number between 1 and the specified number
    rolled_number = random.randint(1, number)
    await ctx.send(f"You rolled: {rolled_number}")

# Update the bot prefix dynamically
bot.command_prefix = get_prefix

# Read the bot token from the config.json file
def read_token():
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config['BOT_TOKEN']

def main():
    token = read_token()
    bot.command_prefix = get_prefix  # Set the initial command prefix
    bot.run(token)

if __name__ == '__main__':
    main()