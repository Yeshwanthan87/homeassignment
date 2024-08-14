from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def get_public_ip():
    ip = requests.get('https://api.ipify.org').text
    return f'Your Public IP is: {ip} and that is a project for BIGID bigwebhooktest'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

