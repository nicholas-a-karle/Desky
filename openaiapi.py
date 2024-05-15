import csv
import datetime
import re
from typing import Literal
from openai import OpenAI
import json
import os
from dotenv import load_dotenv
import requests
    
class Chat:

    def __init__(self, openai_api_key, serp_api_key):
        self.openai_api_key = openai_api_key
        self.serp_api_key = serp_api_key
        self.token_limit = 250
        self.client = OpenAI(api_key=self.api_key)
        self.message_history = []
        self.display_history = []
        self.running_model = 'gpt-4-turbo'
        self.use_console = True

    def __init__(self):
        # Load the .env file
        load_dotenv()
        # Get the OPENAI_API_KEY from environment variables
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if self.openai_api_key is None:
            raise ValueError("OPENAI_API_KEY not found in .env file")
        
        self.serp_api_key = os.getenv('SERP_API_KEY')
        if self.serp_api_key is None:
            raise ValueError("SERP_API_KEY not found in .env file")

        self.token_limit = 250
        self.client = OpenAI(api_key=self.openai_api_key)
        self.message_history = []
        self.display_history = []
        self.running_model = 'gpt-4-turbo'
        self.use_console = True

    def google_search(self, query):
        search_url = "https://serpapi.com/search"
        params = {
            "engine": "google",
            "q": query,
            "api_key": self.serp_api_key
        }
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        return response.json()

    def add_message_to_history(self, content: str, role: Literal['system', 'user', 'assistant'] = 'user'):
        if role not in {'system', 'user', 'assistant'}:
            raise ValueError("Role must be 'system' or 'user'")
        self.message_history.append({'role': role, 'content': content})

    def add_message_to_display(self, content: str, role: Literal['system', 'user', 'assistant'] = 'user'):
        if role not in {'system', 'user', 'assistant'}:
            raise ValueError("Role must be 'system' or 'user'")

        self.display_history.append({'role': role, 'content': content})

        
    def prompt(self, content: str, role: Literal['system', 'user', 'assistant'] = 'user', with_history = True, append_to_history = True, append_to_display = True):
        if role not in {'system', 'user', 'assistant'}:
            raise ValueError("Role must be 'system' or 'user'")

        if with_history:
            messages = self.message_history + [{'role': role, 'content': content}]
        else:
            messages = [{'role': role, 'content': content}]

        # currently just takes choices[0]
        response = self.client.chat.completions.create(
            model=self.running_model,
            messages=messages,
            max_tokens=self.token_limit
        ).choices[0]

        response_content = response.message.content
        response_role = response.message.role

        if append_to_history:
            self.add_message_to_history(content, role=role)    
            self.add_message_to_history(response_content, role = response_role)

        if append_to_display:
            self.add_message_to_display(content, role=role)
            self.add_message_to_display(response_content, role = response_role)

if __name__ == "__main__":
    uin = "START"
    print("Please start your chat with GPT")

    chat = Chat()
    while (uin != "END"):
        uin = input("USER: \t\t")
        if uin == "END": break # redundancies in checking, makes me feel better though
        chat.prompt(uin)
        display_message = chat.display_history[-1]
        print(f"{display_message['role'].upper()}: \t{display_message['content']}")

    print(chat.google_search("Software Engineering Role in LA"))