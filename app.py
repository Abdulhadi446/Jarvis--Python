import speech_recognition as sr
import pyttsx3
import wikipedia
import datetime
import requests
import os
import webbrowser
import time
import threading
import random
import math
import string
import re


recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Secure API keys by storing them in environment variables
api_key = ("921bcee8ed642d28e47c4a003f6e5e9e")  # Ensure the environment variable is set correctly
news_api_key = ("f785af0b988f4820a99a5b03d045bebe")  # Set your news API key as an environment variable

def speak(text):
    """Speak the provided text."""
    engine.say(text)
    print("Jarvis: " + text)
    engine.runAndWait()

def listen():
    """Listen to the user's command."""
    with sr.Microphone() as source:
        speak("Listening.")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I can't understand. Please type your command.")
            # Ask for manual input if speech recognition fails
            manual_command = input("User said (manual input): ")
            return manual_command.lower()
        except sr.RequestError:
            speak("Sorry, my speech service is down. Please type your command.")
            # Ask for manual input if the service is down
            manual_command = input("User said: ")
            return manual_command.lower()

def greet():
    """Greet the user based on the time of day."""
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

def get_wikipedia_info(query):
    """Fetch information from Wikipedia."""
    try:
        summary = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia, " + summary)
    except wikipedia.exceptions.DisambiguationError:
        speak("The topic was too broad, please specify.")
    except Exception:
        speak("Sorry, I couldn't fetch information on that topic.")

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def get_city():
    try:
        response = requests.get("https://ipinfo.io")
        data = response.json()
        city = data.get("city")
        return city if city else "City not found"
    except requests.RequestException as e:
        return f"Error: {e}"

def get_weather(city):
    api_key = "921bcee8ed642d28e47c4a003f6e5e9e"  # Replace with your actual API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        return weather_data["main"]["temp"], weather_data["weather"][0]["description"]
    except requests.RequestException as e:
        return f"HTTP error occurred: {e}"




def tell_joke():
    """Tell a random joke."""
    joke = "Why did the scarecrow win an award? Because he was outstanding in his field!,"
    joke1 = "Why don't scientists trust atoms? Because they make up everything!"
    speak(f"{joke}. and second joke is {joke1}")

def recommend_movie():
    """Recommend a movie."""
    movie = "I recommend watching 'Inception'. It's a great thriller!"
    speak(movie)

def set_timer(minutes):
    """Set a timer for a specified number of minutes."""
    def timer():
        time.sleep(minutes * 60)  # Timer delay
        speak(f"Time's up! {minutes} minutes have passed.")
    threading.Thread(target=timer).start()
    speak(f"Setting a timer for {minutes} minutes.")

def convert_units(value, unit_from, unit_to):
    """Convert between units."""
    conversion_factors = {
        ('miles', 'kilometers'): 1.60934,
        ('kilometers', 'miles'): 0.621371,
        ('pounds', 'kilograms'): 0.453592,
        ('kilograms', 'pounds'): 2.20462,
        ('inches', 'centimeters'): 2.54,
        ('centimeters', 'inches'): 0.393701,
    }

    if (unit_from.lower(), unit_to.lower()) == ('celsius', 'fahrenheit'):
        converted_value = (value * 9/5) + 32
    elif (unit_from.lower(), unit_to.lower()) == ('fahrenheit', 'celsius'):
        converted_value = (value - 32) * 5/9
    else:
        key = (unit_from.lower(), unit_to.lower())
        if key in conversion_factors:
            converted_value = value * conversion_factors[key]
        else:
            speak("Sorry, I can't convert those units.")
            return

    speak(f"{value} {unit_from} is equal to {converted_value:.2f} {unit_to}.")

def add_to_todo_list(item):
    """Add an item to a to-do list."""
    todo_list.append(item)  # Assuming you have a list called todo_list
    speak(f"I've added {item} to your to-do list.")

def open_website(site):
    """Open a website."""
    if "http://" in site or "https://" in site:
        webbrowser.open(site)
        speak(f"Opening {site}.")
    else:
        webbrowser.open(f"https://{site}.com")
        speak(f"Opening {site}.com")

