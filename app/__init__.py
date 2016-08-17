from flask import Flask

# This is the path to the upload directory
UPLOAD_FOLDER = 'tmp'
# These are the extension that we are accepting to be uploaded
ALLOWED_EXTENSIONS = set(['tcx'])

# Initialize the Flask application
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

from app import views
