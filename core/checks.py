from discord.ext import commands


def event_starter():
    def predicate(ctx):
        return ctx.message.author.id in ctx.bot.event_starters
    return commands.check(predicate)
