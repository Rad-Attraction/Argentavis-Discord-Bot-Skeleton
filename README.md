
# Argentavis Discord Bot Skeleton

This is a skeleton that i made while building discord bots in discord.py.  

It simplifies a couple useful bot abilities into modules that you can use by instantiating them.


### Action Timers

The action timer system is a coroutine that performs arbitrary functions every second, or when a timer runs out.

###### Response Timers

A subclass of action timers that listens in a channel for a user's response. Can be used to make a fluent chatbot-style interaction.

### Emoji Actions

When a user reacts to a discord post, it makes a little button with that emoji, to allow other users to react too.  
This module lets a bot use reactions to create simple buttons, labelled with emojis. When a user clicks on the button, then the bot runs an arbitrary action, and handles the action's completion.

This is made a little redundant by the actual buttons introduced by discord's api, but you can have way more than 9 reactions on one post.