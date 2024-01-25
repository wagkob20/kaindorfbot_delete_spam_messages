import discord
from discord.ext import commands
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

import discord
from discord.ext import commands
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

last_messages = {}

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = message.author.id
    message_content = message.content
    channel_id = message.channel.id
    message_id = message.id
    timestamp = datetime.now()

    key = (user_id, message_content)

    if key in last_messages:
        last_channel_id, last_message_id, last_timestamp = last_messages[key]

        if last_channel_id != channel_id:
            log_channel_id = "channel_id"  
            log_channel = bot.get_channel(int(log_channel_id))
            if log_channel:
                await log_channel.send(f"User {message.author} (ID: {user_id}) hat die Nachricht '{message_content}' in mehreren Kanälen gesendet.")
            
            await message.author.timeout(timedelta(minutes=5), reason="Wiederholte Nachricht in verschiedenen Kanälen")
            
            other_channel = bot.get_channel(last_channel_id)
            if other_channel:
                try:
                    other_message = await other_channel.fetch_message(last_message_id)
                    await other_message.delete()
                except discord.NotFound:
                    pass
            await message.delete()

        elif channel_id == last_channel_id and (timestamp - last_timestamp) < timedelta(minutes=1):
            await message.delete()
            return

    last_messages[key] = (channel_id, message_id, timestamp)


bot.run("bot_token")
