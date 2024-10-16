import spacy
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Load spaCy's English model
nlp = spacy.load('en_core_web_lg')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_message = data.get('msg', '').lower()
    doc = nlp(user_message)

    # Similarity threshold
    threshold = 0.6

    # Related terms
    training_terms = ["train", "training"]
    nutrition_terms = ["nutrition"]
    injury_terms = ["injury", "hurt"]
    mental_terms = ["mental", "mentally", "nervous"]
    joke_terms = ["joke", "laugh", "funny"]

    # Similarity score for intents
    training_score = max(doc.similarity(nlp(term)) for term in training_terms)
    nutrition_score = max(doc.similarity(nlp(term)) for term in nutrition_terms)
    injury_score = max(doc.similarity(nlp(term)) for term in injury_terms)
    mental_score = max(doc.similarity(nlp(term)) for term in mental_terms)

    # Similarity score for each intent
    scores = {
        'training': training_score,
        'nutrition': nutrition_score,
        'injury': injury_score,
        'mental': mental_score
    }

    # Finds the intent with the highest similarity score above the threshold
    best_intent = max(scores, key=scores.get)
    best_score = scores[best_intent]

    # Debugging purposes
    print("Tokens: ", [token.text for token in doc]) # See all tokens in the input
    print("Lemmas: ", [token.lemma_ for token in doc]) # See lemmatized forms of tokens
    print("Training score: ", round(training_score, 2)) # See similarity scores for "training"
    print("Nutrition score: ", round(nutrition_score, 2))
    print("Injury score: ", round(injury_score, 2))
    print("Mental score: ", round(mental_score, 2))

    # Define chatbot responses based on the incoming message
    if best_score >= threshold:
        if best_intent == 'training':
            reply = "Try 3 sets of 10 spikes and 10 sets!"
        elif best_intent == 'nutrition':
            reply = "Eat a meal high in carbs and protein 2-3 hours before your game."
        elif best_intent == 'injury':
            reply = "Stretch before your game. Ice any areas that you feel soreness."
        elif best_intent == 'mental':
            reply = "Visualize yourself succeeding in the game. It's key to building confidence."
    else:
        reply = "I'm sorry. What was that?"

    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)