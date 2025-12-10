import requests
import os


ACCESS_TOKEN = "EAAVFytjDZC30BQBgmsqlsBZBGX2WrEGtJwRJV1vIpAMAZCTzaDTv347cOROqrMC93iZBOfbTId0UB7i1Bx5FT4hG0CuEAvKv7ElpZCcyELtdKZBWvQyPhTE4VGnZBa9eVjEEBKhUJKaBoCXUrZBfFhMEwXMvFD6wZAmz77SxtX2IbFkBAnAk6zkRN8WUqmZBwsMqFjv3UIKkxSpbdy4315eU1mvHW2DjXvOzGKXNW2zogPNmaCsgRNjJtK1jnmOr55zsbZALlRr4xZChOAAnb8p8ZA0xBQ5ZA0"
PHONE_NUMBER_ID = "773981995803524"

def send_whatsapp_document(user_number, file_path):
    file_path = os.path.abspath(file_path)
    # 1. Upload file
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/media"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    files = {
        "file": (file_path, open(file_path, "rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    }

    data = {
        "messaging_product": "whatsapp",
        "type": "document"
    }

    upload_res = requests.post(url, headers=headers, files=files, data=data).json()
    media_id = upload_res.get("id")

    print("MEDIA UPLOAD RESULT:", upload_res)

    if media_id is None:
        print("UPLOAD FAILED")
        return

    # 2. Send document to teacher
    message_url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    msg_data = {
        "messaging_product": "whatsapp",
        "to": user_number,
        "type": "document",
        "document": {
            "id": media_id,
            "filename": "attendance.csv"
        }
    }

    msg_res = requests.post(message_url, headers=headers, json=msg_data).json()
    print("MESSAGE SEND RESULT:", msg_res)
