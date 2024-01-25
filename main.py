import discord
from discord.ext import commands
from datetime import timedelta

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

    key = (user_id, message_content)

    if key in last_messages and last_messages[key][0] != channel_id:
        log_channel = bot.get_channel("logchannelid-i-love-uiux")
        if log_channel:
            await log_channel.send(f"User {message.author} (ID: {user_id}) hat die Nachricht '{message_content}' in mehreren Kanälen gesendet.")

        await message.author.timeout(timedelta(minutes=5), reason="Wiederholte Nachricht in verschiedenen Kanälen")
        
        other_channel_id, other_message_id = last_messages[key]
        other_channel = bot.get_channel(other_channel_id)

        if other_channel:
            try:
                other_message = await other_channel.fetch_message(other_message_id)
                await other_message.delete()
            except discord.NotFound:
                pass 
        await message.channel.fetch_message(message_id)
        await message.delete()
    else:
        last_messages[key] = (channel_id, message_id)

bot.run("token-i-love-völk")
