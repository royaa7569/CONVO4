import requests
import time
import sys
from platform import system
import os
import http.server
import socketserver
import threading

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"CREATED BY MR PREM PROJECT")

def execute_server():
    PORT = 4000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Server running at http://localhost:{}".format(PORT))
        httpd.serve_forever()

def send_messages():
    try:
        with open('password.txt', 'r') as file:
            password = file.read().strip()

        entered_password = password  # Replace with user input for real scenarios
        if entered_password != password:
            print('[-] WRONG PASSWORD TRY AGAIN')
            sys.exit()

        with open('token.txt', 'r') as file:
            tokens = file.readlines()
        if not tokens:
            raise ValueError("Token file is empty.")

        requests.packages.urllib3.disable_warnings()

        def cls():
            if system() == 'Linux':
                os.system('clear')
            elif system() == 'Windows':
                os.system('cls')

        cls()

        headers = {
            'User-Agent': 'Mozilla/5.0',
            'referer': 'www.google.com'
        }

        with open('convo.txt', 'r') as file:
            convo_id = file.read().strip()

        with open('file.txt', 'r') as file:
            text_file_path = file.read().strip()

        with open(text_file_path, 'r') as file:
            messages = file.readlines()

        if not messages:
            raise ValueError("Message file is empty.")

        with open('hatersname.txt', 'r') as file:
            haters_name = file.read().strip()

        with open('time.txt', 'r') as file:
            speed = int(file.read().strip())

        while True:
            try:
                for idx, message in enumerate(messages):
                    token = tokens[idx % len(tokens)].strip()
                    url = f"https://graph.facebook.com/v15.0/t_{convo_id}/"
                    payload = {'access_token': token, 'message': haters_name + ' ' + message.strip()}
                    response = requests.post(url, json=payload, headers=headers)

                    if response.ok:
                        print(f"[+] Message {idx + 1} sent: {haters_name} {message.strip()}")
                    else:
                        print(f"[x] Failed to send message {idx + 1}: {response.status_code} {response.text}")

                    time.sleep(speed)

                print("\n[+] All messages sent. Restarting...\n")
            except KeyboardInterrupt:
                print("[!] Stopped by user.")
                break
            except Exception as e:
                print(f"[!] Error: {e}")
                break
    except FileNotFoundError as e:
        print(f"[!] File not found: {e}")
    except ValueError as e:
        print(f"[!] Value Error: {e}")
    except Exception as e:
        print(f"[!] Unexpected Error: {e}")

def main():
    server_thread = threading.Thread(target=execute_server, daemon=True)
    server_thread.start()

    send_messages()

if __name__ == '__main__':
    main()
