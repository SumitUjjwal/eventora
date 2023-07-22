
import os
from flask import Flask
from dotenv import load_dotenv
from routes.authRouter import auth
from routes.userRouter import user
from routes.venueRouter import venue
from routes.eventRouter import event
from middlewares.authenticator import token_required

# Environement variables
load_dotenv()
PORT = os.getenv('PORT')


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'Welcome to Eventora!'

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(venue, url_prefix='/venue')
app.register_blueprint(event, url_prefix='/event')

if __name__ == '__main__':
    app.run(debug=True)