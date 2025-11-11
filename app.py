from flask import Flask, render_template
from flask_restful import Api
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

api = Api(app)

@app.route('/')
def frontend_home():
    return render_template('index.html')

from routes import *

if __name__ == '__main__':
    app.run(port=6209, debug=True, host='0.0.0.0')