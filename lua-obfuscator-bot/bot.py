import discord
import re
import random
import string
import time
import os

intents = discord.Intents.default()
intents.members = True
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

if not os.path.exists('obfuscated'):
    os.makedirs('obfuscated')

# Config:

config_token = ""
config_thumbnail_url = ""
config_icon_url = ""
config_failtitle = "**FEHLER**"
config_footer = "© onkelseo 2022"
config_watermark = "-- MADE BY onkelseo\n-- OBFUSCATE WITH onkelseo-lua-obfuscator\n\n"
config_repeat = 3

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!obfuscate'):
        if len(message.attachments) == 0:

            embed = discord.Embed(title=config_failtitle, description='Please attach a file!', color=discord.Color.red())
            embed.set_footer(text=config_footer, icon_url=config_icon_url)
            embed.set_thumbnail(url=config_thumbnail_url)
            await message.channel.send(embed=embed)
            return


        attachment = message.attachments[0]
        if not attachment.filename.lower().endswith('.lua'):

            embed = discord.Embed(title=config_failtitle, description='Please attach a `.lua` file!', color=discord.Color.red())
            embed.set_footer(text=config_footer, icon_url=config_icon_url)
            embed.set_thumbnail(url=config_thumbnail_url)
            await message.channel.send(embed=embed)
            return

        attachment_content = await attachment.read()

        code = attachment_content.decode('utf-8')

        obfuscated_code = obfuscate_lua(code)
        obfuscation_time = round(time.time() - message.created_at.timestamp(), 0)

        obfuscated_code = f'{config_watermark}\n{obfuscated_code}'

        timestamp = int(time.time())
        filename = f'obfuscated/obfuscated_{timestamp}.lua'
        original_filename = f'obfuscated/original_{timestamp}.lua'

        with open(original_filename, 'w', encoding='utf-8') as f:
            f.write(code)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(obfuscated_code)

        obfuscated_file = discord.File(filename)
        response = f"**Here is your obfuscated code, {message.author.mention}! It took {obfuscation_time} seconds to obfuscate!**"

        await message.channel.send(response, file=obfuscated_file)

def obfuscate_lua(code):
    try:
        code = re.sub(r'--.*', '', code)

        code = ''.join(code.split())

        variables = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)', code)
        for var in variables:
            new_var = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=len(var)))
            code = code.replace(var, new_var)

        functions = re.findall(r'function([a-zA-Z_][a-zA-Z0-9_]*)', code)
        for func in functions:
            new_func = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=len(func)))
            code = code.replace(f'function{func}', f'function {new_func}')

        random_string = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=random.randint(10, 20)))
        obfuscated_code = f'return({random_string}{code}{random_string})()'

        num_repeats = (config_repeat)
        for i in range(num_repeats):
            obfuscated_code += obfuscated_code

        return obfuscated_code

    except Exception as e:
        print(e)
        return code

client.run(config_token)







