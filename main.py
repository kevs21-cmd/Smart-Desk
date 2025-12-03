from website import create_app


from flask import Flask
app = Flask(__name__, static_foldre='static')

app = create_app()
