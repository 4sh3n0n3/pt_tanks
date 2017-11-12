import socket


class Server:
    def __init__(self, PORT):
        self.HOST = ''
        self.PORT = PORT

    def make_socket(self):
        if self.PORT == '':
            self.PORT = 9090
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.HOST, self.PORT))
        s.listen(1)
        print("ожидаем подключения")
        conn, addr = s.accept()
        conn.setblocking(0)
        print("подключение установлено")
        return conn


class Client:
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT

    def make_socket(self):
        if self.PORT == '':
            self.PORT = 9090
        if self.HOST == '':
            self.HOST = 'localhost'
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST, self.PORT))
        print("подключение установлено")
        return s
