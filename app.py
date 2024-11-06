from flask import Flask, render_template, request, redirect, url_for
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()

conversation_history = []

# Chat GPT clone
@app.route('/')
def chat():
    return render_template('chat.html', conversation=conversation_history)

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['message']
    
    # Append the user message to the conversation history
    conversation_history.append({"role": "user", "content": user_message})
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.5,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
        ] + conversation_history  # Include the conversation history
    )
    
    response_message = completion.choices[0].message.content
    
    # Append the assistant's response to the conversation history
    conversation_history.append({"role": "assistant", "content": response_message})
    
    return render_template('chat.html', conversation=conversation_history)


@app.route('/reset_chat', methods=['POST'])
def reset_chat():
    global conversation_history
    conversation_history = []  # Clear the conversation history
    return redirect(url_for('chat'))  # Redirect to the chat page

# Image generation
@app.route('/image_gen')
def image_gen():
    return render_template('image_gen.html')

@app.route('/generate_image', methods=['POST'])
def generate_image():
    prompt = request.form['prompt']
    image_response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = image_response.data[0].url
    return render_template('image_gen.html', image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)