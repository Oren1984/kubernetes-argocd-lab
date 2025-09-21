# Simple Flask application for ArgoCD lab
# Returns a JSON message on the root endpoint

from flask import Flask
import os

app = Flask(__name__)

@app.get("/")
def hello():
    return {"message": "Hello from ArgoCD lab!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
