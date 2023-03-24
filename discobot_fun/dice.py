import random

async def roll(message):
    #the args are seperated by a d
    command = message.content.lower().split()[1]
    args = command.split("d")
    dcount = int(args[0])
    dsize = int(args[1])
    rolls = []
    total = 0
    for i in range(dcount):
        roll = random.randint(1, dsize)
        rolls.append(roll)
        total += roll
    #result line should be simple if one dice
    result = f"{rolls} {total}" if len(rolls) > 1 else str(total)
    await message.channel.send(f"Rolling {command}:\n{result}")
