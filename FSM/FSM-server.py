from multiprocessing.connection import Listener

from System.manager import *


class SERVER:
    def __init__(self):
        self.fsm = FileSystemManager()

        self.address = ('localhost', 9000)

        self.password = b'password'

        self.server()

    def server(self):

        Methods.cod(text=f"Listening {self.address[0]}, port: {self.address[1]}", color='blue', flag='info')

        while True:

            with Listener(address=self.address, authkey=self.password) as listener:

                with listener.accept() as conn:

                    Methods.cod(text=f"[Connect] Connection accepted from {listener.last_accepted}", color='blue')

                    msg = conn.recv()

                    self.fsm.input(msg=msg)

                    result = self.fsm.output()

                    conn.send(str(result))


if __name__ == '__main__':
    SERVER()
