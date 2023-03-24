import asyncio
import discord
from typing import Callable
import inspect
from dataclasses import dataclass

active_timers = []

DELTA_TIME = 1

class Action_Timer:
    """
    Coroutine system that calls arbitrary functions every second, and when the timer runs out.
    
    on_timeout is called after the timer runs out of time.
    on_tick is called, by default, every second.
    on_tick must take an integer: the current time.
    
    For this module to work, you must call iterate_timers() to start the ticking coroutine.
    """

    def __init__(self, length:int = 60, on_timeout:Callable=lambda:None, on_tick:Callable=lambda time:None):
        self.length = length
        self.current_time = length
        self.on_timeout = on_timeout
        self.on_tick = on_tick
        self.paused = False
        # Add timer to the iteration list
        active_timers.append(self)
    
    async def basetick(self):
        """
        The actions that every timer shoud preform every tick.
        
        This controls calling on_tick, on_timeout, 
        incrementing time, and canceling the timer.
        """
        if self.paused:
            return
        self.current_time -= DELTA_TIME
        await self.async_maybe(self.on_tick, self.current_time)
        
        if self.current_time <= 0:
            await self.async_maybe(self.on_timeout)
            self.cancel()

    async def async_maybe(self, func, args = None):
        """
        Call a function, regardless if it is a regular function or a coroutine.
        """
        if not callable(func):
            raise ValueError("func is not callable")
        #First we call the function.
        if args is not None:
            rv = func(args)
        else:
            rv = func()
        #if it's a coroutine, it returns a coroutine object, ready for us to await.
        if inspect.isawaitable(rv):
            rv = await rv
        return rv

    def cancel(self):
        active_timers.remove(self)

class Response_Timer(Action_Timer):
    """
    Action Timer that listens for a post in a channel.
    
    When a message is sent to a specific channel, 
    pass it to an arbitrary function.
    
    As of right now, this class only works if that arbitrary function
    takes exactly one argument: the message.
    
    For this class to work, you must call listen_timers(message) after every message.
    """
    def __init__(self, message, length:int = 60, on_timeout:Callable=lambda:None, on_tick:Callable=lambda:None, on_response:Callable=lambda:None):
        super().__init__(length, on_timeout, on_tick)
        
        self.m_id = message.id # Message from whence the timer originated
        self.c_id = message.channel.id
        self.on_response = on_response


@dataclass
class RT_Response():
    """
    This represents what to do after a timer hears a response.
    """
    cancel : bool = False
    delete : bool = False
    # Potentially, this class can be used to give responses more control.
    # not_int : bool = False
    # not_float : bool = False 
    # wrong_user : bool = False
    

async def iterate_timers():
    """
    Start a coroutine that increments each timer's clock.
    """
    while(DELTA_TIME):
        await asyncio.sleep(DELTA_TIME) # Sleep in seconds.
        for timer in active_timers:
            try:
                await timer.basetick()
            except exception:
                print(f"error ticking {timer}")
            
async def listen_timers(message):
    """
    If a response timer recieves a message, 
    call its on_response() func and pass it the message
    """
    for timer in active_timers:
        if not isinstance(timer, Response_Timer):
            continue # Only RTs listen for responses.
        if timer.paused:
            continue
        if message.content == "":
            continue
        if message.author.bot:
            continue
        if message.channel.id == timer.c_id:
            rtr = await timer.async_maybe(timer.on_response, message)
            if not rtr:
                rtr = rt_response()
            if rtr.cancel:
                timer.cancel()
            if rtr.delete:
                await message.delete()

