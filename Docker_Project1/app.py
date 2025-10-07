from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import logging
import os
import redis
import json
import socket

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    filename='flask_app.log',      # Log file path
    level=logging.DEBUG,            # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s %(levelname)s: %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Get the database URL from environment variable
db_password = ''
with open("/run/secrets/postgres_password") as f:
    db_password = f.read().strip()

db_user = os.getenv("POSTGRES_USER", "postgres")
db_service = os.getenv("POSTGRES_SERVICE", "db")
db_database = os.getenv("POSTGRES_DB", "db")
db_url = "postgresql://{user}:{password}@{service}:5432/{db}".format(user=db_user, password=db_password, service=db_service, db=db_database)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
cache = redis.from_url(redis_url)

# Get env variable for app environment from .env file
load_dotenv()
environment = os.getenv("ENVIRONMENT", "development")
app.logger.info(f"Environment: {environment}")

debug = os.getenv("DEBUG", "false")


# Example model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    hostname = socket.gethostname()
    return "Flask + PostgreSQL is working! Host: {}".format(hostname)

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/users")
def get_users():
    cached = cache.get("users")
    if cached:
        app.logger.info("Cached")
        return cached, 200, {"Content-Type": "application/json"}  # Return cached JSON

    users = User.query.all()
    users_list = [{"id": u.id, "name": u.name} for u in users]
    users_json = json.dumps(users_list)

    # Cache for 120 seconds
    cache.setex("users", 120, users_json)
    return users_json, 200, {"Content-Type": "application/json"}

@app.route("/add/<name>")
def add_user(name):
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    cache.delete("users")
    return f"Added user {name}!"

if __name__ == "__main__":
    # Also log when the app starts
    app.logger.info("Starting Flask app...")
    app.run(debug=debug, port=5000, host='0.0.0.0')
