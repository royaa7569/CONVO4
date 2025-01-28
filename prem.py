import requests
import time
import sys
from platform import system
import os
import http.server
import socketserver
import threading
import json

# HTTP Server Handler
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"CREATER BY MR PREM PROJECT")

# Server Execution
def execute_server():
    PORT = 4000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Server running at http://localhost:{}".format(PORT))
        httpd.serve_forever()

# Offline Queue Handler
def load_queue():
    if os.path.exists('offline_queue.json'):
        with open('offline_queue.json', 'r') as file:
            return json.load(file)
    return []

def save_queue(queue):
    with open('offline_queue.json', 'w') as file:
        json.dump(queue, file)

def send_messages():
    # Password Verification
    with open('password.txt', 'r') as file:
        password = file.read().strip()
    
    entered_password = password
    if entered_password != password:
        print('[-] WRONG PASSWORD TRY AGAIN')
        sys.exit()

    # Token Loading
    with open('token.txt', 'r') as file:
        tokens = [token.strip() for token in file.readlines()]
    num_tokens = len(tokens)

    requests.packages.urllib3.disable_warnings()

    # Console Clear Function
    def cls():
        if system() == 'Linux':
            os.system('clear')
        elif system() == 'Windows':
            os.system('cls')

    cls()

    # Line Separator
    def liness():
        print('\u001b[37m' + '---------------------------------------------------')

    # Headers for HTTP Request
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
        'referer': 'www.google.com'
    }

    # Validate Password Online (Optional)
    mmm = requests.get('https://pastebin.com/raw/TcQPZaW8').text
    if mmm not in password:
        print('[-] WRONG PASSWORD TRY AGAIN')
        sys.exit()

    liness()

    # Load Conversation, Messages, and Parameters
    with open('convo.txt', 'r') as file:
        convo_id = file.read().strip()

    with open('file.txt', 'r') as file:
        text_file_path = file.read().strip()

    with open(text_file_path, 'r') as file:
        messages = [msg.strip() for msg in file.readlines()]

    with open('hatersname.txt', 'r') as file:
        haters_name = file.read().strip()

    with open('time.txt', 'r') as file:
        try:
            speed = int(file.read().strip())
        except ValueError:
            speed = 5  # Default speed if invalid value

    # Load Offline Queue
    queue = load_queue()

    while True:
        try:
            # Send Pending Messages from Queue
            if queue:
                print("[*] Sending offline queued messages...")
                for message_data in queue[:]:  # Use a copy of the list to modify safely
                    try:
                        response = requests.post(message_data['url'], json=message_data['parameters'], headers=headers)
                        if response.ok:
                            print(f"[+] Offline Message Sent: {message_data['parameters']['message']}")
                            queue.remove(message_data)  # Remove from queue if successful
                            save_queue(queue)  # Save updated queue
                        else:
                            print("[x] Failed to send offline message")
                    except requests.exceptions.RequestException:
                        print("[!] Unable to send offline message (No Internet)")
                        break  # Exit loop if offline

            # Send New Messages
            for i, message in enumerate(messages):
                token_index = i % num_tokens
                access_token = tokens[token_index]

                url = f"https://graph.facebook.com/v15.0/t_{convo_id}/"
                parameters = {'access_token': access_token, 'message': f"{haters_name} {message}"}

                try:
                    response = requests.post(url, json=parameters, headers=headers)
                    if response.ok:
                        print(f"[+] Message Sent: {haters_name} {message}")
                    else:
                        print(f"[x] Failed to send message: {haters_name} {message}")
                except requests.exceptions.RequestException:
                    print("[!] Offline Mode: Storing message in queue")
                    queue.append({'url': url, 'parameters': parameters})
                    save_queue(queue)  # Save queue to file

                time.sleep(speed)

        except Exception as e:
            print(f"[!] Error: {e}")

        print("\n[+] Restarting the process...\n")

def main():
    # Start HTTP Server in a Thread
    server_thread = threading.Thread(target=execute_server, daemon=True)
    server_thread.start()

    # Run Message Sending
    send_messages()

if __name__ == '__main__':
    main()
