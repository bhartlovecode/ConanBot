# Conan Exiles Discord Bot
# Author: Bradley Hartlove
# Version: 0.1

"""
Features:
(1): Store server information (IP, password) -> Loading...
(2): Search Conan Wiki Pages -> Loading...
(3): Track user's progess -> Loading...
(4): Easily share clips/screenshots -> Loading...
(5): Inform server of new updates: -> Loading...
"""

from asyncio.windows_events import NULL
import discord
from decouple import config
from crypt import encrypt
from helpers import *
from database import *
from crypt import *
import asyncio
import argparse

# Set up discord client
client = discord.Client()

# Create parser
update_parser = argparse.ArgumentParser()

# Add arguments
update_parser.add_argument('--name', type=str)
update_parser.add_argument('--ip', type=str)
update_parser.add_argument('--password', type=str)

# helpers
def err_check(arr, num_params):
    if len(arr) != num_params:
        embed = discord.Embed(description = "Error: Invalid formatting", color = get_color("red"))
        return True, embed
    return False, NULL

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    dbinit()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content

    #Feature (1) Store server information (IP, password)
    # add server
    if msg.startswith("$add_server"):
        split = msg.split()
        error, embed = err_check(split, 4)
        if error: 
            await message.channel.send(embed = embed)
        else:
            server_info = "IP: " + split[1] + "\nPassword: " + split[2] + "\nName: " + split[3]
            encIP = encrypt(split[1])
            encPassword = encrypt(split[2])
            name = split[3]
            embed = discord.Embed(title = "Add Server?", description = server_info + "\nY/N?", color = get_color("blue"))
            await message.channel.send(embed = embed)

            channel = message.channel
            author = message.author

            def check(m):
                return (m.content == 'Y' or m.content == 'y' or m.content == 'N' or m.content == "n") and m.channel == channel and m.author == author

            try:
                msg = await client.wait_for('message', check=check, timeout=60)
            except asyncio.TimeoutError:
                embed = discord.Embed(description = wrap_message("Cancled server add request"), color = get_color("red"))
                await channel.send(embed = embed)
            else:
                if (msg.content == "y" or msg.content == "Y"):
                    dbadd(name, encIP, encPassword, message.author)
                    embed = discord.Embed(title = "Added Server", de mOscription = server_info, color = get_color("green"))
                    await channel.send(embed = embed)
                else:
                    embed = discord.Embed(description = wrap_message("Cancled server add request"), color = get_color("red"))
                    await channel.send(embed = embed) 

    # get server
    elif msg.startswith("$get_server"):
        split = msg.split()
        error, embed = err_check(split, 2)
        if error: 
            await message.channel.send(embed = embed)
        else:
            name = split[1]
            success, output = dbget(name)  
            if success:
                embed = discord.Embed(title = name, description = output, color = get_color("blue"))
                await message.channel.send(embed = embed)
            else:
                embed = discord.Embed(title = name, description = output, color = get_color("red"))
                await message.channel.send(embed = embed) 

    # delete server
    elif msg.startswith("$delete_server"):
        split = msg.split()
        error, embed = err_check(split, 2)
        if error: 
            await message.channel.send(embed = embed)    
        else:
            name = split[1]
            success, output = dbget(name)
            if success:
                embed = discord.Embed(title = "Delete Server?", description = output + "\nY/N?", color = get_color("blue"))
                await message.channel.send(embed = embed)

                channel = message.channel
                author = message.author

                def check(m):
                    return (m.content == 'Y' or m.content == 'y' or m.content == 'N' or m.content == "n") and m.channel == channel and m.author == author

                try:
                    msg = await client.wait_for('message', check=check, timeout=60)
                except asyncio.TimeoutError:
                    embed = discord.Embed(description = wrap_message("Cancled server deletion request"), color = get_color("red"))
                    await channel.send(embed = embed)
                else:
                    if (msg.content == "y" or msg.content == "Y"):
                        success = dbdelete(name, author)
                        if success:
                            embed = discord.Embed(title = "Deleted Server", description = output, color = get_color("green"))
                            await channel.send(embed = embed)
                        else:
                            embed = discord.Embed(description = wrap_message("Error removing server (you must own the server to delete it"), 
                            color = get_color("red"))
                            await channel.send(embed = embed)
                    else:
                        embed = discord.Embed(description = wrap_message("Cancled server delete request"), color = get_color("red"))
                        await channel.send(embed = embed) 

            else:
                embed = discord.Embed(title = name, description = output, color = get_color("red"))
                await message.channel.send(embed = embed) 
  

    # list servers
    elif msg.startswith("$list_server"):
        embed = discord.Embed(title = "Servers", description = wrap_message(dbread()), color = get_color("blue"))
        await message.channel.send(embed = embed)

    # update server 
    elif msg.startswith("$update_server"):
        author = message.author
        split = msg.split()
        name = split[1]
        success, output = dbget(split[1])
        if success:
            # proper formatting
            args = update_parser.parse_args(split[2:])
            server_info = ""
            print(type(args))
            for arg in vars(args):
                print(arg , getattr(args, arg))
                if getattr(arg, args) != None:
                    server_info += str(arg) + ": " + str(getattr(args, arg)) + "\n"
            embed = discord.Embed(title = f"Update Server, {name}?", description = server_info + "\nY/N?", color = get_color("blue"))
            await message.channel.send(embed = embed)
            #dbupdate(name, args)
        else:
            # improper formatting
            embed = discord.Embed(title = name, description = output, color = get_color("red"))
            await message.channel.send(embed = embed) 

                
        """
        success, output = dbget(name)
        if success:     
            if (chkown(name, author)): 
                print("Updating")
            else:
                embed = discord.Embed(title = name, description = wrap_message("Failed to update server info (you most own the server to update it"), 
                color = get_color("red"))
                await message.channel.send(embed = embed)       
        else:
            embed = discord.Embed(title = name, description = output, color = get_color("red"))
            await message.channel.send(embed = embed)          

    
    elif message.content.startswith('$greet'):
        channel = message.channel
        await channel.send('Say hello!')

        def check(m):
            return m.content == 'hello' and m.channel == channel

        msg = await client.wait_for('message', check=check)
        await channel.send('Hello {.author}!'.format(msg))
        """

client.run(config('TOKEN'))