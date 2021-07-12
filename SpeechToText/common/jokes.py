import requests
import json
import time

JOKES_URL = r"https://official-joke-api.appspot.com/random_ten"


def get_random_joke():

    data = requests.get(JOKES_URL)
    joke = json.loads(data.text)
    return joke[0]


def say_joke(say):
    say("Alright, let me think of a joke!")
    joke = get_random_joke()
    say(joke["setup"], speed=170)
    time.sleep(0.75)
    say(joke["punchline"], speed=150)
    say("Ha ha ha ha")
