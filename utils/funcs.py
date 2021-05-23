from .vars import PREFIXES, DEFAULT_PREFIX

def prefix(ctx):
    try:
        return PREFIXES.find_one({"serverid": ctx.guild.id}).get("prefix")
    except AttributeError:
        return DEFAULT_PREFIX