# TODO: docstring del main

# -*- coding: utf8 -*-

# noinspection PyPackageRequirements
import discord
# noinspection PyPackageRequirements
from configs.dbConnector import DbConnector
from configs.settings import Settings

Settings.VERSION = "1.0.0.0"
Settings.startup(test=True)
DbConnector.startup()
DbConnector.create_connection()
client = discord.Client()


async def check_admin_role_in_guild(guild):
    for role in guild.roles:
        if role.name.lower() == Settings.admin_role.lower():
            return
            pass
        pass
    await guild.create_role(name=Settings.admin_role)
    return


async def check_admin_role():
    for guild in Settings.guilds:
        await check_admin_role_in_guild(guild)
    return


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    Settings.guilds = client.guilds
    await check_admin_role()
    print('------')
    return


@client.event
async def on_guild_join(guild):
    await check_admin_role_in_guild(guild)
    return


def fetch_command(content, args):
    lst = content.split(" ")
    command = lst.pop([0]).strip(Settings.command_prefix)
    if len(lst) <= 1:
        return command
    for arg in lst:
        args.append(arg)
        pass
    return command


async def announce_leaderboard():
    # TODO:
    return


async def promotion(player_to_promote):
    # TODO:
    return


async def downgrade(player_to_downgrade):
    # TODO:
    return


async def run_command(message):
    args = []
    command = fetch_command(message.content, args)

    if command == "leaderboard" or command == "leader":
        await announce_leaderboard()
        return

    if command == "promo" and len(args) == 1:
        await promotion(args[0])
        return

    if command == "down" and len(args) == 1:
        await downgrade(args[0])
        return

    return


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(Settings.command_prefix):
        await run_command(message)
    return


client.run(Settings.token)
