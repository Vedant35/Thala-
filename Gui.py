import json
import requests
import uuid
import tkinter as tk
import os
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# Load service account credentials
SERVICE_ACCOUNT_FILE = 'newagent-vxbt-cc7c0d88c7aa.json'  # Replace with your JSON key file path
DIALOGFLOW_PROJECT_ID = 'newagent-vxbt'  # Replace with your Dialogflow project ID
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = str(uuid.uuid4())

# Function to get a Google OAuth2 access token
def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    credentials.refresh(Request())
    return credentials.token

# Function to call the Dialogflow API and get a response
def get_bot_response(user_input):
    access_token = get_access_token()
    url = f"https://dialogflow.googleapis.com/v2/projects/{DIALOGFLOW_PROJECT_ID}/agent/sessions/{SESSION_ID}:detectIntent"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "query_input": {
            "text": {
                "text": user_input,
                "language_code": DIALOGFLOW_LANGUAGE_CODE,
            }
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        return response_json["queryResult"]["fulfillmentText"]
    except Exception as e:
        return f"Error: {str(e)}"

# Function to handle the user input and display the bot response
def send_message():
    user_message = user_input.get()
    if user_message:
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, "You: " + user_message + "\n")
        user_input.delete(0, tk.END)

        bot_response = get_bot_response(user_message)
        chat_history.insert(tk.END, "Bot: " + bot_response + "\n")
        chat_history.config(state=tk.DISABLED)
        chat_history.yview(tk.END)

# Initialize the main window
window = tk.Tk()
window.title("ChatBot Interface")
window.geometry("500x500")

# Chat history display
chat_history = tk.Text(window, height=20, width=60, state=tk.DISABLED)
chat_history.pack(pady=10)

# User input field
user_input = tk.Entry(window, width=50)
user_input.pack(pady=5)

# Send button
send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack()

# Start the Tkinter event loop
window.mainloop()
