from flask import Flask, render_template, url_for, request, redirect, session
import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from dashboard import calculate_statistics, generate_trend_plot, generate_category_plot

# Load the model and vectorizer
filename = 'nlp_model.pkl'
clf = pickle.load(open(filename, 'rb'))
cv = pickle.load(open('tranform.pkl', 'rb'))

app = Flask(__name__)
app.secret_key = "secret_key"  # Needed for session management

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        sender_email = request.form['sender_email']
        receiver_email = request.form['receiver_email']
        
        # Save emails in the session
        session['sender_email'] = sender_email
        session['receiver_email'] = receiver_email
        
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    stats = calculate_statistics()
    trend_plot = generate_trend_plot()
    category_plot = generate_category_plot()
    return render_template('dashboard.html', stats=stats, trend_plot=trend_plot, category_plot=category_plot)

@app.route('/')
def home():
    if 'sender_email' not in session or 'receiver_email' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        message = request.form['message']
        data = [message]
        vect = cv.transform(data).toarray()
        my_prediction = clf.predict(vect)
        
        # Determine background color based on prediction
        bg_color = "red" if my_prediction[0] == 1 else "green"
        prediction_text = "Spam" if my_prediction[0] == 1 else "Not Spam"
        
        return render_template(
            'result.html', 
            prediction=prediction_text, 
            bg_color=bg_color,
            sender_email=session.get('sender_email'),
            receiver_email=session.get('receiver_email')
        )

if __name__ == '__main__':
    app.run(debug=True)
