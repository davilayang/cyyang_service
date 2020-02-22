# app.__init__
# import os
# from flask import Flask, request
# from flask_sqlalchemy import SQLAlchemy
# from dotenv import load_dotenv
# from pathlib import Path

# # Define WSGI object
# app = Flask(__name__)

# # Get Environment Variables
# # env_path = Path('.') / '.env' # ./.env
# # load_dotenv(verbose=True, dotenv_path=env_path)

# # Configurations
# app.config.from_object('app.config.Config') 



# Development Setting
# app.config.from_object(os.environ['APP_SETTINGS']) # add settings variable from current env
# app.config.from_object(os.getenv('APP_SETTINGS')) # add settings variable with load_dotenv

# Database Configurations
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # add URI variable from current env
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Define SQLAlchemy object
# db = SQLAlchemy(app)







