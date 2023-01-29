from flask import Flask
from utils import *

# Create app object
app = Flask(__name__)

# Set configs
app.config.from_object('config.Config')

from views import *

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')