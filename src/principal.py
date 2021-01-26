# TODO: docstring del main

# -*- coding: utf8 -*-

# noinspection PyPackageRequirements
import discord
from configs.dbConnector import DbConnector
from configs.settings import Settings

Settings.VERSION = "1.3.0.0"
Settings.startup(test=True)
DbConnector.startup()
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
    command = lst.pop(0)
    command = command[len(Settings.command_prefix):len(command)]
    for arg in lst:
        if arg == "":
            continue
        args.append(arg)
        pass
    return command


async def announce_leaderboard(channel_to_publish):
    tabla = DbConnector.fetch_leaderboard()
    embed = discord.Embed(title="Xatos League", color=0x21c115)
    for entrada in tabla:
        embed.add_field(name=entrada[0], value="->  **" + entrada[1] + "**", inline=False)
        pass

    await channel_to_publish.send(embed=embed)
    return


async def promotion(channel_to_publish, player_to_promote):
    player_to_promote = parse_tag(player_to_promote)
    if player_to_promote is None:
        await channel_to_publish.send("Se ingresó una etiqueta como id de Ranker invalida")
        return
    nueva_liga = DbConnector.promote_user(player_to_promote)
    if nueva_liga is not None:
        await channel_to_publish.send("<@" + player_to_promote + "> ha subido a " + nueva_liga)
    return


async def downgrade(channel_to_publish, player_to_downgrade):
    player_to_downgrade = parse_tag(player_to_downgrade)
    if player_to_downgrade is None:
        await channel_to_publish.send("Se ingresó una etiqueta como id de Ranker invalida")
        return
    nueva_liga = DbConnector.downgrade_user(player_to_downgrade)
    if nueva_liga is not None:
        await channel_to_publish.send("<@" + player_to_downgrade + "> ha bajado a " + nueva_liga)
    return


def registered_players():
    return DbConnector.fetch_players()
    pass


def parse_league(league_raw):
    if league_raw.lower() == Settings.ligas[len(Settings.ligas) - 1].lower():
        return Settings.ligas[len(Settings.ligas) - 1]
        pass

    raw_length = len(league_raw)
    if raw_length < 4 or raw_length > 9:
        return None
        pass

    league = league_raw[0:raw_length - 1]
    try:
        division = int(league_raw[raw_length - 1:raw_length])
        pass
    except ValueError:
        return None
        pass
    if division < 1 or division > 5:
        return None
        pass

    for liga in Settings.ligas:
        if league.lower() == liga.lower():
            return liga + " " + str(division)
            pass
        pass
    return None


def parse_tag(tag_player):
    if tag_player[0] != '<':
        return None
    if tag_player[1] != '@':
        return None
    if tag_player[2] != '!':
        return None
    if tag_player[len(tag_player) - 1] != '>':
        return None
    return tag_player[3:len(tag_player) - 1]


async def register(channel_to_publish, id_player_to_add, nick_player_to_add, league_to_add):
    id_player_to_add = parse_tag(id_player_to_add)
    if id_player_to_add is None:
        await channel_to_publish.send("Se ingresó una etiqueta como id de Ranker invalida")
        return

    if is_registered(id_player_to_add):
        await channel_to_publish.send("Ranker ya registrado")
        return

    league_to_add = parse_league(league_to_add)
    if league_to_add is None:
        await channel_to_publish.send("La combinación liga/división ingresada no coincide con las disponibles")
        return

    DbConnector.register(id_player_to_add, nick_player_to_add, league_to_add)
    await channel_to_publish.send(
        "Registrado <@" + id_player_to_add + "> como " + nick_player_to_add + " en la liga " + league_to_add)
    return


def has_perm(member):
    for role in member.roles:
        if role.name.lower() == Settings.admin_role.lower():
            return True
    return False


async def change_alias(channel_to_publish, user_id, new_nick):
    DbConnector.change_alias(user_id, new_nick)
    await channel_to_publish.send("<@" + str(user_id) + "> renombrado a " + new_nick)
    return


def is_registered(user_id):
    players = registered_players()
    for player in players:
        if int(user_id) == player[0]:
            return True
    return False


async def run_command(message):
    args = []
    command = fetch_command(message.content, args)
    arg_count = len(args)

    if command == "leaderboard" or command == "leader":
        await announce_leaderboard(message.channel)
        return

    if is_registered(message.author.id):
        if command == "alias":
            if arg_count == 1:
                await change_alias(message.channel, message.author.id, args[0])
                return
            if arg_count == 0:
                await change_alias(message.channel, message.author.id, message.author.display_name)
                return
            await message.channel.send("No tienes permisos para eso")
            return

    if not has_perm(message.author):
        await message.channel.send("No tienes permisos para eso")
        return

    if command == "add" and arg_count == 5 and args[1] == "as" and args[3] == "in":
        await register(message.channel, args[0], args[2], args[4])
        return

    if command == "promo" and arg_count == 1:
        await promotion(message.channel, args[0])
        return

    if command == "down" and arg_count == 1:
        await downgrade(message.channel, args[0])
        return

    return


@client.event
async def on_message(message):
    if message.channel.id != Settings.channel_id:
        return
    if message.author == client.user:
        return

    if message.content.startswith(Settings.command_prefix):
        await run_command(message)
    return


client.run(Settings.token)
