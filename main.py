from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from backend import scanner, renamer
import os
app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
@app.route('/home')
def index():
    return render_template('test.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def aboutPage():
    return render_template('about.html')

@app.route('/upload', methods=['GET','POST'])
def uploadPage():
    if request.method == "POST":
        files = request.files.getlist("files")
        if not files or all(f.filename == "" for f in files):
            return render_template("errorPage.html")
        saved = []
        for f in files:
            if f and f.filename:
                saved.append(f.filename)
        scanner.imageLoader(saved)
        return render_template("processing.html")
    else:
        return render_template('upload.html')

if __name__ == "__main__":
    app.run(debug=True)
    os.makedirs(app.config['TMP_DIR'], exist_ok=True)