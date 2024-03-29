import discord
from discord import app_commands

import fileio
import env

TOKEN=env.TOKEN
intents=discord.Intents.all()
client=discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event #起動時
async def on_ready():
    print(f'We have logged in as {client.user}')
    await tree.sync(guild=discord.Object(id=416582664062238730))

@client.event #message受信時
async def on_message(message):
    if message.author.bot:
        return
    print(message.guild.id)
    await message.reply(message.content)

@client.event #voice channel変化時
async def on_voice_state_update(member, before, after):
    if(member.guild.id not in guild_list): #監視対象外
        return
    text_channel=client.get_channel(guild_list[member.guild.id])
    
    if(before.channel==None): #参加時
        n=len(after.channel.members)
        name=f'{member.name}'
        await text_channel.send(f'現在{n}人  {name}さんが参加しました')

        
    if(after.channel==None): #退出時
        n=len(before.channel.members)
        name=f'{member.name}'
        await text_channel.send(f'現在{n}人  {name}さんが退出しました')


@client.event #reaction受信時
async def on_raw_reaction_add(payload):
    message_id=payload.message_id
    if(message_id not in message_list):
        return
    guild_id=payload.guild_id
    guild=client.get_guild(guild_id)
    role=discord.utils.get(guild.roles, name=message_list[message_id])
    if(role is None):
        return
    member=guild.get_member(payload.user_id)
    await member.add_roles(role)



guild_list={} #[guild_id:channel_id]
guild_list=fileio.import_guild_list()

@tree.command(name='set', description='報告チャンネルをここに設定し監視を開始')
@discord.app_commands.guilds(416582664062238730)
async def test(interaction: discord.Interaction):
    guild_list[interaction.guild_id]=interaction.channel_id
    
    await interaction.response.send_message('こんにちは。任務を開始します')

    # await client.get_channel(interaction.channel_id).send('こんにちは')


message_list={} #[message_id:role_name]
@tree.command(name='role', description='ロールを付与')
@discord.app_commands.guilds(416582664062238730)
@discord.app_commands.describe(
    text="投稿文",
    role="付与するロール名"
)
async def test(interaction: discord.Interaction, text:str, role:str):
    await interaction.response.send_message(text)
    message=await interaction.original_response()
    message_list[message.id]=role
    

client.run(TOKEN)
fileio.export_guild_list(guild_list)