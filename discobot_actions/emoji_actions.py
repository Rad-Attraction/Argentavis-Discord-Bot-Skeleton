import discord
from typing import Callable
from typing import Tuple
from typing import Any
import inspect
from dataclasses import dataclass, field


active_actions = {}

class emoji_action:
    """
    An emoji button that appears on a post, and does a specific action when it is pressed.
    This stores the two function callables and an arguments tuple.
    
    Can also capture an emoji and pass it to the action, 
    if you set the emoji string to "*".
    
    Each emoji action (EA) is stored in a dict in memory, local to this module.
    the keys to this dict are discord message ids.
    
    When an EA is clicked, it will return a response object.
    After this response is recieved, the module will manage the active actions dict.
    """
    def __init__(self, emoji:str, name:str, action:Callable, args:Tuple[Any,...]=(), pass_user:bool=False):
        self.emoji = emoji
        self.name = name
        self.action = action
        self.args = args
        self.pass_user = pass_user
        self.user = None
    
    async def execute_action(self):
        #concatenate tuples
        my_args = self.args
        if self.pass_user:
            my_args = (my_args,) + (self.user,)
        #perform action
        return await self.async_maybe(self.action, my_args)

    def __str__(self):
        return self.emoji + "-" + self.name

    async def async_maybe(self, func, args=None):
        """
        Call a function, regardless if it is a regular function or a coroutine, regardless if it takes arguments or not.
        """
        #print(func, args)
        if callable(func):
            #Call the function.
            #pass it args if we have any.
            #if it's a coroutine, it returns a "coroutine object", 
            #ready for us to await with the await keyword.
            if args is not ():
                rv = func(args)
            else:
                rv = func()
            if inspect.isawaitable(rv):
                rv = await rv
            return rv
        else:
            raise ValueError(f"\nError in action \"{self}\"\n\nfunc \"{func}\" is not callable\n")

async def action_button_list(message, a_list:list):
    """
    Add buttons for a list of reactions to a post.
    Pass it a discord message and a list of action objects.
    """
    for a in a_list:
        await message.add_reaction(a.emoji)
    active_actions[str(message.id)] = a_list

async def action_listen_list(reaction, user):
    """
    Listen if the reacted emoji is in the active actions hash map.
    """
    message = reaction.message
    emoji = reaction.emoji
    if str(message.id) in active_actions:
        for a in active_actions[str(message.id)]:
            if a.emoji not in [str(emoji), "*"]:
                continue
            if str(emoji) == a.emoji:
                print ("Matched emoji " + str(emoji))
            # Can set an emoji as * to capture the next emoji.
            # Appends it to the args.
            elif a.emoji == "*": 
                print ("Captured emoji " + str(emoji))
                a.args = (str(emoji))
            #if a action requires the user, try this.
            if a.pass_user:
                a.user = user
            
            response = await a.execute_action()
            if not response:
                response = ea_response()
            
            if response.complete_action:
                active_actions[str(message.id)].remove(a)
                
            if response.remove_reaction:
                await reaction.remove(user)
                
            if response.clear_reactions:
                await reaction.message.clear_reactions()
                
            if response.remove_dis_post:
                del active_actions[str(message.id)]
                
            if response.delete_dat_post:
                await message.delete()
    # When a post has no more reactions remove it from the database
    # Check the condition again, in case it's been deleted
    if str(message.id) in active_actions:
        if len(active_actions[str(message.id)]) == 0:
            del active_actions[str(message.id)]

def help_list(a_list:list):
    """
    Easy way to print a block of text that shows each emoji.
    """
    helps = map(str, a) # Calls str() on each action.
    return "\n".join(helps)

@dataclass
class ea_response():
    """
    A response emitted by an emoji action.
    by default, remove the emoji from the post,
    and remove this action from the active actions.
    
    set complete_action to false to make the action reusable.
    
    Can also clear all reactions from a post,
    and remove it from the active actions.
    """
    remove_reaction : bool = True
    complete_action : bool = True
    clear_reactions : bool = False
    remove_dis_post : bool = False
    delete_dat_post : bool = False
    