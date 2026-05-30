from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# LOAD MODEL
model = pickle.load(
	open('model.pkl', 'rb')
)

# LOAD TF-IDF VECTORIZER
vectorizer = pickle.load(
	open('vectorizer.pkl', 'rb')
)

# LOAD LABEL ENCODER
encoder = pickle.load(
	open('encoder.pkl', 'rb')
)


@app.route('/')
def home():

	return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

	text = request.form['clinical_note']

	text_vector = vectorizer.transform([text])

	prediction = model.predict(text_vector)

	specialty = encoder.inverse_transform(prediction)

	probabilities = model.predict_proba(text_vector)

	confidence = np.max(probabilities) * 100

	return render_template(
		'index.html',
		prediction=specialty[0],
		confidence=round(confidence, 2),
		input_text=text
	)


if __name__ == '__main__':

	app.run(debug=True)
