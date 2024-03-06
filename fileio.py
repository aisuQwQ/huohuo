def import_guild_list():
    guild_list={}
    with open('guild_list.txt') as f:
        lines=[s.rstrip() for s in f.readlines()]
        for line in lines:
            guild_id,channel_id=line.split(' ')
            guild_list[int(guild_id)]=int(channel_id)
    return guild_list

def export_guild_list(guild_list):
    with open('guild_list.txt', mode='w') as f:
        for key, value in guild_list.items():
            f.write(f'{key} {value}\n')
    return