def get_news():
    """Fetch the latest news articles."""
    def fetch_articles():
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"
        response = requests.get(url)
        data = response.json()
        
        if data['status'] == 'ok' and data['totalResults'] > 0:
            first_article = data['articles'][0]
            return first_article
        else:
            return None

    if news_api_key:  # Use the correct API key variable
        article = fetch_articles()  
        
        if article:
            title = article['title']
            description = article['description']
            published_at = article['publishedAt']
            speak(f"Title: {title}. Description: {description}. Published At: {published_at}.")
        else:
            speak("No articles found.")
    else:
        speak("News service is unavailable. Please set your News API key in the environment variables.")


def main():
    greet()
    global todo_list  # Declare the global variable for the to-do list
    todo_list = ["Saying hello to my mom"]  # Example to-do list
    while True:
        command = listen()

        if "wikipedia" in command or "summary" in command:
            speak("What topic would you like to know about?")
            topic = listen()
            if topic:
                get_wikipedia_info(topic)
        
        elif "countdown timer" in command:
            speak("How many seconds.")
            seconds = int(listen())
            if seconds:
                speak(f"Start timer for {seconds} seconds.")
                while seconds:
                    mins, secs = divmod(seconds, 60)
                    timer = f"{mins:02d}:{secs:02d}"
                    print(timer, end="\r")
                    time.sleep(1)
                    seconds -= 1
                speak("Time's up!")

        elif "weather" in command or "environment" in command:
            # Get the city and then use it to fetch the weather
            city = get_city()
            if "Error" not in city:
                temperature, description = get_weather(city)
                speak(f"The weather in {city} is {temperature}°C with {description}.")
            else:
                print(city)
                
        elif "city" in command:
            city = get_city()
            print(city)

        elif  "what is happening" in command or "what happened" in command:
            get_news()

        elif "exit" in command or "stop" in command:
            speak("Are you sure you want to exit?")
            confirm_exit = listen()
            if "yes" in confirm_exit or "exit" in confirm_exit:
                speak("Goodbye!")
                break
        
        elif "tell me a joke" in command:
            tell_joke()

        elif "recommend a movie" in command:
            recommend_movie()

        elif "set a timer for" in command:
            try:
                minutes = int(command.split("for")[-1].strip().split()[0])  # Extract minutes
                set_timer(minutes)
            except ValueError:
                speak("I couldn't understand the number of minutes.")

        elif "convert" in command:
            # Example: "Convert 5 miles to kilometers"
            parts = command.split()
            try:
                value = float(parts[1])
                unit_from = parts[2]
                unit_to = parts[-1]
                convert_units(value, unit_from, unit_to)
            except (IndexError, ValueError):
                speak("I couldn't understand the conversion request.")

        elif "add to my to do list" in command:
            item = command.split("add to my to do list")[-1].strip()
            add_to_todo_list(item)

        elif "open file" in command or "file" in command:
            speak("What file do you want to open?")
            name = listen()  # Assuming listen() gets the file name from the user
            file_path = os.path.join("C:\\Users\\TECHNOSELLERS\\Downloads", name)

            # Check if the file exists before trying to open it
            if os.path.isfile(file_path):
                os.startfile(file_path)  # This will open the file with its default application
                speak(f"Opening file {name}")
            else:
                speak(f"File {name} not found.")

        elif "open facebook" in command:
            open_website("https://www.facebook.com/")
            speak("Opening facebook")

        elif "open itchio" in command:
            open_website("https://itch.io/")
            speak("Opening itch.io")

        elif "open youtube" in command:
            open_website("https://www.youtube.com/")
            speak("Opening youtube")

        elif "open" in command or "run" in command:
            speak("What would you like to open?")
            site = listen()
            if site:
                open_website(site)

        elif "search" in command:
            speak("What would you like to search for?")
            query = listen()
            if query:
                webbrowser.open(f"https://www.google.com/search?q={query}")

        elif "hello" in command or "hi" in command:
            speak("hello. I am here to help you today.")

        elif "what are you doing" in command:
            speak("I am answering your commands.")

        elif "location" in command or "country" in command or "region" in command or "cordinates" in command:
            try:
                response = requests.get("https://ipinfo.io")
                data = response.json()
                country = data.get("country")
                city = data.get("city")  # Access the city directly
                region = data.get("region")
                location = data.get("loc")  # Retrieves latitude and longitude
                speak(f" Country: {country}, Region: {region}, City: {city}, and Cordinates are {location}.")
            except requests.RequestException as e:
                print(f"Error: {e}")


        elif "close" in command or "unrun" in command:
            speak("Which app would you like to close?")
            name = listen()
            
            if name in ["chrome", "firefox", "edge"]:
                # Close specific browser by name; adjust based on your OS and browser choice
                if name == "chrome":
                    speak("Closing chrome.")
                    os.system("taskkill /f /im chrome.exe")  # For Windows
                elif name == "firefox":
                    speak("Closing FireFox.")
                    os.system("taskkill /f /im firefox.exe")  # For Windows
                elif name == "edge":
                    speak("Closing Edge.")
                    os.system("taskkill /f /im msedge.exe")  # For Windows
            else:
                try:
                    os.system(f"taskkill /f /im {name}.exe")  # For Windows
                    speak(f"{name.capitalize()} application closed.")
                except Exception as e:
                    speak(f"Could not close {name}. Error: {e}.")

        elif "what is apple" in command:
            speak("which are you saying, about apple fruit or apple company, do you want to visit apple official web.")
            answer = listen()
            if answer == "yes" or answer == "visit":
                webbrowser.open("https://www.apple.com/")
                speak("opening apple official web")

        elif "samsung" in command or "oppo" in command or "android" in command:
            speak("The mobile which you are talking is android. Do you want to open android official web")
            answer = license()
            if answer == "yes":
                webbrowser.open("https://www.android.com/")
                speak("opening anddroid official web")

        elif "random" in command:
            speak(f"Your random number is {random.randint(-1000000, 1000000)}.")

        elif "numeric" in command:
            speak("say numeric what you want to try.")
            s = listen()
            if s:
                speak(f"{s.isdigit()}")

        elif "smallest factor" in command:
            speak("Say Number! to get smallest factor")
            n = int(listen())
            if n:
                for i in range(2, n + 1):
                    if n % i == 0 and is_prime(i):
                        speak(f"{i}")

        elif "ascii value" in command:
            speak("Say Ascii value.")
            char = listen()
            if char:
                speak(f"Your value is {ord(char)}.")

        elif "char from ascii" in command:
            speak("What thing char do you want.")
            Str = listen()
            if Str:
                speak(f"Your value is {chr(Str)}.")
        
        elif "get quote" in command:
            speak("The only limit to our realization of tomorrow is our doubts of today.")

        elif "reverse word" in command:
            speak("Say a word to reverse.")
            s = listen
            if s:
                speak(str(s[::-1]))

        elif "hex to rgb"in command:
            hex_color = hex_color.lstrip('#')
            speak(str(tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))))

        elif "longest word"in command:
            speak("Say sentence to get longest word.")
            sentence = listen()
            if sentence:
                words = sentence.split()
                speak("The longest word in the sentence is "+str(max(words, key=len))+'.')

        elif "smallest word"in command:
            speak("Say sentence to get smallest word.")
            sentence = listen()
            if sentence:
                words = sentence.split()
                speak("The smallest word is "+str(sum(c.isdigit() for c in s))+".")

        elif "smallest prime factor"in command:
            speak("Say a number to get smallest factor")
            for i in range(2, n + 1):
                if n % i == 0 and is_prime(i):
                    speak("The smallest prime factor is "+str(i)+".")

        elif "count words" in command:
            speak("Word to count chars")
            s = listen
            speak(str(len(s.split())))

        elif "time" in command:
            speak("The current time is "+str(datetime.datetime.now().strftime("%H:%M:%S"))+".")

        elif "is valid email" in command:
            speak('What email you are asking for is valid.')
            email = listen()
            if email:
                pattern = r"[^@]+@[^@]+\.[^@]+"
                speak( re.match(pattern, email) is not None)

        elif "count vowels" in command:
            speak("Say the word to count Vowels.")
            s = int(listen)
            if s:
                speak("The count of vowels is "+str(sum(1 for char in s if char.lower() in 'aeiou')))

        elif "count consonants" in command:
            speak("Say a word to count consonants")
            s = listen()
            speak("The count of consonants is "+str(sum(1 for char in s if char.isalpha() and char.lower() not in 'aeiou')))

        elif 'create directory' in command:
            speak("Say directory.")
            directory = listen()
            if directory:
                speak('Creating your directory.')
                os.makedirs(directory, exist_ok=True)
                speak('Directory created.')

        elif "count spaces"in command:
            speak("Say a sentence to count spaces.")
            s = listen
            if s:
                speak("The count of spaces in a sentence is "+str(s.count(' '))+".")

        elif "square" in command:
            speak("Say Number to get square.")
            n = int(listen)
            speak(str(n ** 2))
        
        elif "cube" in command:
            speak("Say Number to get cube.")
            n = int(listen)
            speak(str(n ** 3))

        elif "decimal to binary" in command:
            speak("Say numbers to get binary.")
            n = int(listen())
            speak(str(bin(n).replace("0b", "")))

        elif 'binary to decimal' in command:
            speak("Say bunary to convert into decimal.")
            b = int(listen())
            if b:
                speak(str(int(b, 2)))
        elif 'first element' in command:
            speak("Say word to get first element.")
            lst = listen()
            if lst:
                value = lst[0] if lst else None
                speak(str(value))

        elif "max in dict"in command:
            speak("Say directory.")
            d = listen()
            if d:
                speak(str(max(d.values())))

        elif "min in dict"in command:
            speak("Say directory.")
            d = listen()
            if d:
                speak(str(min(d.values())))

        elif "key of max value"in command:
            speak("Say drectory to get max value.")
            d = listen()
            if d:
                speak(str(max(d, key=d.get)))

        elif 'key of min value'in command:
            speak("Say drectory to get min value.")
            d = listen()
            if d:
                speak(str(min(d, key=d.get)))

        elif "current unix timestamp":
            speak(str(int(time.time())))

        elif "timestamp to human readable"in command:
            ts = int(time.time())
            datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        elif "day of week"in command:
            date_string = f"{datetime.datetime.now().date}"
            date = datetime.datetime.strptime(date_string, '%Y-%m-%d')
            speak(date.strftime("%A"))

        elif "calculate age":
            speak("Say your birth date.")
            birth_date = listen()
            today = datetime.datetime.now()
            birth_date = datetime.datetime.strptime(birth_date, '%Y-%m-%d')
            speak(str(today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))))

        elif "random color"in command:
            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            speak(color)

        elif "count lines"in command:
            speak("Say file name or path.")
            filename = listen()
            if filename:
                with open(filename, 'r') as file:
                    some = str(len(file.readlines()))
                    speak(some)

        elif "random element from dict"in command:
            speak(str(random.choice(list(d.items())) if d else None))

        elif "delete directory" in command:
            speak("Which directory you want to delete.")
            directory = listen()
            if directory:
                speak("Deleting directory.")
                os.rmdir(directory)
                speak("Directory is deleted.")

        elif "generate password"in command:
            characters = string.ascii_letters + string.digits + string.punctuation
            length = 12
            speak("Your passor is "+''.join(random.choice(characters) for _ in range(length)))

        elif "check internet" in command:
            try:
                # Attempting to connect to Google to check internet availability
                response = requests.get("https://www.google.com", timeout=5)
                if response.status_code == 200:
                    speak("Internet is working.")
                else:
                    speak("Internet is connected, but there's an issue with the connection.")
            except requests.ConnectionError:
                speak("Your internet is not working.")
            except requests.Timeout:
                speak("The connection timed out. Please check your internet.")


        elif "get ip address"in command:
            apikey = {requests.get("https://api.ipify.org").text}
            speak(f"Your api key is {apikey}.")

        elif "find lenght of a word":
            speak("Say a word to count length")
            s = listen()
            if s:
                speak(str(len(s)))

        
        elif "i have an error" in command or "i got a priblem" in command:
            speak("Oh! no. can i help, you to solve this problem.")

        else:
            speak("I can not understand this command yet.")

if __name__ == "__main__":
    main()