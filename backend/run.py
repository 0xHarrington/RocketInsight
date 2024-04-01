from flask import Flask
from app.api import api

# Create the Flask application instance
app = Flask(__name__)

# Register the Blueprint with the Flask application
app.register_blueprint(api, url_prefix='/api')

# Optionally, you can configure the host and port in the run configuration
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
