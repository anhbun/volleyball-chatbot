from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()

    user_message = data.get('msg', '').lower()

    # Define chatbot responses based on the incoming message
    if 'training' in user_message:
        reply = "Here's a great volleyball trainind drill for you: Try 3 sets of 10 spikes and 10 sets!"
    elif 'nutrition' in user_message:
        reply = "Pre-game nutrition tip: Eat a meal high in carbs and protein 2-3 hours before the game."
    elif 'injury' in user_message:
        reply = "To prevent ankle injuries, always stretch and wear proper footwear. Ice any pain postgame."
    elif 'mental' in user_message:
        reply = "Mental Wellness Tip: Visualize yourself succeeding in the game. It's key to building confidence."
    else:
        reply = "Hello! I am your Volleyball Training and Wellness Assistant. Ask me about training, nutrition, or injury prevention!"

    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)