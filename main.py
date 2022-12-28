from flask import Flask
from app import create_app
from dotenv import load_dotenv,find_dotenv
import os
load_dotenv(find_dotenv())
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True,port=8080)
