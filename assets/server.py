from connectIO import Server, threaded


class ExampleServer(Server):

    def __init__(self, ip='127.0.0.1', port=5555):
        super(ExampleServer, self).__init__(ip, port)
        self.func = self.threaded_conn

    @threaded
    def threaded_conn(self, conn, addr):
        raddr = conn.getpeername()

        greeting = 'hello client!'
        print(f'Server -> {raddr}: {greeting}')

        self.send(conn, greeting)
        print(f'{raddr} -> Server: {self.recieve(conn)}')

        response = 'great you?'
        print(f'Server -> {raddr}: {response}')

        self.send(conn, response)
        print(f'{raddr} -> Server: {self.recieve(conn)}')

    def __del__(self):
        print("Server closed")


if __name__ == "__main__":
    ExampleServer().run()
