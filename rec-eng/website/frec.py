from flask import Flask, render_template, request
from . import rec
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/recommendations', methods=['POST'])
def recommendations():
    song_name = request.form['song_name']
    recommendations = rec.get_recommendations(song_name)
    return render_template('recommendations.html', song_name=song_name, recommendations=recommendations)
if __name__ == '__main__':
    app.run(debug=True)