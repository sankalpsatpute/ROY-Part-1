

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import pywhatkit
import wikipedia
import pyjokes
import requests
import os
import random
import time
from bs4 import BeautifulSoup
from PyDictionary import PyDictionary
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import threading


engine = pyttsx3.init()
engine.setProperty('rate', 175)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
dictionary = PyDictionary()


def speak(text):
    output_box.insert(END, f"Roy 🧠: {text}\n")
    output_box.see(END)
    engine.say(text)
    engine.runAndWait()


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio)
        output_box.insert(END, f"You 👤: {query}\n")
        output_box.see(END)
        return query.lower()
    except:
        speak("Sorry, I didn't catch that.")
        return ""


def get_weather():
    speak("For which city do you want the weather?")
    city = listen().title()
    api_key = "20e644f29bc60653729fbe01dc6f9104"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    res = requests.get(url).json()
    if res.get("main"):
        temp = res["main"]["temp"]
        desc = res["weather"][0]["description"]
        speak(f"The temperature in {city} is {temp}°C with {desc}.")
    else:
        speak("Weather details not available.")

def get_news():
    url = "https://news.google.com/news/rss"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features="xml")
    headlines = soup.findAll('title')[2:7]
    speak("Top 5 news headlines:")
    for headline in headlines:
        speak(headline.text)

def play_music():
    music_folder = "C:\\Music"
    songs = os.listdir(music_folder)
    if songs:
        song = random.choice(songs)
        os.startfile(os.path.join(music_folder, song))
        speak("Playing music.")
    else:
        speak("No music found.")

def open_app(name):
    apps = {
        "notepad": "C:\\Windows\\system32\\notepad.exe",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "vs code": "C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
    }
    app_path = apps.get(name.lower())
    if app_path and os.path.exists(app_path):
        os.startfile(app_path)
        speak(f"Opening {name}")
    else:
        speak(f"{name} not found.")

def get_meaning(word):
    meaning = dictionary.meaning(word)
    if meaning:
        for key in meaning:
            speak(f"{key} meaning: {meaning[key][0]}")
    else:
        speak("No meaning found.")

def take_note():
    speak("What should I write?")
    note = listen()
    with open("notes.txt", "a") as f:
        f.write(f"{datetime.datetime.now()}: {note}\n")
    speak("Note saved.")

def set_alarm():
    speak("Set the alarm time in HH:MM format")
    alarm_time = listen()
    speak(f"Alarm set for {alarm_time}")
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == alarm_time:
            speak("Time to wake up!")
            break
        time.sleep(30)


def roy_ai():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning Sankalp!")
    elif 12 <= hour < 18:
        speak("Good afternoon Sankalp!")
    else:
        speak("Good evening Sankalp!")
    speak("I am Roy, your desktop assistant.")

    while True:
        query = listen()

        if "time" in query:
            speak(datetime.datetime.now().strftime("%I:%M %p"))
        elif "open youtube" in query:
            webbrowser.open("https://www.youtube.com")
        elif "open google" in query:
            webbrowser.open("https://www.google.com")
        elif "play" in query and "on youtube" in query:
            search = query.replace("play", "").replace("on youtube", "").strip()
            pywhatkit.playonyt(search)
            speak(f"Playing {search} on YouTube")
        elif "search information of" in query and "from wikipedia" in query:
            name = query.replace("search information of", "").replace("from wikipedia", "").strip()
            result = wikipedia.summary(name, sentences=2)
            speak(result)
        elif "search" in query:
            speak("What should I search?")
            term = listen()
            webbrowser.open(f"https://www.google.com/search?q={term}")
        elif "weather" in query:
            get_weather()
        elif "news" in query:
            get_news()
        elif "play music" in query:
            play_music()
        elif "open" in query:
            app = query.replace("open", "").strip()
            open_app(app)
        elif "meaning of" in query:
            word = query.replace("meaning of", "").strip()
            get_meaning(word)
        elif "note" in query:
            take_note()
        elif "joke" in query:
            speak(pyjokes.get_joke())
        elif "alarm" in query:
            set_alarm()
        elif "exit" in query or "bye" in query:
            speak("Goodbye Sankalp.")
            break
        else:
            webbrowser.open(f"https://www.google.com/search?q={query}")


root = Tk()
root.title("Roy - AI Desktop Assistant")
root.geometry("600x700")
root.configure(bg="#1e1e2f")


image = Image.open("Roy_Avatar.png")
image = image.resize((150, 150))
photo = ImageTk.PhotoImage(image)
Label(root, image=photo, bg="#1e1e2f").pack(pady=10)


Label(root, text="Roy - AI Desktop Assistant", font=("Arial", 20, "bold"), fg="cyan", bg="#1e1e2f").pack()


output_box = Text(root, wrap=WORD, font=("Arial", 12), bg="black", fg="white", height=20, width=70)
output_box.pack(pady=10)


start_btn = Button(root, text="Start Roy", command=lambda: threading.Thread(target=roy_ai).start(), font=("Arial", 14), bg="green", fg="white")
start_btn.pack(pady=10)


exit_btn = Button(root, text="Exit", command=root.destroy, font=("Arial", 14), bg="red", fg="white")
exit_btn.pack(pady=5)


root.mainloop()
