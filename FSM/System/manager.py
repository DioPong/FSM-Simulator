from System.structure import SuperBlock, Inode, User

import sys

try:
    from numpy import zeros, where

except ImportError:
    print('[ERROR] Cannot import numpy, '
          'please install numpy.')
    exit(-1)


class FileSystemManager(object):

    def __init__(self):

        self.result = ''

        self.command = []

        self.parameters = []

        self.user_index = 0

        self.commands = {
            'register': self.register,
            'stat': self.stat,
            'cd': self.cd,
            'ls': self.ls,
            'mkdir': self.mkdir,
            'rmdir': self.rm,
            'rm': self.rm,
            'find': self.find,
            'more': self.more,
            'cp': self.cp,
            'import': self.file_import,
            'export': self.file_export
        }

        self.super_block = SuperBlock()

        self.file_manager = FileManager(self.super_block)

        self.user_manager = UserManager()

        Methods.cod(text='File System Initialized', flag='info', color='indigo')

    def input(self, msg):

        self.msg_process(msg)

        self.dispatcher()

    def output(self):

        result = self.result

        self.result = ''

        return result

    def msg_process(self, msg):

        msg_list = msg.split()

        self.user_index, self.command = msg_list[:2]  # str

        self.user_index = int(self.user_index)

        self.parameters = msg_list[2:]  # str_list

        # choose

    def dispatcher(self):

        instruct = self.commands.get(self.command)

        try:
            instruct()

        except SyntaxError as e:
            Methods.cod(text=f"{e}", flag='error', color='red')

        except Exception as e:
            Methods.cod(text=e, flag='error', color='red')

    def register(self):

        self.result = self.user_manager.add_user()

    def stat(self):

        location_index = self.user_manager.get_location_index(self.user_index)
        dir_data = self.file_manager.load(location_index, 'dir')

        try:
            name = self.parameters[0]
            index = dir_data[name]

        except KeyError:

            self.result = 'No such file or directory!'

            return

        except IndexError:
            self.result = 'Command error!'
            return

        information = self.file_manager.get_information(index)

        information['file name'] = name

        result = '\n'

        for k, v in information.items():
            result += k
            result += ':'
            result += str(v)
            result += ' '

        self.result = result

    def cd(self):

        location_index = self.user_manager.get_location_index(self.user_index)

        dir_data = self.file_manager.load(location_index, 'dir')

        try:
            name = self.parameters[0]
            index = dir_data[name]

        except KeyError:

            self.result = 'No such file or directory!'

            return

        except IndexError:
            self.result = 'Command error!'
            return

        next_location_index = index
        self.user_manager.set_location_index(
            self.user_index, next_location_index)

        next_dir_data = self.file_manager.load(next_location_index, 'dir')

        self.result = next_dir_data['.']

    def ls(self):

        location_index = self.user_manager.get_location_index(self.user_index)
        dir_data = self.file_manager.load(location_index, 'dir')

        dir_data.pop('.')
        dir_data.pop('..')

        if not dir_data:
            self.result = '\nNone'
            return

        result = '\n'

        for key in dir_data.keys():
            result += key
            result += '\n'

        self.result = result

    def mkdir(self):

        location_index = self.user_manager.get_location_index(self.user_index)

        try:

            name = self.parameters[0]
        except IndexError:
            self.result = 'Command error!'
            return

        data = {
            '.': name,
            '..': location_index
        }

        index = self.file_manager.save(data)

        Methods.cod(text=f"New dir file inode index: {index}, name: {name}", flag='info', color='yellow')

        Methods.cod(text=f"Current dir inode index: {location_index}", flag='info', color='yellow')

        index = self.file_manager.update_dir_file(location_index, {name: index})

        Methods.cod(text=f"Current dir saved in inode index: {index}")

        self.user_manager.set_location_index(self.user_index, index)

        self.result = 'mkdir succeed!'

    def rm(self):

        location_index = self.user_manager.get_location_index(self.user_index)

        Methods.cod(text=f"Current dir inode index: {location_index}", flag='info', color='yellow')

        dir_data = self.file_manager.load(location_index, 'dir')

        Methods.cod(text=f"Current dir: {dir_data}", flag='info', color='yellow')

        try:
            name = self.parameters[0]
            index = dir_data[name]

        except KeyError:

            self.result = 'No such file or directory!'

            return
        except IndexError:
            self.result = 'Command error!'
            return

        self.file_manager.delete(index)

        Methods.cod(text=f"Current dir {dir_data} update", flag='info')

        index = self.file_manager.update_dir_file(
            location_index, {name: index}, 'del')

        Methods.cod(text=f"Current dir save in inode index: {index}")

        self.user_manager.set_location_index(self.user_index, index)

        self.result = 'rm succeed!'

    def find(self):

        location_index = self.user_manager.get_location_index(self.user_index)

        name_list = self.file_manager.sub_file(location_index, '')

        try:
            name = self.parameters[0]

        except IndexError:

            self.result = 'Command error!'

            return

        find_list = list(
            filter(lambda x: name in x.split('/').pop(), name_list))

        result = '\n'

        if find_list:

            for i in find_list:

                result += i

                result += '\n'
        else:

            result = 'Not found.'

        self.result = result

    def more(self):

        location_index = self.user_manager.get_location_index(self.user_index)

        dir_data = self.file_manager.load(location_index, 'dir')

        try:

            name = self.parameters[0]

            index = dir_data[name]

        except KeyError:

            self.result = 'No such file or directory!'

            return
        except IndexError:

            self.result = 'Command error!'

            return

        data = self.file_manager.load(index, 'text')

        data = '\n'+data

        self.result = data

        pass

    def cp(self):

        location_index = self.user_manager.get_location_index(self.user_index)

        dir_data = self.file_manager.load(location_index, 'dir')

        try:
            name1 = self.parameters[0]
            name2 = self.parameters[1]
            index1 = dir_data[name1]

        except KeyError:

            self.result = 'No such file or directory!'

            return

        except IndexError:
            self.result = 'Command error!'

            return

        data = self.file_manager.load(index1, 'binary')

        index = self.file_manager.save(data)

        self.file_manager.update_dir_file(location_index, {name2: index})

        self.result = 'cp succeed!'

    def file_import(self):

        try:

            name1 = self.parameters[0]

            name2 = self.parameters[1]

            name1 = sys.path[0]+'/'+name1

            f = open(name1, 'rb')

        except IndexError:

            self.result = 'Command error!'

            return
        except FileNotFoundError:

            self.result = 'FileNotFoundError: not found!'

            return

        data = f.read()

        index = self.file_manager.save(data)

        location_index = self.user_manager.get_location_index(self.user_index)

        self.file_manager.update_dir_file(location_index, {name2: index})

        self.result = 'file import succeed!'

    def file_export(self):

        try:

            name = self.parameters[0]

            path = self.parameters[1]

        except IndexError:

            self.result = 'Command error!'

            return

        location_index = self.user_manager.get_location_index(self.user_index)

        dir_data = self.file_manager.load(location_index, 'dir')

        try:
            index = dir_data[name]

        except KeyError:

            self.result = 'No such file or directory!'

            return

        data = self.file_manager.load(index, 'binary')

        path = sys.path[0]+'/'+path

        with open(path, 'wb') as f:

            f.write(data)

        self.result = 'file export succeed!'


