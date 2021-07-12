import sys
import time
import pyttsx3
import speech_recognition as sr

from common.weather import say_weather
from common.jokes import say_joke
from common.websites import open_website
from better_profanity import profanity

converter = pyttsx3.init()
VOICE_IDS = {
    "default_male": "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0",
    "default_female": "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0",
}
WHITELIST_WORDS = []


def main():
    setup()
    r = sr.Recognizer()
    try:
        while True:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)

                say("Hello! How can I help you today?")
                audio = r.listen(source)

                try:
                    phrase = r.recognize_google(audio)
                    parse_phrase(phrase.lower())
                    time.sleep(1)
                except Exception as e:
                    print(f"Error : {e}")
                    say("There was an error recognizing what you said")
    except KeyboardInterrupt:
        say("Terminating")
        sys.exit()


def parse_phrase(phrase):
    tokens = phrase.split(" ")
    print(tokens)
    if profanity.contains_profanity(phrase):
        say("That is not a phrase I can understand")
    if phrase == "hello":
        say("Why, hello there?")
    elif "joke" in phrase:
        say_joke(say)
    elif "terminate" in phrase or "exit" in phrase:
        shutdown()
    elif "weather" in phrase:
        say_weather(say)
    elif "open" == tokens[0] and len(tokens) > 1:
        open_website(tokens[1:], say)
    elif phrase == "":
        pass
    else:
        say("I do not recognize the command")


def say(phrase, speed=190, volume=0.7):
    print(phrase)
    converter.setProperty("rate", speed)
    converter.setProperty("volume", volume)
    converter.say(str(phrase))
    converter.runAndWait()


def get_voices():
    voices = converter.getProperty("voices")
    for voice in voices:
        print("Voice:")
        print("ID: %s" % voice.id)
        print("Name: %s" % voice.name)
        print("Age: %s" % voice.age)
        print("Gender: %s" % voice.gender)
        print("Languages Known: %s" % voice.languages)
        print("Voice : ", voice)


def setup():
    profanity.load_censor_words(WHITELIST_WORDS)
    converter.setProperty("voice", VOICE_IDS["default_female"])
    converter.setProperty("rate", 190)
    converter.setProperty("volume", 0.7)
    say("Initializing...")


def shutdown():
    say("Terminating...")
    sys.exit()


if __name__ == "__main__":
    main()
    # get_voices()
