from flask import Flask
from app import create_app
from dotenv import load_dotenv
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True, port=5000)
    load_dotenv()
