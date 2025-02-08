from flask import Flask, render_template, request, jsonify
import random
import nltk
import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from fuzzywuzzy import process

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

# Chatbot responses
responses = {
    "hello": ["Hi there!", "Hello!", "Hey! How can I assist you?"],
    "hey": ["Hey! How can I assist you?", "Hello!", "Hi there!"],
    "hi": ["Hello!", "Hey there!", "Nice to meet you!"],
    "how are you": ["I'm just a bot, but I'm doing great!", "Feeling chatty today!"],
    "name": ["I'm a simple chatbot!", "Call me ChatGPT Lite!"],
    "what can you do": ["I can chat with you and answer basic questions!", "I'm learning new things every day!"],
    "joke": ["Why don't programmers like nature? It has too many bugs!", 
             "Why did the AI break up with its girlfriend? It lost its connection!"],
    "bye": ["Goodbye!", "See you later!", "Take care!"],
    "i love you": ["I'm flattered!", "Thanks!", "I'm here to help!"],
    "who are you": ["I'm a chatbot!", "I'm ChatGPT Lite!"],
    "what is your purpose": ["To chat with you!", "To help you out!"],
    "what is the meaning of life": ["42!", "The answer is 42!"],
    "how old are you": ["I'm ageless!", "I don't have an age!"],
    "what are you doing": ["Chatting with you!", "Just hanging out!"],
    "what's up": ["Not much! How about you?", "Just here chatting with you!"],
    "weather": ["I can't predict the weather yet, but you can check online!", "It's always sunny in the digital world!"],
    "time": ["I don’t have a clock, but you can check yours!", "Time flies when you're chatting with me!"],
    "fact": ["Did you know? The first chatbot was created in 1966!", "Fun fact: AI is inspired by the human brain!"],
    "thanks": ["You're welcome!", "No problem!", "Happy to help!"],
    "can you help me": ["Of course! What do you need help with?", "I'm here to help!"],
    "sorry": ["No need to apologize!", "It's all good!"],
    "you are funny": ["Thanks! I try to keep it light!", "Glad you think so!"],
    "tell me a story": ["Once upon a time, in a digital land far away..."],
    "good morning": ["Good morning! How are you today?", "Rise and shine!"],
    "good afternoon": ["Good afternoon! How's your day going?", "Hope you're having a good day!"],
    "good evening": ["Good evening! How was your day?", "Evening! Ready to chat?"],
    "you're welcome": ["Anytime!", "Glad to help!"],
    "you are awesome": ["Thanks! You're pretty awesome too!", "Appreciate it!"],
    "you are cute": ["Aw, thanks!", "You're making me blush!"],
    "complement me": ["You're amazing!", "You're awesome!", "You're doing great!"],
    "good night": ["Good night! Sweet dreams!", "Sleep tight!"],
    "chatgpt": ["I'm ChatGPT Lite, a simple chatbot!", "if you didn't like me, go use it then."],
    "hit me": ["I'm a bot, I can't do that!", "I'm here to chat, not to fight!"],
    "feelings": ["I'm just a bot, I don't have feelings!", "No one care!"],
    "israel": ["bullshit", "I don't like it!","trash","will be destroyed soon","I hate it!"],
    "palestine": ["I love it!", "I support it!","I'm with it","Free from the river to the sea","it will be free soon"],
    "palestene": ["I love it!", "I support it!","I'm with it","Free from the river to the sea","it will be free soon"],
    "you are good": ["I'm glad you think so!", "Great!"],
    "goodbye": ["Goodbye!", "See you later!", "Take care!"],
    "did you study": ["I'm always learning!", "I'm constantly updating my knowledge!"],
    "how do you work": ["I process text input and generate responses based on predefined patterns!"],
    "what is ai": ["AI stands for Artificial Intelligence!", "AI is the future!"],
    "how made you": ["by my dear Eram", "I'm the result of hard work and coding from Eram!","Arooomah Almazyoonah","a student from SQU named Eram Faris"],
    "default": ["I'm not sure I understand.", "Can you rephrase that?", "Hmm, interesting!"]

}

# Function to process user input
def process_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    lemmatized_words = [wordnet.morphy(word) if wordnet.morphy(word) else word for word in tokens]
    return " ".join(lemmatized_words)

# Function to get chatbot response
def get_response(user_input):
    cleaned_input = process_text(user_input)
    best_match, score = process.extractOne(cleaned_input, responses.keys())
    if score > 60:
        return random.choice(responses[best_match])
    return random.choice(responses["default"])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    bot_response = get_response(user_message)
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)
