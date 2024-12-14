import requests
import subprocess
import time
from twilio.rest import Client



# Function to get the ngrok URL
def get_ngrok_url():
    try:
        # Fetch the tunnels from the ngrok API
        response = requests.get('http://127.0.0.1:4040/api/tunnels')
        data = response.json()

        # Extract the public URL
        url = data['tunnels'][0]['public_url']
        return url
    except Exception as e:
        print(f"Error fetching ngrok URL: {e}")
        return None

# Function to send the URL via WhatsApp
def send_whatsapp_message(ngrok_url):
    # Twilio credentials
    account_sid = "AC9400f9908d04610268bc0661a644c6ae"  # Replace with your Account SID
    auth_token = "3cdd592d45a4fa8daa09a4c786fbe460"   # Replace with your Auth Token
    from_whatsapp_number = "whatsapp:+14155238886"  # Twilio Sandbox WhatsApp number
    to_whatsapp_number = "whatsapp:+918389967188"  # Your verified phone number

    client = Client(account_sid, auth_token)
    message_body = f"Your ngrok URL is: {ngrok_url}"

    try:
        message = client.messages.create(
            body=message_body,
            from_=from_whatsapp_number,
            to=to_whatsapp_number,
        )
        print(f"Message sent successfully! SID: {message.sid}")
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")

# Main script
if __name__ == "__main__":
    print("Waiting for ngrok to initialize...")
    ngrok_url = get_ngrok_url()
    
    if ngrok_url:
        print(f"Ngrok URL: {ngrok_url}")
        send_whatsapp_message(ngrok_url)
    else:
        print("Failed to fetch ngrok URL.")
