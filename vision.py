import speech_recognition as sr
import webbrowser
import urllib.parse
import pywhatkit as kit
from google import genai
import pyttsx3 
import pyautogui  
import time
import os  # Imported to handle system-level operations like shutdown

# ==================== AI SETUP ====================

# ⚠️ IMPORTANT: Please generate a NEW API Key from Google AI Studio and paste it here
API_KEY = "API_KEY" 

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    print("AI Client Setup Error:", e)

# ==================== YOUR CONTACTS BOOK ====================
CONTACTS = {
    "Naman": "+918929730378",
    "vipib": "+919988776655",
    "amit": "+918877665544",
    "brother": "+917766554433"
}

# ==================== ENGLISH MALE VOICE SETUP ====================

def speak(text):
    """This function speaks out the text in an English male voice (David)"""
    print("Vision:", text)
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id) 
        engine.setProperty('rate', 170) 
        engine.say(text)
        engine.runAndWait()
        engine.stop() 
    except Exception as e:
        print("Voice Error:", e)

def take_command():
    """This function captures audio input from your microphone"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower().strip()
    except:
        return ""

# ==================== MAIN PROGRAM LOOP ====================

speak("Hello Vishal, I am Vision. How can I help you today?")

while True:
    command = take_command()

    if not command:
        continue

    # --- 1. OPEN WHATSAPP ONLY ---
    if command == "open whatsapp" or command == "open chat":
        speak("Opening WhatsApp for you, Vishal.")
        webbrowser.open("https://web.whatsapp.com")

    # --- 2. WHATSAPP FEATURE (BY CONTACT NAME) ---
    elif "whatsapp" in command or "send message" in command:
        target_name = ""
        phone_number = ""
        
        if "to" in command:
            target_name = command.split("to")[-1].strip()
            
        if not target_name or target_name not in CONTACTS:
            speak("Whom do you want to send a WhatsApp message to?")
            target_name = take_command().strip()
            
        if target_name in CONTACTS:
            phone_number = CONTACTS[target_name]
            speak(f"What is the message for {target_name}?")
            message = take_command()
            
            if message:
                speak(f"Sending message to {target_name}")
                kit.sendwhatmsg_instantly(phone_number, message, wait_time=15, tab_close=True)
                time.sleep(2)
                pyautogui.press("enter")  
                speak("Message sent successfully.")
            else:
                speak("Message was empty. Operation cancelled.")
        else:
            speak(f"Sorry Vishal, I couldn't find {target_name} in your contact list.")

    # --- 3. YOUTUBE AUTOMATIC PLAY FEATURE ---
    elif "play song" in command or "play" in command:
        song = command.replace("play song", "").replace("play", "").strip()
        if song:
            speak(f"Playing {song} on YouTube")
            kit.playonyt(song) 
        else:
            speak("Which song would you like to play?")

    # --- 4. GOOGLE SEARCH FEATURE ---
    elif "search" in command or "google" in command:
        search_query = command.replace("search", "").replace("google", "").strip()
        if search_query:
            speak(f"Searching for {search_query} on Google")
            query = urllib.parse.quote_plus(search_query)
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            speak("What should I search for?")

    # --- 5. LAPTOP SHUTDOWN FEATURE ---
    elif "shutdown" in command or "turn off pc" in command or "system off" in command:
        speak("Shutting down your laptop in 5 seconds. Please save your work, Vishal. Goodbye!")
        time.sleep(5)  # Gives the user 5 seconds to save any unsaved work
        os.system("shutdown /s /t 1")  # Executes Windows shutdown command
        break

    # --- 6. EXIT FEATURE ---
    elif "stop" in command or "exit" in command or "bye" in command:
        speak("Goodbye Vishal, have a great day!")
        break

    # --- 7. AI CHAT FEATURE (CORRECT NEW SDK MODEL) ---
    else:
        try:
            print("Vision is thinking...")
            
            # Standard valid model name for Google GenAI SDK v2
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=(
                    f"You are Vision, a smart male AI voice assistant like Jarvis. "
                    f"You are talking to Vishal. Reply in very short, 1 line, professional ENGLISH. "
                    f"Strictly do NOT use any markdown characters like asterisks (*). "
                    f"User said: {command}"
                )
            )
            ai_reply = response.text
            clean_reply = ai_reply.replace("*", "").replace("#", "").replace("`", "").strip()
            
            if clean_reply:
                speak(clean_reply)
            else:
                speak("I did not catch that.")
        except Exception as e:
            print("AI Error Detail:", e)
            if "429" in str(e) or "Quota" in str(e):
                speak("Vishal, the current project quota is full. Please use a new API key.")
                time.sleep(5) 
            else:
                speak("I am facing a connection issue with my servers.")