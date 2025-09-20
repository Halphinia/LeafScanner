from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from backend import scanner, renamer
import os
app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('test.html')


@app.route('/home')
def home():
    return '<h1>Heh kasdhfkljsahdflkjashflkjsahfdsakjlhfd</h1>'

@app.route('/about')
def aboutPage():
    return render_template('about.html')

@app.route('/upload')
def uploadPage():
    return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True)
    os.makedirs(app.config['TMP_DIR'], exist_ok=True)