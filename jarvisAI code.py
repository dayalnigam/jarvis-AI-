import speech_recognition as sr
import wikipedia
import pyttsx3 #pip install pyttsx3
import speech_recognition as sr  #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import requests
from bs4 import BeautifulSoup
import json
import os
import smtplib
from covid import Covid

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[1].id)
engine.setProperty('voice', voices[0].id)

def takeCommand():
    r=sr.Recognizer()
    print(sr.Microphone.list_microphone_names())
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=1)
        currentTime = datetime.datetime.now()
        if currentTime.hour < 12:
            engine.say("Good morning sir,I am Jarvis Please tell me how may I help you")
            engine.runAndWait()
            audio= r.listen(source)
        elif 12 <= currentTime.hour < 18:
            engine.say("Good Afternoon sir,I am Jarvis Please tell me how may I help you")
            engine.runAndWait()
            audio= r.listen(source)
        elif 18 <= currentTime.hour < 19:
            engine.say("Good evening sir,I am Jarvis Please tell me how may I help you")
            engine.runAndWait()
            audio= r.listen(source)
        else:
            engine.say("Good night sir,I am Jarvis Please tell me how may I help you")
            engine.runAndWait()
            audio= r.listen(source)
    # r.energy_threshold()
        #engine.say("I am Jarvis Sir. Please tell me how may I help you")
        #engine.runAndWait()
        #audio= r.listen(source)

        try:
            text = r.recognize_google(audio)
            print(text)
            if 'time' in text:
                hour = datetime.datetime.now()
                print(hour)
                engine.say(f"Sir, current date & time is {hour} .")
                engine.runAndWait()
            elif 'news' in text:
                speak_news()
            elif 'covid-19' in text:
                Covid_data()
            elif 'nodemcu' in text:
                Nodemcu_data() 
            else:
                title=wikipedia.search(text)[0]
                page=wikipedia.page(title)
                text1=page.content
                engine.say(text1)
                engine.runAndWait()
        except:
            engine.say("Sorry sir i am not able to recognize you i am not connected to internet")
            engine.runAndWait()
            
def speak_news():
     url = 'https://newsapi.org/v2/top-headlines?sources=the-times-of-india&language=en&apiKey=8e19b13f4d674732b6fa9c425b2fdc45'
     req = requests.get(url, 'lxml')
     soup = BeautifulSoup(req.content, 'html.parser')
     news_dict = json.loads(soup.prettify())
     arts = news_dict['articles']
     for index, articles in enumerate(arts):
         engine.say(articles['title'])
         engine.runAndWait()
         if index == len(arts)-1:
             break
         engine.say('Moving on the next news headline..')
     engine.say('These were the top headlines, Have a nice day Sir!!..')
     engine.runAndWait()

def Covid_data():
    covid = Covid()
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=1)
        engine.say('please tell me the name of the country for which u have to find covid-19 cases')
        engine.runAndWait()
        audio= r.listen(source)
        text = r.recognize_google(audio)
    print(text)
    cases = covid.get_status_by_country_name(text)['active']
    engine.say(f'sir the current active cases in {text} are {cases}' )
    engine.runAndWait()

def Nodemcu_data():
    url = 'http://192.168.43.45/'
    req = requests.get(url, 'lxml')
    soup = BeautifulSoup(req.content, 'html.parser')
    node=soup.find('p').getText()
    engine.say(f'the current Data from Nodemcu is {node} sir')
    engine.runAndWait()
    
    

    
    
    
if __name__ == "__main__":
    takeCommand()
    
    


