import discord
import asyncio
from discord.ext import commands
import utils.vars as var

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member:discord.User=None, *, reason="No reason given :("):
        if member == ctx.author:
            await ctx.send("You can't ban yourself :eyes:")
        await ctx.guild.ban(member, reason=reason)
        await member.send(embed=discord.Embed(title=f"You have been banned from {ctx.guild.name}",
                                             description="Sorry I'm just a bot and I follow orders :(", color=var.RED).add_field(name="Reason", value=reason).add_field(name="Banned by", value=ctx.author))
        await ctx.send(f"`{member}` got banned :O")


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member:discord.User=None):
        if member == ctx.author:
            await ctx.send("You are not even banned why you trying to unban yourself :joy:")
        await ctx.guild.unban(member)
        await member.send(embed=discord.Embed(title=f"You have been unbanned from {ctx.guild.name}!",
                                            description="Yay I would be happy to see you back!", color=var.GREEN).add_field(name="Unbanned by", value=ctx.author))
        await ctx.send(f'`{member}` is now unbanned!')
    

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member:discord.Member=None):
        if not discord.utils.get(ctx.guild.roles, name='Muted'):
            await ctx.send(embed=discord.Embed(title="Creating a Muted role...", 
                                            description="Since there is no role named 'Mute' and this is the first time the command is used, I am creating a muted role!")
                                            .set_footer("This is only a one time process, next mute won't create any new role and use the already existing one."))

            perms = discord.Permissions(send_messages=False)
            mutedrole = await ctx.guild.create_role(name="Muted", colour=discord.Colour(0xa8a8a8), permissions=perms)
        mutedrole = discord.utils.get(ctx.guild.roles, name='Muted')
        await mutedrole.edit(position=1)
        await member.add_roles(mutedrole)
        await ctx.send(f"`{member}` have been muted!")


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member:discord.Member=None):
        if not discord.utils.get(ctx.guild.roles, name='Muted'): 
            await ctx.send("There is no muted role yet, Muting someone automatically makes one.")
        mutedrole = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.remove_roles(mutedrole)
        await ctx.send(f"`{member}` have been unmuted")

    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member:discord.Member=None, *, reason="No reason provided"):
        await member.kick(reason=reason)
        await member.send(embed=discord.Embed(title=f"You have been kicked from {ctx.guild.name}",
                                            color=var.RED).add_field(name="Reason", value=reason).add_field(name="Kicked by", value=ctx.author))

        await ctx.send(f"`{member}` have been kicked from the server")


    @commands.command(aliases=["clean", "deletemsgs"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        info = await ctx.send(f"Deleted {limit} messages (Including the command).")
        await asyncio.sleep(3)
        await info.delete()
            

def setup(bot):
    bot.add_cog(Moderation(bot))