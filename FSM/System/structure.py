class SuperBlock(object):

    def __init__(self):

        config = Method().config_loader()

        self.system_name = config['System']
        self.version = config['Version']
        self.bit = config['bit']
        self.file_system_size = config['DiskSize'] * 1024 * 1024    # MB
        self.data_block_size = config['DataBlockSize'] * 1024  # KB
        self.data_block_index_size = config['DataBlockIndexSize'] * 1024   # KB
        self.data_block_num = config['DataBlockNum']
        self.inode_size = config['InodeSize']   # KB
        self.inode_density = config['InodeDensity']
        self.inode_num = int(self.file_system_size / self.inode_density)
        self._address_ = 4

        Method.cod(text='[INFO] Load config succeed', color='yellow')


class Inode(object):

    def __init__(self):
        self.file_size = 0

        self.block_num = 0

        self.block_index = {
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None,
            7: None,
            8: None,
            9: None,
            10: None,
            11: {},
            12: {},
        }

    def get_inode_information(self):

        return {'file_size': self.file_size, 'block_num': self.block_num}

    def get_blocks_index(self):

        blocks_index = []

        count = 0

        for i in range(self.block_num):

            count += 1

            if count < 11:
                blocks_index.append(self.block_index[count])

            elif 11 <= count < 2048 + 11:
                blocks_index.append(self.block_index[11][count - 10])

            elif 2048 + 11 <= count < 2048 * 2048 + 11:
                blocks_index.append(self.block_index[12][count - 10])

            else:
                Method.cod(text='[ERROR] Out if Memory, system crash!', color='red')

        return blocks_index

    def set_file_size(self, size):

        self.file_size = size

    def set_blocks_index(self, blocks_index):

        tmp = len(blocks_index)

        if tmp >= 2048 * 2048 + 11:

            Method.cod(text=f"[ERROR] File out of memory, operation cancel", color='red')

            return

        self.block_num = tmp

        count = 0

        for index in blocks_index:

            count += 1

            if count < 11:
                self.block_index[count] = index

            elif 11 <= count < 2048 + 11:
                self.block_index[11][count - 10] = index

            elif 2048 + 11 <= count < 2048 * 2048 + 11:
                self.block_index[12][count - 10] = index

            else:
                pass


class User(object):
    def __init__(self, name, index, level):

        self.user_name = name

        self.dir_index = index

        self.user_level = level


class Method:

    def config_loader(self):

        try:
            from yaml import load, SafeLoader

            f = open(file='./config.yml', mode='r', encoding='utf-8')

            content = f.read()

            f.close()

            Method.cod(text=f"[INFO] Read config succeed", color='yellow')

            return load(stream=content, Loader=SafeLoader)

        except FileNotFoundError:

            Method.cod(text=f"[ERROR] Cannot read config!", color='red')

            exit(-1)

        except ImportError:

            self.cod(text=f"[ERROR] Cannot import yaml, try 'pip install pyyaml'", color='red')

            exit(-1)

    @staticmethod
    def cod(text, dp='default', color='white', bg='None', end_str=True):
        """
        :param end_str: True to jump to next line
        :param text: content to print
        :param dp: display mode
        :param color: font-color
        :param bg: background color
        :return: deal to get_value
        """
        display = {
            'default': 0,
            'highlight': 1,
            'underline': 4,
            'swing': 5,
        }
        font_color = {
            'None': '',
            'black': 30,
            'red': 31,
            'green': 32,
            'yellow': 33,
            'blue': 34,
            'purple': 35,
            'indigo': 36,
            'white': 37,
        }
        background_color = {
            'None': '',
            'black': 40,
            'red': 41,
            'green': 42,
            'yellow': 43,
            'blue': 44,
            'purple': 45,
            'indigo': 46,
            'white': 47,
        }
        if end_str is True:
            print(f"\033[{display[dp]};{background_color[bg]};{font_color[color]}m{text} \033[0m")
        else:
            print(f"\033[{display[dp]};{background_color[bg]};{font_color[color]}m{text} \033[0m", end='')
