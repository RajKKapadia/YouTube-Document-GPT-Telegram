import os

from document_gpt.helper.telegram_api import get_file_path, save_file_and_get_local_path, send_message
from document_gpt.helper.conversation import create_conversation
from document_gpt.helper.create_index import create_index

qa = create_conversation()


def process_telegram_data(data: dict) -> dict:

    is_text = False
    is_document = False
    is_unknown = True

    sender_id = ''
    text = ''
    file_id = ''
    mime_type = ''

    if 'message' in data.keys():
        message = data['message']
        sender_id = message['from']['id']
        if 'text' in message.keys():
            text = message['text']
            is_text = True
            is_unknown = False
        if 'document' in message.keys():
            file_id = message['document']['file_id']
            mime_type = message['document']['mime_type']
            is_document = True
            is_unknown = False

    return {
        'is_text': is_text,
        'is_document': is_document,
        'is_unknown': is_unknown,
        'sender_id': sender_id,
        'text': text,
        'file_id': file_id,
        'mime_type': mime_type
    }


def generate_text_response(text: str) -> str:

    if text == '/start':
        return 'Hi, I can help you with saving your data to the cloud and retive it, I can also help you with your questions.'
    if text == '/file':
        return 'Select the pdf document file that you want to query.'
    if text == '/help':
        return 'I am an AI and I am here to help you. You can upload PDF files and once uploaded, you can query them.'

    '''TODO
    We can add chat_history here...
    Save all the messages in a DB
    Retrive when this function is called
    Create chat_history variable and pass it in the qa 
    '''

    result = qa(
        {
            'question': text,
            'chat_history': {}
        }
    )

    try:
        return result['answer']
    except:
        return 'We are facing some technical issue.'


def generate_file_response(file_id: str, mime_type: str, sender_id: str) -> str:

    if 'pdf' not in mime_type:
        return 'The bot can only understand PDF files at this moment.'

    file_path = get_file_path(file_id)

    if file_path['status'] == 1:
        local_file_path = save_file_and_get_local_path(file_path['file_path'])

        if local_file_path['status'] == 1:
            try:
                send_message(sender_id, 'Processing the file and generating the knowledge...')
                create_index(local_file_path['local_file_path'])
                os.unlink(local_file_path['local_file_path'])
                return 'File saved successfully.'
            except:
                return 'We are facing some technical issue at saving the file.'
