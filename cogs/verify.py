import discord
from discord.ext import commands
import utils.vars as var
from utils.funcs import getprefix

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def verification(self, ctx, channel:discord.TextChannel=None):
        guilddoc = var.VERIFY.find_one({"_id":ctx.guild.id})
        if guilddoc is None:
            if channel is not None:
                embed = discord.Embed(
                title="Setup verification",
                description="React to the respective emojis below to choose the verification type",
                color=var.CMAIN
                ).add_field(name="Command verification", value=f"{var.ACCEPT} Simple command", inline=False
                ).add_field(name="Bot verification", value="🤖 Captcha like image", inline=False)
                botmsg = await ctx.send(embed=embed)
                await botmsg.add_reaction(var.ACCEPT)
                await botmsg.add_reaction("🤖")

                def check(reaction, user):
                    return user == ctx.author and reaction.message == botmsg

                reaction, user = await self.bot.wait_for('reaction_add', check=check)
                if str(reaction.emoji) == var.ACCEPT:
                    NVerified = await ctx.guild.create_role(name="Not Verified", colour=discord.Colour(0xa8a8a8))
                    await botmsg.clear_reactions()
                    embed.title="Processing..."
                    embed.description="Setting up everything, just a second"
                    embed.remove_field(1)
                    await botmsg.edit(embed=embed)
                    for i in ctx.guild.text_channels:
                        await i.set_permissions(NVerified, view_channel=False)
                    await channel.set_permissions(NVerified, view_channel=True)

                    await ctx.send(embed=discord.Embed(
                        title="Command verification",
                        description=f"Successfully setted up verification. New members can now only access other channels after they verify in {channel.mention}",
                        color=var.CGREEN
                    ).set_footer(text="A new role 'Not Verified' is created which can only access the verification channel, after users verify their 'Not Verified' role is removed hence they are able access other channels.")
                    )            
                    var.VERIFY.insert_one({"_id":ctx.guild.id, "type": "command", "channel": channel.id, "roleid": NVerified.id})

                if str(reaction.emoji) == "🤖":
                    NVerified = await ctx.guild.create_role(name="Not Verified", colour=discord.Colour(0xa8a8a8))
                    await botmsg.clear_reactions()
                    embed.title="Processing..."
                    embed.description="Setting up everything, just a second"
                    embed.remove_field(0)
                    await botmsg.edit(embed=embed)
                    for i in ctx.guild.text_channels:
                        await i.set_permissions(NVerified, view_channel=False)
                    await channel.set_permissions(NVerified, view_channel=True)

                    await ctx.send(embed=discord.Embed(
                        title="Bot verification",
                        description=f"Successfully setted up verification. New members can now only access other channels after they verify in {channel.mention}",
                        color=var.CGREEN
                    ).set_footer(text="A new role 'Not Verified' is created which can only access the verification channel, after users verify their 'Not Verified' role is removed hence they are able access other channels.")
                    )
                    var.VERIFY.insert_one({"_id":ctx.guild.id, "type": "bot", "channel": channel.id, "roleid": NVerified.id})

            else:
                await ctx.send(f"Looks like you forgot to mention the verification channel, if you don't have one already then create it!\n```{getprefix(ctx)}verification <#channel>```")

        else:
            verifytype = guilddoc.get("type")

            botmsg = await ctx.send(embed=discord.Embed(
                        title="Verification is already enabled",
                        description=f"This server current has **{verifytype}** verification",
                        color=var.CTEAL
            ).add_field(name="Remove verification", value=var.DISABLE)
            )
            await botmsg.add_reaction(var.DISABLE)
            def reactioncheck(reaction, user):
                return user == ctx.author and reaction.message == botmsg

            reaction, user = await self.bot.wait_for('reaction_add', check=reactioncheck, timeout=60.0)
            if str(reaction.emoji) == var.DISABLE:
                await botmsg.clear_reactions()
                var.VERIFY.delete_one({"_id": ctx.guild.id})
                await discord.utils.get(ctx.guild.roles, name="Not Verified").delete()
                await ctx.send("Removed verification from this server (Also removed 'Not Verified' role)")


    @commands.command()
    async def verifytype(self, ctx):
        guilddoc = var.VERIFY.find_one({"_id":ctx.guild.id})
        if guilddoc is not None:
            verifytype = guilddoc.get("type")
            if verifytype == "command":

                embed = discord.Embed(
                title=f"This server has Command verification",
                description="This is a basic type of verification where users enter a command in the verification channel and they are quickly verified and given access to other channels, this can be used to verify people and low-medium level raid/spam bot.",
                color=var.CTEAL
                )

            else:
                embed = discord.Embed(
                title="This server has Bot verification",
                description="This is a much advanced bot captcha like verification most suitable to bypass advance bot raids, after users enter the command a captcha image is sent in the channel with distorted text (enough for a human to read) and if the users enter the code correctly they are verified. The image lasts only for 15 seconds, entering the command again will send another new image.",
                color=var.CTEAL
                )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
            title="This server has no verification",
            description="Verification is setted up to ensure safe raid free server environment, at it's core verification process is very simple, when the verification is setted up a role named 'Not Verified' is created which is given to every new member by me, this role can only access verification channel, once user passes the verification their 'Not Verified' role is taken away hence giving them access to all channels.",
            color=var.CBLUE
            ).add_field(name="Command verification", value="This is a basic easy to use quicker verification method where users can verify by just entering a command"
            ).add_field(name="Bot verification", value="This is a captcha like image verification useful for protection against advanced spam/raid bots. To verify users need to enter the command and type the correct code from the captcha image."
            )
            await ctx.send(embed=embed)
    

    @commands.command()
    async def verifyswitch(self, ctx):
        guilddoc = var.VERIFY.find_one({"_id":ctx.guild.id})
        if guilddoc is not None:
            if guilddoc.get("type") == "command":
                newdata = {"$set":{
                    "type": "bot"
                }}
            else:
                newdata = {"$set":{
                    "type": "command"
                }}
            var.VERIFY.update_one(guilddoc, newdata)
            await ctx.send(embed=discord.Embed(
                        title="Switched to "+newdata.get("$set").get("type")+" verification",
                        description="Use the command again to switch to the other method",
                        color=var.CGREEN)
            )
        else:
            await ctx.send("Can't switch verifcation methods since the server does not have verification enabled.")
    

    @commands.command()
    async def verifyremove(self, ctx):
        guilddoc = var.VERIFY.find_one({"_id":ctx.guild.id})
        if guilddoc is not None:
            var.VERIFY.delete_one(guilddoc)
            await discord.utils.get(ctx.guild.roles, name="Not Verified").delete()
            await ctx.send("Successfully removed verification from this server!")
        else:
            await ctx.send("Verification for this server is not setted up hence cannot remove it either ¯\_(ツ)_/¯ ")


    @commands.Cog.listener()
    async def on_member_join(self, member):
        guilddoc = var.VERIFY.find_one({"_id":member.guild.id})
        if guilddoc is not None:
            role = member.guild.get_role(guilddoc.get("roleid"))
            await member.add_roles(role)


def setup(bot):
    bot.add_cog(Verification(bot))