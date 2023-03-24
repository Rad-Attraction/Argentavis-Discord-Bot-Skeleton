import json
import requests
import random


kot = "https://some-random-api.ml/img/cat"
pup = "https://some-random-api.ml/img/dog"
fug = "https://some-random-api.ml/img/fox"
brb = "https://some-random-api.ml/img/birb"

pics = [kot, pup, fug, brb]

def get_pic(): #uses the json off of zenquotes
  try:
    response = requests.get(pics[random.randint(0, 3)])
    json_data = json.loads(response.text)
    url = json_data['link']
  except:
    url = "https://cdn.discordapp.com/attachments/873834474390040589/914382622996701184/caption.gif"
  return url