from flask import *
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html', name='Hello')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
