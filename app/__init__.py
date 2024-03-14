from flask import Flask,flash
from app.main.index import main as main
from app.main.excel import excel as excel
from app.main.schedule import schedule as schedule

app = Flask(__name__)
app.secret_key='musinsamanagerSever'
app.register_blueprint(main)
app.register_blueprint(excel)
app.register_blueprint(schedule)

