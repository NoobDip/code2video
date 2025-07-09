import speech_recognition as sr
import pyttsx3
import random
from datetime import datetime
import requests


# ----------- PHRASES & SETUP ------------
greeting_inputs = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
greeting_responses = [
    "Hi there! How can I assist you today?",
    "Hello! I'm ready when you are.",
    "Hey! What can I do for you?",
    "Hi! What would you like to do today?"
]


# Initialize speech recognizer and TTS engine
r = sr.Recognizer()
engine = pyttsx3.init()


# ----------- LISTEN FUNCTION ------------
def listen():
    with sr.Microphone() as source:
        print("[System]: Listening...")
        audio_text = r.listen(source)
        print("[System]: Done listening. Processing...")

        try:
            return r.recognize_google(audio_text)
        except sr.UnknownValueError:
            print("Sorry, I did not get that")
            return None
        except sr.RequestError:
            print("API unavailable or unresponsive")
            return None
        except:
            return None


# ----------- SPEAK FUNCTION ------------
def speak(user_input):
    if user_input:
        print(f"[Assistant]: {user_input}")
        engine.say(user_input)
        engine.runAndWait()
    

# ----------- GREETING CHECK ------------
def is_greeting(user_input):
    return any(greet in user_input.lower() for greet in greeting_inputs)


# ----------- TIME & DATE CHECK ------------
def is_time_date(text):
    keywords = ["time", "date", "today", "day", "clock"]
    return any(keyword in text.lower() for keyword in keywords)


def tell_time_and_date():
    current_time = datetime.now().strftime("%I:%M %p")
    current_date = datetime.now().strftime("%A, %B %d")
    return f"The current time is {current_time} and today's date is {current_date}."


# ----------- SEARCH FUNCTION ------------
def is_search_query(text):
    keywords = ["search for", "look up", "find information on", "what is", "who is", "tell me about", "how to", "where is"]
    return any(phrase in text.lower() for phrase in keywords)


def perform_search(query):
    try:
        response = requests.get("https://api.duckduckgo.com/", params={"q": query, "format": "json"})
        data = response.json()
        result = data.get("AbstractText", "")
        return result if result else "I couldn't find a short answer, but you can check online for more details."
    except Exception as e:
        return f"Something went wrong during the search: {str(e)}"
    

# def main():
    # Print "Welcome to voice assistant"
    # If the command is heard, respond to it (+ subtitles for the VA's response)
    # Else, fallback
    # Exit when the coomand is "exit" || "quit" || "goodbye"










# ----------- MAIN ASSISTANT LOOP ------------
def main():
    speak("Welcome to your voice assistant!")
    print("[Assistant] : Welcome to your voice assistant!")

    # Listen for a voice command
    while True:
        user_input = listen()

        if user_input is None:
            speak("Sorry, I didn't catch that.")
            print("[Assistant]: Sorry, I didn't catch that.") 
            continue    # Continue to listen for the next command

        print(f"[User]: {user_input}")
        user_input_lower = user_input.lower()

        if user_input_lower in ["exit", "quit", "goodbye"]:
            speak("Goodbye!")
            print("[Assistant]: Goodbye!")
            break

        elif is_greeting(user_input):
            response = random.choice(greeting_responses)
            speak(response)
            print(f"[Assistant]: {response}")

        elif is_time_date(user_input):
            speak(tell_time_and_date())

        elif is_search_query(user_input):
            result = perform_search(user_input)
            speak(result)    

        else:
            speak("I'm not sure how to help with that yet.")

            

if __name__ == "__main__":
    main()
