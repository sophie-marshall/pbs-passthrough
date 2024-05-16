from flask import Flask
from routes import home, about, passthrough, demo, facial_recognition, query

app = Flask(__name__)

# Registering blueprints for routes
app.register_blueprint(home.bp)
app.register_blueprint(about.bp)
app.register_blueprint(passthrough.bp)
app.register_blueprint(demo.bp)
app.register_blueprint(facial_recognition.bp)
app.register_blueprint(query.bp)

if __name__ == "__main__":
    app.run(debug=True)