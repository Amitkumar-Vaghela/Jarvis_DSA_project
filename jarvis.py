import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import pyautogui
import pyjokes
import json
import pyaudio
import time

class Assistant:
    def __init__(self):
        # Initializing the text-to-speech engine
        self.engine = pyttsx3.init()
        self.set_voice()
        self.set_rate()
        self.set_volume()
        self.name = self.load_name()

    def set_voice(self):
        """Sets the voice for the assistant."""
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # Female voice
        self.engine.runAndWait()

    def set_rate(self):
        """Sets the speaking rate for the assistant."""
        self.engine.setProperty('rate', 150)

    def set_volume(self):
        """Sets the volume of the assistant."""
        self.engine.setProperty('volume', 1)

    def speak(self, audio):
        """Converts text to speech."""
        self.engine.say(audio)
        self.engine.runAndWait()

    def time(self):
        """Tells the current time."""
        current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
        self.speak(f"The current time is {current_time}")
        print(f"The current time is {current_time}")

    def date(self):
        """Tells the current date."""
        now = datetime.datetime.now()
        self.speak(f"The current date is {now.day} {now.strftime('%B')} {now.year}")
        print(f"The current date is {now.day}/{now.month}/{now.year}")

    def wishme(self):
        """Greets the user based on the time of day."""
        self.speak(f"Welcome back, sir! {self.name} at your service. How may I assist you?")
        hour = datetime.datetime.now().hour
        if 4 <= hour < 12:
            self.speak("Good morning!")
        elif 12 <= hour < 16:
            self.speak("Good afternoon!")
        elif 16 <= hour < 24:
            self.speak("Good evening!")
        else:
            self.speak("Good night, see you tomorrow.")

    def screenshot(self):
        """Takes a screenshot and saves it."""
        try:
            img = pyautogui.screenshot()
            img_path = os.path.join(os.path.expanduser("~"), "Pictures", "screenshot.png")
            img.save(img_path)
            self.speak(f"Screenshot saved as {img_path}.")
            print(f"Screenshot saved as {img_path}.")
        except Exception as e:
            self.speak(f"An error occurred while taking the screenshot: {e}")
            print(f"Error: {e}")

    def take_command(self):
        """Listens to user's command and returns it as text."""
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            try:
                audio = r.listen(source, timeout=5)
            except sr.WaitTimeoutError:
                self.speak("Timeout occurred. Please try again.")
                return None

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(query)
            return query.lower()
        except sr.UnknownValueError:
            self.speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            self.speak("Speech recognition service is unavailable.")
            return None
        except Exception as e:
            self.speak(f"An error occurred: {e}")
            print(f"Error: {e}")
            return None

    def play_music(self, song_name=None):
        """Plays music from the user's Music directory."""
        song_dir = os.path.expanduser("~\\Music")
        songs = os.listdir(song_dir)

        if song_name:
            songs = [song for song in songs if song_name.lower() in song.lower()]

        if songs:
            song = random.choice(songs)
            os.startfile(os.path.join(song_dir, song))
            self.speak(f"Playing {song}.")
            print(f"Playing {song}.")
        else:
            self.speak("No song found.")
            print("No song found.")

    def set_name(self):
        """Sets a new name for the assistant."""
        self.speak("What would you like to name me?")
        name = self.take_command()
        if name:
            with open("assistant_name.txt", "w") as file:
                file.write(name)
            self.speak(f"Alright, I will be called {name} from now on.")
        else:
            self.speak("Sorry, I couldn't catch that.")

    def load_name(self):
        """Loads the assistant's name from a file, or uses a default name."""
        try:
            with open("assistant_name.txt", "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return "Jarvis"  # Default name

    def search_wikipedia(self, query):
        """Searches Wikipedia and returns a summary."""
        try:
            self.speak("Searching Wikipedia...")
            result = wikipedia.summary(query, sentences=2)
            self.speak(result)
            print(result)
        except wikipedia.exceptions.DisambiguationError:
            self.speak("Multiple results found. Please be more specific.")
        except Exception:
            self.speak("I couldn't find anything on Wikipedia.")

    def open_youtube_and_search(self, search_query):
        """Opens YouTube and performs a search."""
        self.speak("Opening YouTube and searching...")
        wb.open("https://www.youtube.com")
        time.sleep(5)  # Wait for the page to load
        pyautogui.click(x=400, y=200)  # Adjust as per screen resolution
        pyautogui.typewrite(search_query, interval=0.1)
        pyautogui.press("enter")
        self.speak(f"Searching for {search_query} on YouTube.")
    

    def manage_todo_list(self, action, task=None):
        """Add, view, or delete tasks from a to-do list."""
        file_path = "todo_list.json"

        try:
            with open(file_path, 'r') as file:
                todo_list = json.load(file)
        except FileNotFoundError:
            todo_list = []

        if action == "add":
            todo_list.append(task)
            self.speak(f"Task '{task}' added to your to-do list.")
        elif action == "view":
            if todo_list:
                tasks = '\n'.join(todo_list)
                self.speak(f"Your tasks are: {tasks}")
                print(f"Your tasks are: {tasks}")
            else:
                self.speak("Your to-do list is empty.")
        elif action == "delete":
            if task in todo_list:
                todo_list.remove(task)
                self.speak(f"Task '{task}' removed from your to-do list.")
            else:
                self.speak(f"Task '{task}' not found in your to-do list.")
        else:
            self.speak("Invalid action. Please try again.")

        with open(file_path, 'w') as file:
            json.dump(todo_list, file)

if __name__ == "__main__":
    assistant = Assistant()
    assistant.wishme()

    while True:
        query = assistant.take_command()
        if not query:
            continue

        if "time" in query:
            assistant.time()

        elif "date" in query:
            assistant.date()

        elif "wikipedia" in query:
            query = query.replace("wikipedia", "").strip()
            assistant.search_wikipedia(query)

        elif "play music" in query:
            song_name = query.replace("play music", "").strip()
            assistant.play_music(song_name)

        elif "open youtube" in query:
                wb.open("youtube.com")

        
        if "search" in query and "on youtube" in query:
            search_query = query.replace("search", "").replace("on youtube", "").strip()
            assistant.search_youtube(search_query)

        elif "open google" in query:
            wb.open("google.com")

        elif "change your name" in query:
            assistant.set_name()

        elif "screenshot" in query:
            assistant.screenshot()

        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            assistant.speak(joke)
            print(joke)

        elif "shutdown" in query:
            assistant.speak("Shutting down the system, goodbye!")
            os.system("shutdown /s /f /t 1")
            break

        elif "restart" in query:
            assistant.speak("Restarting the system, please wait!")
            os.system("shutdown /r /f /t 1")
            break

        elif "offline" in query or "exit" in query:
            assistant.speak("Going offline. Have a good day!")
            break

        elif "thank you" in query:
            assistant.speak("You're welcome! Starting a new conversation.")
            break
