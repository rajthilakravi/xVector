import os
from flask import Flask, url_for, request, Response
from route.route import app
from dotenv import load_dotenv
env_path='.env'
load_dotenv(dotenv_path=env_path)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
if __name__ == '__main__':
    #port and host
    app.config.setdefault('LOG_REQUEST_ID_GENERATE_IF_NOT_FOUND', True)
    app.config.setdefault('LOG_REQUEST_ID_LOG_ALL_REQUESTS', False)
    app.config.setdefault('LOG_REQUEST_ID_G_OBJECT_ATTRIBUTE', 'log_request_id')
    COMPRESS_MIMETYPES = ['text/html','text/css','applictaion/json']
    app.run(host='0.0.0.0',port = os.getenv("PORT"),debug=False)