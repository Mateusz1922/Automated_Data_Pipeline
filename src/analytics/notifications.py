import requests
import logging

class TelegramNotifier:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
    
    def send_message(self, message):
        if not self.token or not self.chat_id:
            logging.error("Telegram Token or Chat ID is missing! Check your .env file.")
            return
        
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id, 
            "text": message, 
            "parse_mode": "HTML"
        }
        try:
            response = requests.post(url, json=payload)
            # if status not 200, raise error
            if response.status_code != 200:
                logging.error(f"Telegram Rejected: {response.text}")
            response.raise_for_status() 
            logging.info("Telegram notification sent successfully.")
        except requests.exceptions.HTTPError as e:
            # Here response from Telegram (e.g. "Unauthorized" or "Chat not found")
            logging.error(f"Telegram API Error: {response.text}")
        except Exception as e:
            logging.error(f"Unexpected error sending Telegram message: {e}")
    