class UserManager(object):

    pass

    def __init__(self):
        self.users = []

    def add_user(self):

        user = User()

        self.users.append(user)

        return len(self.users) - 1

    def delete_user(self):
        pass

    def get_location_index(self, index):

        return self.users[index].dir_index

    def set_location_index(self, user_index, loc_index):

        self.users[user_index].dir_index = loc_index


class FileManager(object):

    def __init__(self, super_block):

        self.inode_manager = InodeManager(super_block.bit, super_block.inode_num)
        self.block_manager = BlockManager(
            super_block.bit, super_block.data_block_size, super_block.data_block_num)

        root_dir = {
            '.': '/',
            '..': 0
        }
        index = self.save(root_dir)

        Methods.cod(text=f"Root dir inode index: {index}", flag='info')

        Methods.cod(text=f"File Manager Initialized", flag='info', color='indigo')
        pass

    def get_information(self, index):

        inode = self.inode_manager.get_inode(index)
        return inode.get_inode_information()

    def sub_file(self, index, dir_name):

        file_list = []

        dir_data = self.load(index, 'dir')

        for k, v in dir_data.items():

            file_list.append(k)

            if '.' not in k:

                file_list.extend(self.sub_file(v, k))

        file_list = [dir_name+'/'+x for x in file_list]

        return file_list

    def update_dir_file(self, index, new_dict, flag='add'):

        dir_data = self.load(index, 'dir')

        if flag == 'del':

            keys = new_dict.keys()

            for key in keys:

                del dir_data[key]

        else:

            dir_data.update(new_dict)

        Methods.cod(text=f"Current dir updated: {dir_data}")

        self.delete(index)

        index = self.save(dir_data)

        return index

    def load(self, index, data_type):

        inode = self.inode_manager.get_inode(index)

        block_index_s = inode.get_blocks_index()

        data = self.block_manager.get_data(block_index_s)

        data = Methods.transform(data=data, to=data_type)

        return data

    def delete(self, index):

        Methods.cod(text=f"Delete inode index: {index}", flag='info')

        blocks_index_s = self.inode_manager.get_block_index_s(index)

        Methods.cod(text=f"Delete blocks index: {blocks_index_s}", flag='info')

        self.block_manager.reset(blocks_index_s)

        self.inode_manager.reset(index)

        pass

    def save(self, data):

        data = Methods.transform(data=data)

        size = len(data)

        block_index_s = self.block_manager.save(data)

        Methods.cod(text=f"Data saved in blocks: {block_index_s}", flag='info')

        return self.inode_manager.save(block_index_s, size)


