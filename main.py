import speech_recognition as sr
import pyttsx3
from datetime import datetime
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics.texture import Texture

# WeatherAPI key
API_KEY = "f5e8240959ba4484bac123118240312"

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
tts = pyttsx3.init()

class AudioAssistant(BoxLayout):

    def listen(self, instance):
        with sr.Microphone() as source:
            self.update_text("Listening...")
            try:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                command = recognizer.recognize_google(audio)
                self.update_text(f"You said: {command}")
                self.process_command(command.lower())
            except sr.WaitTimeoutError:
                self.update_text("No input detected, please try again.")
            except sr.UnknownValueError:
                self.update_text("Sorry, I didn't catch that.")
            except sr.RequestError as e:
                self.update_text(f"Could not request results; {e}")

    def process_command(self, command):
        if "hello" in command:
            self.respond("Hello! How can I help you?")
        elif "time" in command:
            now = datetime.now().strftime("%H:%M")
            self.respond(f"The time is {now}.")
        elif "weather in " in command:
            city, date = self.extract_city_and_date(command)
            if city:
                self.get_weather(city, date)
            else:
                self.respond("Please specify the city for the weather.")
        elif "goodbye" in command:
            self.respond("Goodbye! Have a great day!")
            App.get_running_app().stop()  # Stops app safely
        else:
            self.respond("I'm sorry, I didn't understand that.")

    def respond(self, text):
        self.update_text(f"Assistant: {text}")
        tts.say(text)
        tts.runAndWait()

    def update_text(self, text):
        self.text_box.text += text + "\n"

    def extract_city_and_date(self, command):
        city = None
        date = "today"
        if "tomorrow" in command:
            date = "tomorrow"
        elif "today" in command:
            date = "today"
        if "weather in" in command:
            city_start = command.find("weather in") + len("weather in")
            city = command[city_start:].strip()
        return city, date

    def get_weather(self, city, date):
        url = "http://api.weatherapi.com/v1/current.json" if date == "today" else "http://api.weatherapi.com/v1/forecast.json"
        params = {"key": API_KEY, "q": city, "days": 2 if date == "tomorrow" else 1}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if date == "today":
                condition = data["current"]["condition"]["text"]
                temp_c = data["current"]["temp_c"]
                self.respond(f"The current weather in {city} is {condition} with {temp_c}°C.")
            else:
                forecast = data["forecast"]["forecastday"][1]["day"]
                condition = forecast["condition"]["text"]
                max_temp = forecast["maxtemp_c"]
                min_temp = forecast["mintemp_c"]
                self.respond(f"Tomorrow in {city}: {condition}, {min_temp}-{max_temp}°C.")
        except requests.exceptions.RequestException as e:
            self.respond(f"Error fetching weather: {e}")

class AssistantApp(App):
    def build(self):
        return AudioAssistant()

if __name__ == "__main__":
    AssistantApp().run()
