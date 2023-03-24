import discord
import discobot_modules.action_timers as at
import discobot_modules.emoji_actions as ea
import discobot_modules.dice as dice
import discobot_modules.egg as egg
from discobot_modules.pretty_disco import pretty_listen
import discobot_modules.text_coloring as tc

print("Modules Imported.")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents)

home_channel = None


@client.event
async def on_ready():
    msg = "Bot skeleton active."
    print(msg)
    if home_channel:
        await client.get_channel(home_channel).send(msg)
    await at.iterate_timers()

@client.event
async def on_reaction_add(reaction, user):
    if True:
        print(reaction.emoji)

    #ignore all reactions from the bot itself
    if (user == client.user):
        return

    await ea.action_listen_list(reaction, user)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
        pass

    msg = message.content
    msgl = msg.lower()
    
    if msgl == "": # Handle image-only messages
        msgl = "."
    
    if msgl.split()[0] == "!hello":
        await message.channel.send("hi :)")
        
    #ping the bot
    if msgl.split()[0] == client.user.mention:
        await message.reply(message.author.mention)

    if msgl.split()[0] == "!roll":
        await dice.roll(message)

    if msgl.split()[0] == "!egg":
        await egg.egg_timer(message)
    
    
    admin_uids = [145031705303056384]
    
    if message.author.id in admin_uids:
        print("__--~~ADMIN SPEAKING~~--__")
        if msgl.split()[0] in ["]", "die", "kill"]:
            await message.channel.send("Killing bot process...")
            quit()
        
    pretty_listen(message)
    await at.listen_timers(message)


def login():
    try:
        #closes the file after the with block
        with open("token", "r+") as keyfile:
            key = keyfile.read()
            client.run(key)
    except OSError:
        print(f"\n\n{tc.R}WARNING: RUNNING BOT FAILED.\n\n{tc.O}There was an error opening the token file. Make sure you have the token file in the right directory. if you don't have one, create a discord bot in the discord developer portal. {tc.W}\n\n")
        raise OSError
    except Exception:
        print(f"\n\n{tc.R}WARNING: RUNNING BOT FAILED.\n\n{tc.O}There was an error connecting to discord for some reason. {tc.W}\n\n")
        raise Exception
        
if __name__ == "__main__":
    # Call login only if this file is being run on its own.
    login()