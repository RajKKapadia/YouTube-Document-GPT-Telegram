from flask import Flask, request

from document_gpt.helper.utils import process_telegram_data, generate_text_response, generate_file_response
from document_gpt.helper.telegram_api import send_message, set_webhook, set_menu_commands


app = Flask(__name__)


@app.route('/')
def home():
    return 'All is well...'


@app.route('/telegram', methods=['POST'])
def telegram_api():
    if request.is_json:
        data = request.get_json()
        print(data)
        try:
            telegram_data = process_telegram_data(data)
            if telegram_data['is_unknown']:
                return 'OK', 200
            if telegram_data['is_text']:
                response = generate_text_response(telegram_data['text'])
                send_message(telegram_data['sender_id'], response)
                return 'OK', 200
            if telegram_data['is_document']:
                response = generate_file_response(
                    telegram_data['file_id'], telegram_data['mime_type'], telegram_data['sender_id'])
                send_message(telegram_data['sender_id'], response)
                return 'OK', 200
        except:
            pass
        return 'OK', 200


@app.route('/set-telegram-webhook', methods=['POST'])
def set_telegram_webhook():
    if request.is_json:
        body = request.get_json()
        flag = set_webhook(body['url'], body['secret_token'])
        if flag:
            return 'OK', 200
        else:
            return 'BAD REQUEST', 400
    else:
        return 'BAD REQUEST', 400


@app.route('/set-telegram-menu-commands', methods=['POST'])
def set_telegram_menu_commands():
    if request.is_json:
        body = request.get_json()
        flag = set_menu_commands(body['commands'])
        if flag:
            return 'OK', 200
        else:
            return 'BAD REQUEST', 400
    else:
        return 'BAD REQUEST', 400
