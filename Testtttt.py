import os
from transformers import pipeline
import random
import speech_recognition as sr
import pyttsx3
from better_profanity import profanity
import random
import re
from datetime import datetime


def random_id():
    random_number = random.randint(10000, 99999)  # Generate random 5-digit number
    return random_number

random = random_id()

r = sr.Recognizer()

def record_text():
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            audio2 = r.listen(source2)
            myText = r.recognize_google(audio2)
            return myText
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        print("Unknown error occurred")
    return ""

def output_text(company, name, text):
    censored_text = profanity.censor(text)
    filename = f"{company}_{name}_{random}.txt"
    with open(filename, "a") as f:
        f.write(censored_text + "\n")

def summarize_file(file_path):
    # Set the environment variable within the script
    os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'
    
    # Specify the model explicitly
    model_name = "sshleifer/distilbart-cnn-12-6"
    
    # Create the summarization pipeline with the specified model
    # Set device=-1 to use the CPU
    summarizer = pipeline('summarization', model=model_name, device=-1)
    
    # Read the text from the file
    with open(file_path, 'r') as file:
        text = file.read()
    
    # Adjust max_length to be appropriate for summarization
    summary = summarizer(text, max_length=60, min_length=30, do_sample=False)
    
    return summary


def extract_reminder_details(text):
    subject_pattern = r'\b(?:meeting|appointment)\s+regarding\s+([\w\s]+)\b'
    subject_match = re.search(subject_pattern, text, re.IGNORECASE)
    
    if subject_match:
        subject = subject_match.group(1)
    else:
        subject = "Subject not found"
    
    return {
        "Subject": subject.strip()
    }

def create_todo_list(text):
    reminder_details = extract_reminder_details(text)
    todo_list = [
        f"Set a reminder for a meeting regarding {reminder_details['Subject']}.",
    ]
    return todo_list

print("Welcome to TikTok sales helper! Your personal assistant")
ans = input("Would you like to record this call? ").lower()

if ans == "yes":
    company = input("Company: ")
    name = input("Customer Name: ")
    while True:
        text = record_text()
        if text.lower() == "stop call":
            print("                                                     ")
            print("Call ended")
            print("                                                     ")
            sum = input("Would you like to summarize your call?")
            if sum.lower() == "yes":
                file_path = f"{company}_{name}_{random}.txt"
                summary = summarize_file(file_path)
                print(summary)
                print("                                                     ")
                print("Here is your to do list: ")
                print("                                                     ")
                # Read conversation text from file
                file_path = f"{company}_{name}_{random}.txt"
                with open(file_path, 'r') as file:
                    conversation_text = file.read()

                # Create the to-do list
                todo_list = create_todo_list(conversation_text)

                # Print the to-do list
                for item in todo_list:
                    print(item)
            break
        output_text(company, name, text)
        print(f"Statement recorded in file: {company}_{name}_{random}.txt")
