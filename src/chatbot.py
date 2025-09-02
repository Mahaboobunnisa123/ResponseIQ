import json
import os
import nltk
import ssl
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

# Initialize console
console = Console()

# Handle SSL for nltk
ssl._create_default_https_context = ssl._create_unverified_context
nltk.data.path.append(os.path.abspath("nltk_data"))
nltk.download('punkt')

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

# Load intents.json
with open(os.path.join(DATA_DIR, "intents.json"), "r") as file:
    intents = json.load(file)

# Create vectorizer & classifier
vectorizer = TfidfVectorizer()
clf = LogisticRegression(random_state=0, max_iter=10000)

# Preprocess the data
tags = []
patterns = []
for intent in intents["intents"]:   # loop inside "intents" list
    for pattern in intent['patterns']:
        tags.append(intent['tag'])
        patterns.append(pattern)

# Train the model
x = vectorizer.fit_transform(patterns)
y = tags
clf.fit(x, y)

# Chatbot function
def chatbot(input_text):
    input_text = vectorizer.transform([input_text])
    tag = clf.predict(input_text)[0]
    for intent in intents["intents"]:   # FIX: use loaded intents
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])
            return response
    return "Sorry, I didn't understand that."

# Run chatbot interactively
if __name__ == "__main__":
    console.print(Panel("🤖 [bold cyan]RespondIQ Chatbot[/bold cyan]\nType 'quit' to exit.", style="cyan"))

    while True:
        user_input = console.input("[bold green]You:[/bold green] ")
        if user_input.lower() == "quit":
            console.print(Panel("👋 Goodbye! Have a great day!", style="yellow"))
            break

        response = chatbot(user_input)

        # User bubble (right-aligned, green)
        console.print(
            Align.right(
                Panel.fit(user_input, title="🧑 You", style="bold green", border_style="green")
            )
        )

        # Bot bubble (left-aligned, magenta)
        console.print(
            Align.left(
                Panel.fit(response, title="🤖 Bot", style="bold magenta", border_style="magenta")
            )
        )