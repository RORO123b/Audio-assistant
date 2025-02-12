import speech_recognition as sr
import pyttsx3
from datetime import datetime
import requests
from kivy.app import App
from kivy.uix.widget import Widget


class AudioAssistant(Widget):
    pass

class AudioAssistant(App):
    def buil(self):
        return AudioAssistant()

# WeatherAPI key
API_KEY = "f5e8240959ba4484bac123118240312"

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
tts = pyttsx3.init()

def get_weather(city, date, api_key):
    """Fetches the weather using WeatherAPI."""
    if date == "today":
        url = "http://api.weatherapi.com/v1/current.json"
    elif date == "tomorrow":
        url = "http://api.weatherapi.com/v1/forecast.json"

    params = {
        "key": api_key,
        "q": city,  # City name or "latitude,longitude"
        "days": 2 if date == "tomorrow" else 1  # Forecast for today/tomorrow
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()

        if date == "today":
            # Extract current weather information
            location = data["location"]["name"]
            condition = data["current"]["condition"]["text"]
            temp_c = data["current"]["temp_c"]
            respond(f"The current weather in {location} is {condition} with a temperature of {temp_c}°C.")
        elif date == "tomorrow":
            # Extract tomorrow's forecast
            location = data["location"]["name"]
            forecast = data["forecast"]["forecastday"][1]["day"]
            condition = forecast["condition"]["text"]
            max_temp = forecast["maxtemp_c"]
            min_temp = forecast["mintemp_c"]
            respond(f"The forecast for tomorrow in {location} is {condition} with temperatures between {min_temp}°C and {max_temp}°C.")

    except requests.exceptions.HTTPError as e:
        respond(f"HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        respond(f"Error fetching data: {e}")

def listen():
    """Capture audio input and convert it to text."""
    with sr.Microphone() as source:
        print("Listening... You can say 'goodbye' to exit.")
        try:
            recognizer.adjust_for_ambient_noise(source)  # Adapt to background noise
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)  # Add time limits
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except sr.WaitTimeoutError:
            print("No input detected, please try again.")
            return None
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

def respond(text):
    """Speak and print the assistant's response."""
    print(f"Assistant: {text}")
    tts.say(text)
    tts.runAndWait()

def extract_city_and_date(command):
    """Extracts city and date (today/tomorrow) from the command."""
    city = None
    date = "today"

    # Check for date keywords
    if "tomorrow" in command:
        date = "tomorrow"
    elif "today" in command:
        date = "today"

    # Extract city by searching after "weather in"
    if "weather in" in command:
        city_start = command.find("weather in") + len("weather in")
        city = command[city_start:].strip()

    return city, date

def main():
    """Main loop for the assistant."""
    while True:
        command = listen()
        if command:
            command_lower = command.lower()
            if "hello" in command_lower:
                respond("Hello! How can I help you?")
            elif "time" in command_lower:
                now = datetime.now().strftime("%H:%M")
                respond(f"The time is {now}.")
            elif "weather in " in command_lower:
                city, date = extract_city_and_date(command_lower)
                if city:
                    get_weather(city, date, API_KEY)
                else:
                    respond("Please specify the city for the weather.")
            elif "goodbye" in command_lower:
                respond("Goodbye! Have a great day!")
                break
            else:
                respond("I'm sorry, I didn't understand that.")
        else:
            print("Waiting for a valid command...")

if __name__ == "__main__":
    main()
    AudioAssistant().run()
