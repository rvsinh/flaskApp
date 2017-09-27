#app __init_file

from flask import Flask

#Intialise the application

app = Flask(__name__, instance_relative_config=True)


#Load the view

from app import views

# Load the config file

app.config.from_object('config')
