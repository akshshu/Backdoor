import listener
li = listener.Listener("192.168.43.36", 4545)
li.bind_and_listen()
li.send_command()
