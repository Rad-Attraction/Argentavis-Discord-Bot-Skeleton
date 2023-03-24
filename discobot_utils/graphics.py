import math

MOONS = ["🌕","🌖","🌗","🌘","🌑","🌒","🌓","🌔"]

BLUE_MOONS = [
"<:b4:991146926378602527>",
"<:b5:991146927255203891>",
"<:b6:991146928207314994>",
"<:b7:991146929083908157>",
"<:b0:991146922263969853>",
"<:b1:991146923325145169>",
"<:b2:991146924285628436>",
"<:b3:991146925250330664>"
]

RED_MOONS = [
"<:r4:991146934372933662>",
"<:r5:991146935396352100>",
"<:r6:991146936432345148>",
"<:r7:991146937594155088>",
"<:r0:991146930325438506>",
"<:r1:991146931516620890>",
"<:r2:991146932397412352>",
"<:r3:991146933311778876>"
]

def moon_bar(maximum, current, bar_length = 8, direction : str = "left", segments = MOONS):
    """
    Automatically draw a progress bar using moon emojis.
    
    Maximum/Current: The size of the bar and its progress
    
    bar_length: how many emojis wide to make the bar.
    note: for custom emojis, discord interprets it as 
    the length of the emoji's code. 
    the max might have to be reduced to 6.
    
    Direction: where the top of the bar goes.
    Imagine the bar fills this direction.
    
    Segments: the list of emojis that go in the bar.
    By default, it will be regular moons.
    alternatively, pass the string "RED" or "BLUE" for red and blue moons.
    alternatively, pass a list of emojis as their string code.
    please load them in this order:
    ["🌕","🌖","🌗","🌘","🌑","🌒","🌓","🌔"]
    """
    
    # Guard clauses that print a message and set the value to default
    current = min(maximum, current)
    if bar_length < 0:
        print("moon bars cant be negative dude...")
        bar_length = 8
    if bar_length == 0:
        print("moon bar length of zero? okay")
        return ""
    bar_length = round(bar_length)
    direction = direction.lower()
    if not direction in ["left","right"]:
        print("ay yo you gotta say left or right to me so i know which way to make a da moon bars")
        direction = "left"
    #parse segments.
    if segments == "BLUE":
        segments = BLUE_MOONS
    if segments == "RED":
        segments = RED_MOONS
    if len(segments) != 8:
        print("the moon bars segments thing has gotta be 8 emojis long")
        segments = MOONS
    
    # Sort emojis to be in the right order.
    # Default order : [0,1,2,3,4,5,6,7]
    lvars = [4,3,2,1,0]
    rvars = [4,5,6,7,0]
    my_variants = []
    if direction == "left":
        my_variants = segments[4::-1]
    else:
        my_variants = segments[4::]
        my_variants.append(segments[0])
    
    #figures out the size of the segments, and the number of full ones
    seg_size = maximum/bar_length
    segs_full = math.floor(current/seg_size)
    segs_any = math.ceil(current/seg_size)
    
    #reverse each variant, to compensate for later reversing
    #only matters if a variant is more than one char
    if direction != "left":#this flips the right side
        my_variants = [variant[::-1] for variant in my_variants]
    
    #puts in a full moon, a partial moon (which can be full or new), or a new moon
    bar = ""
    for seg in range(bar_length):
        if seg < segs_full:
            bar += my_variants[-1]
        elif seg < segs_any:
            this_seg = current - (seg * seg_size) #crops my view to this seg
            this_seg /= seg_size #scales the segment to be between 0 and 1
            this_seg = round(this_seg*4) #scales that to an int between 0 and 4
            bar += my_variants[this_seg] #thats the moon i want
        else:
            bar += my_variants[0]
    if direction != "left":#flip right-facing bars.
        bar = bar[::-1]
    return bar

if __name__ == "__main__":
    for i in range(40):
        #dir = "left" if i%2 else "right"
        if i == 13:
            print(moon_bar(40, i, direction = dir, segments = BLUE_MOONS))
            continue
        print(moon_bar(40,i, direction = dir, segments = RED_MOONS))
    
