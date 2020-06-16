from multiprocessing.connection import Client

from System.structure import Method


class UserUI(object):

    def __init__(self):

        self.address = ('localhost', 9000)
        self.location = '/'
        self.loc_flag = 0

        self.login_info()

        try:
            with Client(self.address, authkey=b'password') as conn:

                conn.send(f"0 register guest")  # register format

                self.user_handle = conn.recv()

                Method.cod(text=f"[Info] Connect to FSM succeed!", color='indigo')

                Method.cod(text=f"[Info] File System Handle {self.user_handle}", color='purple')

                Method.cod(text=f"[Hint] Please log in first, or you don't have any permissions!", color='red')

        except ConnectionRefusedError:
            Method.cod(text=f"Cannot connect to server, please try again", color='red', )
            exit(1)

    @staticmethod
    def login_info():
        paragraph = '──────────────────────────────────────────────────────────\n' \
                    '   ██████  ██████  █     █   Welcome to                   \n' \
                    '   █       █       ██   ██   FSM Simulator Beta v1.0      \n' \
                    '   ██████  ██████  █ █ █ █                                \n' \
                    '   █            █  █  █  █   @ZeongPaang. SID:3118004985  \n' \
                    '   █       ██████  █     █   /report to report any bugs.  \n' \
                    '──────────────────────────────────────────────────────────'
        Method.cod(text=paragraph, color='yellow', )

    def command(self, commands):

        command = commands.split()

        try:

            operation = command[0]
        except IndexError:
            return

        if operation == 'help':
            Method.cod(text='FSM helper\n'
                            '  -permission\n'
                            '  -stat         [name]\n'
                            '  -cd           [name]\n'
                            '  -mkdir        [name]\n'
                            '  -rm           [name]\n'
                            '  -search       [name]\n'
                            '  -read/-cat    [name]\n'
                            '  -cp           [source] [target]\n'
                            '  -download     [source] [target]\n'
                            '  -upload       [source] [target]\n'
                            '  -stop/exit    \n'
                            '  -clear        \n',
                       color='indigo')

        elif operation == 'exit':
            print('[Process completed]')
            exit(0)

        elif operation == 'clear':
            print('\n' * 20)
            self.login_info()

        elif operation in ['stat', 'cd', 'ls', 'mkdir', 'rmdir', 'rm', 'search', 'cat', 'cp', 'upload', 'download',
                           'login', 'logout', 'permission']:

            if operation == 'cd':

                if command[1] == '.':
                    return

                self.loc_flag = 1

            try:
                with Client(self.address, authkey=b'password') as conn:

                    conn.send(str(self.user_handle) + ' ' + commands)

                    result = conn.recv()

                    if result == 'No such file or directory!':
                        pass

                    else:
                        if self.loc_flag:
                            self.location = result
                            self.loc_flag = 0
                            return

                    self.terminal()

                    print(result)

            except ConnectionRefusedError:
                Method.cod(f"[Connect] Connect lost, please restart client", color='red')

        else:
            print('-bash:', operation, ': command not found')

    def terminal(self):

        Method.cod(text=f"> {self.location} $", end_str=False)


def main():
    ui = UserUI()

    while True:
        ui.terminal()

        user_input = input()

        ui.command(user_input)


if __name__ == '__main__':
    main()
