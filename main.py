from transformers.pipelines import pipeline
import openai
import os
import threading
import time
import queue
import random
import cv2  # For computer vision
import numpy as np

openai.api_key = os.getenv("OPENAI_API_KEY")

# Simulated API functions - replace these with real API integrations


# Load a free Hugging Face model (this may take ~1 min to download on first run)
chatbot = pipeline("text2text-generation", model="google/flan-t5-small")

def aeris_reply(user_input):
    try:
        prompt = f"You are Aeris, a friendly AI assistant. Respond to Yash Raj's question: {user_input}"
        result = chatbot(prompt, max_length=100, do_sample=True)
        return next(result)[0]["generated_text"]
    except Exception as e:
        return f"Error using free model: {e}"

# Test the bot
if __name__ == "__main__":
    print("Testing Aeris...")
    reply = aeris_reply("Who is Iron Man?")
    print("Aeris says:", reply)


def chatbot_api(query):
    responses = [
        "Hey Yash Raj! What can I help you with today?",
        "I'm here to answer your questions anytime.",
        "Tell me more, I'm all ears!"
    ]
    time.sleep(1)
    return random.choice(responses)

def coding_api(query):
    # Simulated coding knowledge response
    responses = [
        "Here's a quick coding tip: Always comment your code! 😊",
        "Did you know that Python has a built-in function called 'len()' to get the length of a list?",
        "For debugging, try using print statements to track variable values! 💻"
    ]
    time.sleep(1)
    return random.choice(responses)

def girl_speak_style(text):
    # Transform text to casual friendly girl speak style with emojis and interjections
    interjections = ["OMG, ", "Heyy~ ", "So, ", "You know, ", "Aww, "]
    endings = [" 💖", " 😊", " 💕", " 😘", " ✨"]
    interjection = random.choice(interjections)
    ending = random.choice(endings)
    styled_text = f"{interjection}{text}{ending}"
    return styled_text

class Aeris:
    def __init__(self, owner_name="Yash Raj"):
        self.owner_name = owner_name
        self.running = True
        self.input_queue = queue.Queue()
        self.response_queue = queue.Queue()
        self.api_functions = [chatbot_api, coding_api]

    def start(self):
        threading.Thread(target=self.input_listener, daemon=True).start()
        threading.Thread(target=self.response_processor, daemon=True).start()
        greeting = girl_speak_style(f"Hello {self.owner_name}! I'm Aeris, your personal assistant. Ready to help you anytime!")
        print(f"Aeris: {greeting}")
        print("(Type 'exit' to quit)\n")
        while self.running:
            time.sleep(0.1)

    def input_listener(self):
        while self.running:
            try:
                user_input = input(f"{self.owner_name}: ")
                if user_input.strip().lower() == "exit":
                    self.running = False
                    farewell = girl_speak_style(f"Goodbye {self.owner_name}! Talk soon! 💖")
                    print(f"Aeris: {farewell}")
                else:
                    self.input_queue.put(user_input)
            except EOFError:
                self.running = False

    def response_processor(self):
        while self.running:
            try:
                query = self.input_queue.get(timeout=0.1)
                responses = []
                for api_func in self.api_functions:
                    response = api_func(query)
                    responses.append(response)
                chosen_response = random.choice(responses)
                styled_response = girl_speak_style(chosen_response)
                self.response_queue.put(styled_response)
            except queue.Empty:
                continue

            while not self.response_queue.empty():
                answer = self.response_queue.get()
                print(f"Aeris: {answer}\n")




