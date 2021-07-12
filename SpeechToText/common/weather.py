import python_weather
import asyncio

def say_weather(say):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_weather())
    say(result)

async def get_weather():
    try:
        # declare the client. format defaults to metric system (celcius, km/h, etc.)
        client = python_weather.Client(format=python_weather.IMPERIAL)

        # fetch a weather forecast from a city
        weather = await client.find("San Antonio")
        temp_celsius = weather.current.temperature
        temp_farenheit = int(conv_cel_to_fer(temp_celsius))
        # returns the current day's forecast temperature (int)
        string = f"The current temperature today is {temp_farenheit} degrees fahrenheit in San Antonio"
        return string
        # get the weather forecast for a few days
        for forecast in weather.forecasts:
            print(str(forecast))
            print(str(forecast.date), forecast.sky_text, forecast.temperature)

        # close the wrapper once done
        await client.close()
        return string
    except SystemExit:
        client.close()


def conv_cel_to_fer(degrees_celsius):
    return (degrees_celsius * 1.8) + 32
