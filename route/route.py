from flask import Flask,Response, render_template
from controller import app_control
from dotenv import load_dotenv

env_path='../.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

def app_test():
    # return Response('Welcome to xVector!')
    return render_template('xvector_base.html')

app.add_url_rule('/',view_func=app_test,methods=['GET'])
app.add_url_rule('/dataset',view_func=app_control.store_data,methods=['POST'])
app.add_url_rule('/dataset',view_func=app_control.list_data,methods=['GET'])
app.add_url_rule('/dataset/<data_name>/compute',view_func=app_control.compute_data,methods=['POST'])
app.add_url_rule('/dataset/<data_name>/plot',view_func=app_control.plot_data,methods=['GET'])