class InodeManager(object):

    def __init__(self, bit, num):

        self.map = zeros((bit, int(num/bit)))
        self.inodes = []

        for i in range(num):
            inode = Inode()
            self.inodes.append(inode)

        Methods.cod(text=f"Inode Manager Initialized", flag='info', color='indigo')

    def reset(self, index):

        Methods.cod(text=f"Inode index is resetting {index}")

        x, y = Methods.index_to_two_dimensional(width=self.map.shape[0],
                                                height=self.map.shape[1],
                                                index=index, )

        self.map[x][y] = 0

    def save(self, block_index_s, size):

        index = self.allocate_inode()

        inode = self.get_inode(index)

        inode.set_file_size(size=size)

        inode.set_blocks_index(blocks_index=block_index_s)

        return index

    def allocate_inode(self):

        inode_index = where(self.map == 0)

        inode_index_x = inode_index[0][0]
        inode_index_y = inode_index[1][0]

        self.map[inode_index_x][inode_index_y] = 1

        inode_index = Methods.two_dimensional_to_index(
            height=self.map.shape[1],
            x=inode_index_x,
            y=inode_index_y, )

        return inode_index

    def get_inode(self, index):
        return self.inodes[index]

    def get_block_index_s(self, index):
        index_s = self.inodes[index].get_blocks_index()
        return index_s


class BlockManager(object):
    def __init__(self, bit, size, num):

        self.block_size = size
        self.map = zeros((bit, int(num/bit)))
        self.blocks = [b''] * num

        Methods.cod(text=f"Block Manager Initialized", flag='info', color='indigo')

    def reset(self, index_s):

        self.set_data(b'', index_s)

        for index in index_s:
            x, y = Methods.index_to_two_dimensional(width=self.map.shape[0],
                                                    height=self.map.shape[1],
                                                    index=index, )
            self.map[x][y] = 0

    def save(self, data):

        size = len(data)
        index_s = self.allocate_blocks(size)
        self.set_data(data, index_s)
        return index_s

    def allocate_blocks(self, size):

        block_num = int(size / self.block_size) + 1

        block_index_s = []

        data_block_index = where(self.map == 0)

        for i in range(block_num):

            data_block_index_x = data_block_index[0][i]

            data_block_index_y = data_block_index[1][i]

            data_block_index_clean = data_block_index_x * \
                self.map.shape[1] + data_block_index_y

            block_index_s.append(data_block_index_clean)

            self.map[data_block_index_x][data_block_index_y] = 1

        return block_index_s

    def set_data(self, data, index_s):

        for i in range(len(index_s)):

            self.blocks[index_s[i]] = data[i * 8192:(i + 1) * 8192]

    def get_data(self, index_byte_data):

        return self.get_data_from_block(self.get_blocks(index_byte_data))

    @staticmethod
    def get_data_from_block(blocks):

        byte_data = b''

        for block in blocks:

            byte_data += block

        return byte_data

    def get_blocks(self, index_s):

        blocks = []

        for index in index_s:
            blocks.append(self.blocks[index])

        return blocks


class Methods:

    @staticmethod
    def cod(text, flag=None, dp='default', color='white', bg=None, get_value=False):
        """
        :param flag: type of msg: info/warning/error
        :param text: content to print
        :param dp: display mode
        :param color: font-color
        :param bg: background color
        :param get_value: just print text or return a value
        :return: deal to get_value
        """
        display = {
            'default': 0,
            'highlight': 1,
            'underline': 4,
            'swing': 5,
        }
        font_color = {
            None: '',
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
            None: '',
            'black': 40,
            'red': 41,
            'green': 42,
            'yellow': 43,
            'blue': 44,
            'purple': 45,
            'indigo': 46,
            'white': 47,
        }
        flag_type = {
            None: '',
            'info': '[INFO]',
            'warning': '[WARNING]',
            'error': '[ERROR]',
        }

        if get_value is False:
            print(f"\033[{display[dp]};{background_color[bg]};{font_color[color]}m {flag_type[flag]}{text} \033[0m")
        else:
            text = f"\033[{display[dp]};{background_color[bg]};{font_color[color]}m {flag_type[flag]}{text} \033[0m"
            return text

    @staticmethod
    def index_to_two_dimensional(width, height, index):

        x, y = 0, 0

        if index == 0:
            return x, y

        else:
            for p in range(width):
                for q in range(height):

                    index -= 1

                    y += 1

                    if index == 0:
                        return x, y

                x += 1

    @staticmethod
    def two_dimensional_to_index(height, x, y):

        return x * height + y

    @staticmethod
    def transform(data, to=None):

        if isinstance(data, str):
            data = bytes(data, encoding='utf-8')

        elif isinstance(data, dict):
            data = bytes(str(data), encoding='utf-8')

        elif isinstance(data, bytes):
            if to == 'dir':
                data = eval(data)

            elif to == 'text':
                data = str(data, encoding='utf-8')

            else:
                data = data

        else:
            Methods.cod(text=f"[ERROR] An error was occur when data transforming", color='red')
            return

        Methods.cod(text=f"[INFO] Succeed to transform data")
        return data
