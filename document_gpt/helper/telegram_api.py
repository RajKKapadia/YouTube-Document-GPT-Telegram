import os
import json
from typing import List
import tempfile
import uuid

import requests

from config import config

BASE_URL = f'https://api.telegram.org/bot{config.TELEGRAM_TOKEN}'


def send_message(chat_id: int, message: str) -> bool:
    '''
    Send message to a Telegram user.

    Parameters:
        - chat_id(int): chat id of the user
        - message(str): text message to send

    Returns:
        - bool: either 0 for error or 1 for success 
    '''

    payload = {
        'chat_id': chat_id,
        'text': message
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.request(
        'POST', f'{BASE_URL}/sendMessage', json=payload, headers=headers)
    status_code = response.status_code
    response = json.loads(response.text)

    if status_code == 200 and response['ok']:
        return True
    else:
        return False


def send_photo(chat_id: int, url: str, caption: str = '') -> bool:
    '''
    Send a photo to a Telegram user.

    Parameters:
        - chat_id(int): chat id of the user
        - url(str): photo url

    Returns:
        - bool: either 0 for error or 1 for success 
    '''

    payload = {
        'chat_id': chat_id,
        'photo': url
    }

    if caption != '':
        payload['caption'] = caption

    headers = {'Content-Type': 'application/json'}

    response = requests.request(
        'POST', f'{BASE_URL}/sendPhoto', json=payload, headers=headers)
    status_code = response.status_code
    response = json.loads(response.text)

    if status_code == 200 and response['ok']:
        return True
    else:
        return False


def set_webhook(url: str, secret_token: str = '') -> bool:
    '''
    Set a url as a webhook to receive all incoming messages

    Parameters:
        - url(str): url as a webhook
        - secret_token(str)(Optional): you will receive this secret token from Telegram request as X-Telegram-Bot-Api-Secret-Token

    Returns:
        - bool: either 0 for error or 1 for success
    '''

    payload = {'url': url}

    if secret_token != '':
        payload['secret_token'] = secret_token

    headers = {'Content-Type': 'application/json'}

    response = requests.request(
        'POST', f'{BASE_URL}/setWebhook', json=payload, headers=headers)
    status_code = response.status_code
    response = json.loads(response.text)

    if status_code == 200 and response['ok']:
        return True
    else:
        return False


def set_menu_commands(commands: List[dict]) -> bool:
    '''
    Set a menu commands in the Telegram bot

    Parameters:
        - commands(List[dict]): commands is a list of objects, each object must have two properties command and description
        where command is postback to Telegram, while description explains the command to the user

    Returns:
        - bool: either 0 for error or 1 for success
    '''

    payload = {'commands': commands}

    headers = {'Content-Type': 'application/json'}

    response = requests.request(
        'POST', f'{BASE_URL}/setMyCommands', json=payload, headers=headers)
    status_code = response.status_code
    response = json.loads(response.text)

    if status_code == 200 and response['ok']:
        return True
    else:
        return False

def get_file_path(file_id: str) -> dict:
    '''
    Get the file path from the file id of the attachement

    Parameters:
        - file_id(str): file id of the attachement
    
    Returns:
        - dict of status and file path of the attachment
    '''

    url = f'https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/getFile'
    querystring = {'file_id': file_id}
    response = requests.request('GET', url, params=querystring)
    
    if response.status_code == 200:
        data = json.loads(response.text)
        file_path = data['result']['file_path']

        return {
            'status': 1,
            'file_path': file_path
        }
    else:
        return {
            'status': 0,
            'file_path': ''
        }

def save_file_and_get_local_path(file_path: str) -> dict:
    '''
    Save the file and get the local file path

    Parameters:
        - file_path(str): file path of the attachment

    Returns:
        - dict of status and the local file path of the attchment
    '''

    url = f'https://api.telegram.org/file/bot{config.TELEGRAM_TOKEN}/{file_path}'
    response = requests.request('GET', url)
    TMP_DIR = tempfile.gettempdir()
    extention = file_path.split('.')[-1]
    file_name = f'{uuid.uuid1()}.{extention}'
    local_file_path = os.path.join(
        TMP_DIR,
        file_name
    )

    if response.status_code == 200:
        with open(local_file_path, 'wb') as file:
            file.write(response.content)

        return {
            'status': 1,
            'local_file_path': local_file_path,
            'file_name': file_name,
            'extension': extention
        }
    else:
        return {
            'status': 0,
            'local_file_path': '',
            'file_name': '',
            'extension': ''
        }
        