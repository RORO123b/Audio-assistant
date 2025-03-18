# Audio Assistant

This project is a Python-based Audio Assistant that leverages speech recognition, text-to-speech, and natural language processing to interact with users. It integrates with a weather API to provide real-time weather updates and uses a pre-trained DialoGPT model to handle conversational commands.

## Features

- **Speech Recognition:** Listens to user commands using the `speech_recognition` library.
- **Text-to-Speech (TTS):** Converts responses to speech with `pyttsx3`.
- **Chatbot Integration:** Generates conversational responses using the `microsoft/DialoGPT-medium` model via the `transformers` library.
- **Weather Updates:** Fetches current weather or forecast data using WeatherAPI.
- **Kivy UI:** Provides a simple graphical interface built with Kivy for a better user experience.

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/RORO123b/Audio-assistant.git
cd Audio-assistant
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the Weather API Key
Obtain an API key from [WeatherAPI.com](https://www.weatherapi.com/) and set it as an environment variable:

- **On Unix-based systems:**
  ```bash
  export API_KEY=your_weather_api_key
  ```
- **On Windows (CMD):**
  ```cmd
  set API_KEY=your_weather_api_key
  ```

## Usage

1. **Run the Application:**
   ```bash
   python3 main.py
   ```

2. **Interacting with the Assistant:**
   - Click the **Listen** button to start voice recognition.
   - Speak commands such as:
     - **"Hello"** – The assistant will greet you.
     - **"Time"** – It will tell you the current time.
     - **"Weather in [city]"** – Retrieves the current weather. To get the forecast for tomorrow, include "tomorrow" in your command.
     - **"Goodbye"** – The assistant will say goodbye and close the application.
     - For other commands, the chatbot generates a response using **DialoGPT**.

## Project Structure

```
├── main.py          # Main application logic
├── assistant.kv     # Kivy language file for UI layout
└── README.md        # Project documentation
```

## Dependencies

- **[speech_recognition](https://pypi.org/project/SpeechRecognition/):** For capturing and recognizing speech.
- **[pyttsx3](https://pypi.org/project/pyttsx3/):** For converting text to speech.
- **[kivy](https://kivy.org/):** For building the graphical user interface.
- **[requests](https://pypi.org/project/requests/):** For making HTTP requests to the weather API.
- **[transformers](https://huggingface.co/transformers/):** For integrating the DialoGPT model.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is open-source and available for personal and educational use.

## Acknowledgments

- The [DialoGPT](https://github.com/microsoft/DialoGPT) model by Microsoft.
- Weather data provided by [WeatherAPI](https://www.weatherapi.com/).
