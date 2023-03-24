import time
import discord
from ..discobot_actions import *
from emoji_actions import Emoji_Action as EA
from action_timers import Action_Timer as AT
from graphics import moon_bar

async def egg_timer(message):
    sex = 32
    if len(message.content.split()) >= 2:
        numero = message.content.split()[1]
        if isdigit(numero):
            sex = int(numero)
    
    egg = await message.channel.send("EGG TIME 2?")
    #define tick and timeout functions
    async def tick(seconds):
        #stupid time module stuff
        timestr = time.strftime("%H:%M:%S", time.gmtime(seconds))
        #then an embed
        em = discord.Embed(
            title="EGG TIME 2",
            description=timestr + "\n" +
            moon_bar(sex, seconds, 8, "left"),
            color=0xddd8b8)
        await egg.edit(embed=em, content="")

    timeout = lambda : message.channel.send(message.author.mention)
    #init the timer
    thistimer = AT(sex, timeout, tick)

    #then add reaction buttons
    async def cancel_egg():
        thistimer.cancel_timer()
        em = discord.Embed(title="EGG CANCELED",
                           description="Egg was stopped by a user :/",
                           color=0xeea898)
        await egg.edit(embed=em, content="")

    def reset_egg():
        thistimer.current_time = thistimer.start_time

    cancel_a = EA("❌", "cancel", cancel_egg)
    reset_a = EA("🔁", "reset", reset_egg)
    await emoji_actions.action_button_list(egg, [cancel_a, reset_a])
