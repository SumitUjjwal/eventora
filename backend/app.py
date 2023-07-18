
import os
from flask import Flask
from dotenv import load_dotenv

# Environement variables
load_dotenv()
PORT = os.getenv('PORT')


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'Welcome to Eventora!'

if __name__ == '__main__':
    app.run(debug=True)