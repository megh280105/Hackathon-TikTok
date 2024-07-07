import os
from transformers import pipeline
import speech_recognition as sr
from better_profanity import profanity
import random
import pyttsx3
import random
import re


# Defining a function to generate a random 5 digit ID
def random_id():
    random_number = random.randint(10000, 99999)  # Generate random 5-digit number
    return random_number


randomID = random_id()    # Storing the random number in variable, random

r = sr.Recognizer()     # Initializing the speech recognizer


# Defining a function to record text recorded from the microphone 
def record_text():

    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)   # Adjusting for ambient noise with a 0.2s duration
            audio2 = r.listen(source2)      # Listen to the source 
            myText = r.recognize_google(audio2)     # Using Google API to recognize speech
            return myText
        
    except sr.RequestError as e:        # Incase of any unexpected errors
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("Unknown error occurred")

    return ""


# Defining a function to output the recorded text to file with the company's name, person and the id, with profanity censorship
def output_text(company, name, text):

    censored_text = profanity.censor(text)
    filename = f"{company}_{name}_{randomID}.txt"
    with open(filename, "a") as f:
        f.write(censored_text + "\n")


# Function to summarize the text from the specified file
def summarize_file(file_path):

    os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'     # Setting the environment variable within the script
    model_name = "sshleifer/distilbart-cnn-12-6"       #Specifying the model we're using
    summarizer = pipeline('summarization', model=model_name, device=-1)     # Creating the pipeline with specified model
    with open(file_path, 'r') as file:
        text = file.read()      # Reading text from a file
        summary = summarizer(text, max_length=50, min_length=10, do_sample=False)   # Setting constraints for the output
    return summary


# Defining a funciton to fetch the reminder details from the text
def extract_reminder_details(text):
    
    subject_pattern = r'\b(meeting|appointment)\b'# Providing a pattern to detect
    subject_match = re.search(subject_pattern, text, re.IGNORECASE)
    
    if subject_match:
        subject = subject_match.group(1)
    else:
        subject = "Subject not found"
    
    return {
        "Subject": subject.strip()
    }

# This function is used to create a to do list using the function above and sends a text to the user
def create_todo_list(text):

    reminder_details = extract_reminder_details(text)
    todo_list = [
        f"Reminder set for: {reminder_details['Subject']}.",       # Format for the reminder
    ]
    return todo_list

# Narrative recommendation: possible responses
context_responses = {
    "department": ["Hello! How are you doing?", "Good day! How are you doing today?", "Hi there! How are you?"],
    "****": ["I'm sorry sir, but using bad language is strictly restricted at our office", "We have a strict policy against using offensive language in our office.", "I'm sorry, but we don't allow the use of offensive language in our workplace."],
    "appintment": ["Yes, we'll take care of that right away.", "Sure, I'll make sure it gets done.", "Affirmative, it's on the list."],
    "thank you": ["You're welcome!", "Glad to be of help!", "Anytime! Have a great day!"],
}

# Recommending responses to the user randomly
def recommend_response(context):
    if context in context_responses:
         print(f"Here are the possible responses: {random.choice(context_responses[context])}")
    else:
        return "                                                    "


# The code begins here, welcoming the user 
print("Welcome to TikTok sales helper! Your personal assistant")

# Takes the input given by the user
ans = input("Would you like to record this call? ").lower()

# If they type in yes
if ans == "yes":

    # The code then asks them for the company calling, customer's name and starts recording the call
    company = input("Company: ")
    name = input("Customer Name: ")
    while True:

        # Recording the call using the record_text() function
        text = record_text()

        # The call stops once the user says "Stop the call"
        if text.lower() == "stop the call":
            print("                                                     ")
            print("Call ended")
            print("                                                     ")

            # Then it asks the user if they would want to summarize the call
            sum = input("Would you like to summarize your call? ")

            # If their response is yes, then it takes text from the specified file and summarizes it
            if sum.lower() == "yes":
                file_path = f"{company}_{name}_{randomID}.txt"
                summary = summarize_file(file_path)
                print(summary)
                print("                                                     ")

                # Then comes the to-do list the code extracted from the text
                print("Here is your to do list: ")
                print("                                                     ")

                # Read conversation text from file
                file_path = f"{company}_{name}_{randomID}.txt"
                with open(file_path, 'r') as file:
                    conversation_text = file.read()

                # Create the to-do list
                todo_list = create_todo_list(conversation_text)

                # Print the to-do list
                for item in todo_list:
                    print(item)
            break

        # Write to the file 
        output_text(company, name, text)

        # lets the user know the file where the call was recorded
        print(f"Statement recorded in file: {company}_{name}_{randomID}.txt")

         # Determine context based on user input
        if "department" in text.lower():
            context = "department"
        elif "shit" in text.lower() or "****" in text.lower():
            context = "****"
        elif "appointment" in text.lower() or "meeting" in text.lower():
            context = "appointment"
        elif "thank you" in text.lower() or "thanks" in text.lower():
            context = "thank you"
        else:
            context = "unknown"

        # Using narrative recommendation
        response = recommend_response(context)
        print("                                                     ")
    


# End of code
