import http.server
import socketserver
import os
import urllib.parse
import socket
import threading
from datetime import datetime

# --- КОНФИГУРАЦИЯ ---
PORT = 3646
LOG_FILE = ".DATA_CHAT.txt" 
ANDROID_ROOT = os.path.abspath(os.path.dirname(__file__)) if __file__ else os.getcwd()

if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        chat_messages = f.readlines()
else:
    chat_messages = []

class ThreadingHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

class IIA_Ultimate_Handler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        # /chat теперь — это "свернутое" состояние (главная)
        if self.path == "/chat" or self.path == "/":
            self.show_main_interface()
        # /chat_inter — это "развернутый" чат
        elif self.path == "/chat_inter":
            self.show_chat_inter()
        elif self.path == "/menu":
            self.show_menu()
        elif self.path == "/storage":
            self.path = "/"
            return super().do_GET()
        elif self.path.startswith("/search"):
            self.show_search()
        else:
            return super().do_GET()

    def do_POST(self):
        if self.path == "/send":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = urllib.parse.parse_qs(post_data)
            
            user_name = params.get('name', ['Пользователь'])[0]
            user_msg = params.get('msg', [''])[0]
            time_now = datetime.now().strftime("%H:%M")
            
            if user_msg:
                full_msg = f"[{time_now}] <b>{user_name}:</b> {user_msg}\n"
                chat_messages.append(full_msg)
                
                with open(LOG_FILE, "a", encoding="utf-8") as f:
                    f.write(full_msg)
                
                if len(chat_messages) > 2000: chat_messages.pop(0)

            # --- ИСПРАВЛЕНИЕ ТУТ ---
            # Перенаправляем обратно в ИНТЕРФЕЙС чата, а не на главную
            self.send_response(303)
            self.send_header("Location", "/chat") 
            self.end_headers()

    def show_main_interface(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        html = f"""
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>|NWS_959.DIRECT|</title>
            <style>
                body {{ font-family: sans-serif; background: black; color: #3C00D4; margin: 0; display: flex; align-items: center; justify-content: center; height: 100vh; }}
                .container {{ text-align: center; background: black; padding: 30px; border-radius: 15px;  width: 90%; max-width: 400px; }}
                h1 {{ color: #5300CB; font-size: 28px; margin-bottom: 5px; }}
                h2 {{ color: #0029FF; font-size: 16px; margin-bottom: 30px; }}
                .btn {{
                    display: block; 
                    padding: 15px; 
                    background: black; 
                    color: #4A00FF; 
                    text-decoration: none; 
                    border: 1px solid black; 
                    border-radius: 5px; 
                    margin: 10px 0; 
                    font-weight: bold;
                }}
                .chat-open {{ background: black; border-color: black; }}
            </style>
        </head>
        <body>
        <div style="border-top: 2px solid #161616;">
        <div style="background: rgba(39,39,39, 0.2);">
            <div class="container">
                <h1>▶__NWS_959_SERVER__◀</h1>
                <h2>≤----[V:10.3.9] [FAST]----≥</h2><br><br>
                <a href="/chat_inter" class="btn chat-open"> ▶   ____[@]-[CHAT]____   ◀</a>
                <a href="/menu" class="btn"> ▶   ____[;]-[MENU]____   ◀</a>
                <a href="/storage" class="btn"> ▶   ____[/]-[STORAGE]____   ◀</a>
                <a href="javascript:void(0);" onclick="window.location.reload();" class="btn" style="background: black; border: 1px solid black;"> ▶   ____[*]-[RESET]____   ◀</a>
            </div>
            </div>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    def show_chat_inter(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        messages_html = "".join([f"<div style='border-bottom:1px solid black; padding:8px;'> {m}</div>" for m in chat_messages])
        
        html = f"""
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>|CHAT|</title>
            <style>
                body {{ font-family: sans-serif; background: black; color: #4900FF; margin: 0; }}
                .chat-container {{ max-width: 600px; margin: auto; display: flex; flex-direction: column; height: 100vh; }}
                .header {{ background: black; padding: 10px; border-bottom: 2px solid blue; display: flex; justify-content: space-between; align-items: center; }}
                .messages {{ flex-grow: 1; overflow-y: auto; background: #222; padding: 10px; font-size: 14px; }}
                .footer {{ background: black; padding: 10px; border-top: 1px solid #101010; }}
                input[type="text"] {{ width: 100%; padding: 12px; margin-bottom: 8px; border-radius: 5px; border: none; background: #444; color: white; box-sizing: border-box; }}
                .btn-row {{ display: flex; gap: 5px; }}
                .send-btn {{ flex-grow: 2; background: black; color: blue; border: none; padding: 10px; border-radius: 3px; font-weight: bold; cursor: pointer; }}
                .fold-btn {{ background: black; color: blue; text-decoration: none; padding: 10px 15px; border-radius: 3px; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="chat-container">
                <div class="header">
                    <span style="color:#5B0BFF; font-weight:bold;">@ CHAT:</span>
                    <a href="javascript:void(0);" onclick="window.location.reload();" class="fold-btn">[*] RESET</a>
                    <a href="/chat" class="fold-btn">[×] HOME</a>

                
                </div>
                <div class="messages" id="msg_box">{messages_html}</div>
                <div class="footer">
                    <form action="/send" method="post">
                        <input type="text" name="name" placeholder="▶/NIKNAME:____" maxlength="10">
                        <input type="text" name="msg" placeholder="▶/TEXT:____" required autofocus>
                        <div class="btn-row">
                            <input type="submit" class="send-btn" value="« ENTER [>]»">
                        </div>
                    </form>
                </div>
            </div>
            <script>
                // Авто-прокрутка вниз при загрузке
                var objDiv = document.getElementById("msg_box");
                objDiv.scrollTop = objDiv.scrollHeight;
            </script>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    def show_menu(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        html = f"""
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>|NWS_959 MENU LIST|</title>
            <style>
                body {{ font-family: sans-serif; background: black; color: #4A09FF; }}
                .container {{ max-width: 500px; margin: auto; background: black; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #171717;}}
                .btn {{ display: block; padding: 12px; background: #171717; color: #5A00FF; text-decoration: none; border: 1px solid #161616; border-radius: 3px; margin: 8px 0; }}
                input[type="text"] {{ width: 80%; padding: 10px; border-radius: 5px; border: none; }}
            </style>
        </head>
        <body>
        
            <div class="container">
                <h2 style="color: #393939; background: none; border: 1px solid #171717;"> » [MENU]:</h2>
                <form action="/search" method="get">
                    <input type="text" name="q" placeholder="Поиск файлов на сервере...">
                    <input type="submit" value="»" style="padding:10px; background: black; border: 1px solid #393939;">
                </form>
                <br>
                <p>▶ [#] [NWS_959]: ◀ </p>
                <a style="border: 1px solid blue; background: #161616;" href="/chat" class="btn" > [×] |HOME_LIST| </a>
                <a  style="border: 1px solid blue;" href="/storage" class="btn"> [/] |SERVER_STORAGE|</a>
                <br>
                <hr>
                <p>▶ [/_] [PROGRAMMS]: ◀</p>
                <p style="color:blue"> [▶Apps◀]: </p>
                <a  style="border: 1px solid blue;" href="{Desktop_UI}.htm" class="btn">[_] ▶|SHINKOR_WebOS|◀</a>
                <br>
                <hr>
                <p style="color:#D2D2D2;  border: 1px solid #555;"> ▶ [->] [INTERNET]: ◀ </p>
                <p style="color:blue"> [▶Online◀]: </p>
                <div style="display: flex; justify-content: space-around; flex-wrap: wrap; background: #303030; color: white; border: 2px solid blue;">
                    <a style="border: 1px solid blue; width: 40%;" href="https://www.google.com" class="btn">[🌐] Google</a>
                    <a style="border: 1px solid blue; width: 40%;" href="https://ya.ru" class="btn">[🌍] Yandex</a>
                    <a style="border: 1px solid blue; width: 40%;" href="https://web.telegram.org/k/" class="btn">[💬] Telegram</a>
                    <a style="border: 1px solid blue; width: 40%;" href="https://alice.yandex.ru/chat/" class="btn">[🎭] Alice</a>
                    <a style="border: 1px solid blue; width: 40%;" href="https://apkpure.com/" class="btn">[💽] Apkpure</a>
                    <a style="border: 1px solid blue; width: 40%;" href="https://www.instagram.com/?utm_source=op_m_sd" class="btn">[📷] Instagram</a>
                    <a style="border: 1px solid blue; width: 40%;" href="https://call2friends.com/free-calls" class="btn">[☎] Телефон</a>
                    <a style="border: 1px solid blue; width: 40%;" href="https://mail.google.com/mail/?authuser=0" class="btn">[✉] Gmail</a>
                    <a style="border: 1px solid blue; width: 40%;" href="http://chatbotchatapp.com/" class="btn">[💭] Chat GPT </a>
                    <a style="border: 1px solid blue; width: 40%;" href="https://yandex.ru/pogoda/65?lat=55.030199&lon=82.92043&utm_campaign=informer&utm_content=main_informer&utm_medium=web&utm_source=home" class="btn">[🌦] Погода</a>
                </div>
                <p style="color:#187754"> |▶     END     ◀|
            </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    def show_search(self):
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get('q', [''])[0].lower()
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        results = []
        if query:
            for root, dirs, files in os.walk(ANDROID_ROOT):
                for name in files:
                    if query in name.lower():
                        rel_path = os.path.relpath(os.path.join(root, name), ANDROID_ROOT)
                        results.append(f"<li><a style='color:blue' href='/{rel_path}'>{rel_path}</a></li>")
        res_html = "".join(results) if results else "[×] [Ничего не найдено по вашему запросу]"
        html = f"<html><body style='background:black; color:#00D2BB;'><div style='padding:20px;'><h2>RESULT: {query}</h2><ul>{res_html}</ul><br><a href='/menu' style='color:white'>[⤴] [Назад в меню]</a></div></body></html>"
        self.wfile.write(html.encode('utf-8'))

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except: ip = "127.0.0.1"
    finally: s.close()
    return ip

local_ip = get_ip()
print()
print("_"*59)
print(f"            [/_] \|SERVER_CONTROL_LIST|/")
print("="*59)
print(f"                  NWS_959 SGO STATUS: ")
print(f"[i] HTTP_HOME.LIST.URL: http://{local_ip}:{PORT}/chat")
print(f"[i] SERVER_LINK_STATUS: ON")
print(f"[i] SERVER_NAME: |NWS_959 SGO|")
print(f"[i] LOCAL_INTRANET: ON")
print(f"[i] TYPE_LINK: INTRANET")
print("="*59)
print(' ')
print("="*59)
print(f"          [#] \|Свойства NWS_959 GO сервера:|/")
print("_"*59)
print(f"[/] IP-АДРЕС СЕРВЕРА: {local_ip}")
print(f"[/] ПОРТ СЕРВЕРА:               {PORT}")
print(f"[i] СТАТИЧНЫЙ IP-АДРЕС СЕРВЕРА: 127.0.0.1 ")
print(f"[_] ССЫЛКА НА ГЛАВНУЮ СТРАНИЦУ: http://{local_ip}:{PORT}/chat")
print(f"[_] ССЫЛКА НА ДИСК СЕРВЕРА:  http://{local_ip}:{PORT}/storage")
print(f"[_] ССЫЛКА НА ЧАТ СЕРВЕРА:  http://{local_ip}:{PORT}/chat_inter")
print(f"[_] ССЫЛКА НА МЕНЮ СЕРВЕРА:   http://{local_ip}:{PORT}/menu")
print("_"*59)
print(f"[?] |ПАРАМЕТРЫ СЕРВЕРА В СЕТИ: IP={local_ip}, PORT={PORT}|")
print("="*59)
print("   |V| [!] Действия на сервере в настоящее время: |V| ")
print(' ')


try:
    with ThreadingHTTPServer(("", PORT), IIA_Ultimate_Handler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n> [!] [Сервер остановлен]")
