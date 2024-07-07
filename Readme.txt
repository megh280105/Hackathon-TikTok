405 Found - README
Overview
TikTok Sales Helper is a personal assistant designed to assist sales representatives by recording, transcribing, summarizing, and generating to-do lists from sales calls. This tool uses speech recognition, text summarization, and natural language processing to enhance the productivity and efficiency of sales interactions.
Features
* Voice Recording: Records sales calls through voice commands.
* Text Transcription: Transcribes recorded audio to text.
* Profanity Filtering: Censors inappropriate language in transcriptions.
* Call Summarization: Summarizes the transcribed text.
* To-Do List Creation: Extracts key details from the conversation and generates a to-do list.


Installation
1. Clone the Repository:
2. Install Dependencies: Install the necessary Python libraries by running the following commands: pip install transformers, pip install speech_recognition, pip install pyttsx3, pip install better_profanity
3. Setup Python Environment (if any errors occur):
* Install Xcode Command Line Tools:
xcode-select --install
   * Update Homebrew:
brew update
   * Reinstall Python using Homebrew:
brew reinstall python
   * Create and Activate a Virtual Environment:
python3 -m venv myenv
source myenv/bin/activate
      * Install setuptools:
pip install setuptools
Usage
         1. Start the Assistant:
python tiktok_sales_helper.py
         2. Follow the On-Screen Prompts:
            * Enter the company and customer name.
            * Record the call by speaking into your microphone.
            * Say "stop call" to end the recording.
            * Choose to summarize the call if desired.


            3. View Summary and To-Do List:
            * The summary of the call will be displayed.
            * A to-do list based on the conversation will be generated and shown.
Code Structure
            * random_id(): Generates a random 5-digit number.
            * record_text(): Captures and transcribes speech from the microphone.
            * output_text(company, name, text): Saves transcribed text to a file with profanity filtering.
            * summarize_file(file_path): Summarizes the content of a text file using a pre-trained model.
            * extract_reminder_details(text): Extracts details for creating reminders from the text.
            * create_todo_list(text): Generates a to-do list based on extracted details.
            * Main Program: Handles user input, records calls, saves transcriptions, summarizes calls, and creates to-do lists.
Dependencies
            * transformers
            * speech_recognition
            * pyttsx3
            * better_profanity
            * os
            * random
            * re
            * datetime