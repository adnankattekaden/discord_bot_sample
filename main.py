import discord
from discord.ext import commands
import os
from discord.utils import get

import mysql.connector as connector

db = connector.connect(host='localhost', user='root', password='admin', db='mulearn_bot')
cursor = db.cursor(dictionary=True)








GENERAL_CHANNEL = 1072592097116426323
WELCOME_CHANNEL = 1073769766382206998
REACTION_UPDATES = 1073860132670283857


from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True

client = commands.Bot(intents=intents,command_prefix='--')

@client.command(name='version')
async def version(context):
    print('version prints here')
    general_channel = client.get_channel(1072592097116426323)
    my_embed = discord.Embed(title="Current Version",description="V1.0",color=0x00ff00)
    my_embed.add_field(name="Version Code:",value="v1.0.0",inline=False)
    my_embed.add_field(name="Date Released",value="April 20 2002",inline=False)
    my_embed.set_footer(text="ss")
    my_embed.set_author(name="Hello")

    await context.message.channel.send(embed=my_embed)



load_dotenv()
TOKEN = os.getenv("TOKEN")

@client.event
async def on_ready():
        print(f'We have logged in as {client.user}')


@client.event
async def on_member_join(member):
    channel = client.get_channel(WELCOME_CHANNEL)
    embed=discord.Embed(title="Welcome!",description=f"{member.mention} Just Joined")
    await channel.send(embed=embed)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '/start':
        general_channel = client.get_channel(GENERAL_CHANNEL)
        my_embed = discord.Embed(title="Current Version",description="V1.0",color=0x00ff00)
        my_embed.add_field(name="Version Code:",value="v1.0.0",inline=False)
        my_embed.add_field(name="Date Released",value="April 20 2002",inline=False)
        my_embed.set_footer(text="ITs footer")
        my_embed.set_author(name="Adnan K")

        await general_channel.send(embed=my_embed)

    await client.process_commands(message)


@client.event
async def on_reaction_add(reaction,user):
    reaction_text = f"{user.name} gave reaction to {reaction.message.author.name}"
    reaction_channel = client.get_channel(REACTION_UPDATES)
    await reaction_channel.send(reaction_text)

@client.command(name="role")
async def create_role(ctx,role):
    existing_role = get(ctx.guild.roles,name=role)
    if existing_role:
        return

    new_role = await ctx.guild.create_role(name=role)
    await ctx.author.add_roles(new_role)
    await ctx.channel.send('heyy')
 


@client.command(name='register')
async def register_user(ctx,full_name):
    cursor.execute(f"select * from user where name = '{full_name}' ")
    myresult = cursor.fetchall()
    if myresult:
        await ctx.channel.send('user already exists')
        return

    cursor.execute(f"insert into user (name) VALUES ('{full_name}')")
    db.commit()


@client.command(name='names')
async def get_names(ctx):
    for i in ctx.author.roles:
        if i.name == 'boe':
            cursor.execute(f"select name from user ")
            myresult = cursor.fetchall()
            await ctx.channel.send(f"{myresult}")
            return



client.run(TOKEN)