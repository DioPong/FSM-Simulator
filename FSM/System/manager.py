from System.structure import SuperBlock, Inode, User
import numpy as np
import sys

"""
>>> File System Manager
"""


class FileSystemManager(object):
    def __init__(self):

        self.result = ''

        self.para = []

        self.usr_index = []

        self.commands = {
            'register': self.register(),
            'stat': self.stat(),
            'cd': self.cd(),
            'ls': self.ls(),
            'mkdir': self.mkdir(),
            'rm': self.rm(),
            'read': self.read(),
            'cat': self.read(),
            'search': self.search(),
            'cp': self.cp(),
            'upload': self.upload(),
            'download': self.download(),
        }

        self.super_block = SuperBlock()

        self.file_manager = FileManager(super_block=self.super_block)

        self.usr_manager = UserManager()

        ColorInfo(content=f"File System Initialized", fg='green')

    def message_processor(self, msg):

        msg_list = msg.split()

        self.usr_index, self.commands = msg_list[:2]

        self.usr_index = int(self.usr_index)

        self.para = msg_list[2:]

    def message_input(self, msg):

        self.message_processor(msg=msg)

        self.dispatcher()

    def message_output(self):

        result = self.result

        self.result = ''

        return result

    def dispatcher(self):
        instruct_ = self.commands.get(self.commands)

        instruct_()

    # >>>>>>>>>>>>>>>>>>>> Commands <<<<<<<<<<<<<<<<<<<<

    def register(self):

        self.result = self.usr_manager.add_usr()

    def stat(self):

        index_loc = self.usr_manager.get_loc_index(index=self.usr_index)

        data_dir = self.file_manager.load(index=index_loc, data_type='dir')

        try:
            name = self.para[0]
            index = data_dir[name]

        except KeyError as e:
            ColorInfo(content=e)
            return

        except IndexError as e:
            ColorInfo(content=e)
            return

        info = self.file_manager.information(index=index)

        info['file name'] = name

        result = '\n'

        for key, value in info.items():
            result += key
            result += ':'
            result += str(value)
            result += ' '

        self.result = result

    def cd(self):

        loc_index = self.usr_manager.get_loc_index(index=self.usr_index)

        data_dir = self.file_manager.load(index=loc_index, data_type='dir')

        try:
            name = self.para[0]
            index = data_dir[name]

        except KeyError:
            # ColorInfo(content=e, fg='yellow')
            self.result = 'No such file or dictionary'
            return

        except IndexError:
            # ColorInfo(content=e, fg='yellow')
            self.result = 'Command Error'
            return

        next_loc_index = index
        self.usr_manager.set_loc_index(usr_index=self.usr_index, loc_index=next_loc_index)

        next_data_dir = self.file_manager.load(index=next_loc_index, data_type='dir')

        self.result = next_data_dir['.']

    def ls(self):

        loc_index = self.usr_manager.get_loc_index(index=self.usr_index)

        data_dir = self.file_manager.load(index=loc_index, data_type='dir')

        data_dir.pop('.')
        data_dir.pop('..')

        if data_dir is None:
            self.result = 'None'
            return

        result = '\n'

        for key in data_dir:
            result = result + key + '\n'

        self.result = result

    def mkdir(self):

        loc_index = self.usr_manager.get_loc_index(index=self.usr_index)

        try:
            name = self.para[0]
        except IndexError:
            self.result = 'Command Error'
            return

        data_ = {'.': name, '..': loc_index, }

        index = self.file_manager.save(data=data_)

        ColorInfo(content=f"New dir {name} created. Inode index: {index}", fg='yellow')

        ColorInfo(content=f"Current dir inode index: {loc_index}")

        index = self.file_manager.update_dir(index=loc_index, new_dict={name: index})

        ColorInfo(content=f"Current dir is save in inode index: {index}")

        self.usr_manager.set_loc_index(usr_index=self.usr_index, loc_index=index)

        self.result = "Folder mkdir succeed"

    def rm(self):

        loc_index = self.usr_manager.get_loc_index(index=self.usr_index)

        ColorInfo(content=f"Current dir inode index: {loc_index}")

        data_dir = self.file_manager.load(index=loc_index, data_type='dir')

        ColorInfo(content=f"Current dir: {data_dir}", fg='yellow')

        try:
            name = self.para[0]
            index = data_dir[name]

        except KeyError:
            self.result = 'No such file or dictionary'
            return

        except IndexError:
            self.result = 'Command Error'
            return

        self.file_manager.delete(index=index)

        ColorInfo(content=f"Current dir updated: {data_dir}")

        index = self.file_manager.update_dir(index=loc_index, new_dict={name: index}, method='del')

        ColorInfo(content=f"Current dir is saved in inode index: {index}")

        self.usr_manager.set_loc_index(usr_index=self.usr_index, loc_index=index)

        self.result = 'Command rm execute succeed'

    def search(self):

        loc_index = self.usr_manager.get_loc_index(index=self.usr_index)

        name_search_list = self.file_manager.sub_file_dir(index=loc_index, dirs='')

        try:
            name = self.para[0]

        except IndexError:
            self.result = 'Command Error'
            return

        to_find = list(filter(lambda item: name in item.xplit('/').pop(), name_search_list))

        result = '\n'

        if to_find is not None:
            for i in to_find:
                result = result + i + '\n'

        else:
            result = 'File or folder is not fount'

        self.result = result

    def read(self):

        loc_index = self.usr_manager.get_loc_index(index=self.usr_index)

        data_dir = self.file_manager.load(index=loc_index, data_type='dir')

        try:
            name = self.para[0]
            index = data_dir[name]

        except KeyError:
            self.result = 'No such file or dictionary'
            return

        except IndexError:
            self.result = 'Command Error'
            return

        data = self.file_manager.load(index=index, data_type='text')

        data = f"\n{data}"

        self.result = data

    def cp(self):

        loc_index = self.usr_manager.get_loc_index(index=self.usr_index)

        data_dir = self.file_manager.load(index=loc_index, data_type='dir')

        try:
            source_file = self.para[0]
            target_file = self.para[1]

            source_file_index = data_dir[source_file]

        except KeyError:
            self.result = 'No such file or dictionary'
            return

        except IndexError:
            self.result = 'Command Error'
            return

        data = self.file_manager.load(index=source_file_index, data_type='binary')

        index = self.file_manager.save(data=data)

        self.file_manager.update_dir(index=loc_index, new_dict={target_file: index})

        self.result = 'Command cp execute succeed'

    def upload(self):

        try:
            source_file = self.para[0]
            target_file = self.para[1]

            source_file_path = f"{sys.path[0]}/{source_file}"

            f = open(source_file_path, 'rb')

        except FileNotFoundError:
            self.result = f"File not found, Please check again"
            return

        except IndexError:
            self.result = 'Command Error'
            return

        file_content = f.read()

        f.close()

        index = self.file_manager.save(data=file_content)

        loc_index = self.usr_manager.get_loc_index(index=self.usr_index)

        self.file_manager.update_dir(index=loc_index, new_dict={target_file: index})

        self.result = 'Upload File Succeed'

    def download(self):

        try:
            file_name = self.para[0]
            file_path = self.para[1]

        except IndexError:
            self.result = 'Command Error'
            return

        loc_index = self.usr_manager.get_loc_index(index=self.usr_index)

        data_dir = self.file_manager.load(index=loc_index, data_type='dir')

        try:
            index = data_dir[file_name]

        except KeyError:
            self.result = 'No such file or dictionary'
            return

        data = self.file_manager.load(index=index, data_type='binary')

        path = f"{sys.path[0]}/{file_path}"

        with open(path, 'wb') as f:
            f.write(data)
        f.close()

        self.result = 'Download file succeed'


class UserManager(object):
    def __init__(self):

        self.users = []

    def add_usr(self):
        user = User()

        self.users.append(user)

        return len(self.users) - 1

    def rm_usr(self):
        user = User()

        self.users.remove(user)

        return len(self.users) + 1

    def get_loc_index(self, index):

        return self.users[index].dir_index

    def set_loc_index(self, usr_index, loc_index):

        self.users[usr_index].dir_index = loc_index


class FileManager(object):
    def __init__(self, super_block):
        self.inode_manager = InodeManager(sys_bit=super_block.bit, block_nums=super_block.inode_num)

        self.block_manager = BlockManager(
            sys_bit=super_block.bit,
            block_size=super_block.data_block_size,
            block_num=super_block.data_block_num,
        )

        root_dir = {'.': '/', '..': 0, }

        index = self.save(root_dir)

        ColorInfo(content=f"Root dictionary inode index is {index}", fg='blue')

        ColorInfo(content=f"File Manager Initialized")

    def save(self, data):
        ColorInfo(content=f"Data: {data}\nis saving")

        data = Methods.transform_type(data=data)

        size = len(data)

        blocks_index = self.block_manager.save(data=data)

        ColorInfo(content=f'Data saved in block: {blocks_index}', fg='blue')

        return self.inode_manager.save(block_index=blocks_index, alloc_size=size)

    def delete(self, index):
        blocks_index = self.inode_manager.get_blocks_index(index=index)

        ColorInfo(content=f"Inode index {index} deleted", fg='red')

        self.block_manager.reset(index_s=blocks_index)

        self.inode_manager.reset(index=index)

        ColorInfo(content=f"Blocks index {blocks_index} deleted", fg='red')

        pass

    def load(self, index, data_type):
        inode = self.inode_manager.get_inode(index=index)

        blocks_index = inode.get_block_index()

        ColorInfo(content=blocks_index)

        data_ = self.block_manager.get_data(index_s=blocks_index)

        data_ = Methods.transform_type(data=data_, target_type=data_type)

        return data_

    def update_dir(self, index, new_dict, method='add'):

        data_dir = self.load(index=index, data_type='dir')

        ColorInfo(content=f"Dir: {data_dir}")

        if method == 'del':

            keys = new_dict.keys()

            for key in keys:
                del data_dir[key]

        else:

            data_dir.update(new_dict)

        ColorInfo(content=f'Dir updated: {data_dir}')

        self.delete(index=index)

        index = self.save(data=data_dir)

        return index

    def sub_file_dir(self, index, dirs):

        file_dir_list = []

        data_dir = self.load(index=index, data_type='dir')

        for key, value in data_dir.items():

            file_dir_list.append(key)

            if '.' not in key:

                file_dir_list.extend(self.sub_file_dir(index=value, dirs=key))

        file_dir_list = [dirs + '/' + x for x in file_dir_list]

        return file_dir_list

    def information(self, index):

        inode = self.inode_manager.get_inode(index=index)

        return inode.get_info()


class InodeManager(object):
    def __init__(self, sys_bit, block_nums):
        self.map_ = np.zeros((sys_bit, int(block_nums / sys_bit)))

        self.inodes = []

        for i in range(block_nums):
            inode = Inode()
            self.inodes.append(inode)

        ColorInfo("Inode Manager initialized.")

    def reset(self, index):
        ColorInfo(f"Resetting inode of index: {index}")

        x, y = Methods.index_2_xy(width=self.map_.shape[0], height=self.map_.shape[1], index=index)

        self.map_[x][y] = 0

    def save(self, block_index, alloc_size):
        index = self.alloc_inode()

        inode = self.get_inode(index=index)

        inode.set_file_size(size=alloc_size)

        inode.set_blocks_index(blocks_index=block_index)

        return index

    def alloc_inode(self):
        inode_index = np.where(self.map_ == 0)

        inode_index_x = inode_index[0][0]

        inode_index_y = inode_index[1][0]

        self.map_[inode_index_x][inode_index_y] = 1

        inode_index = Methods.xy_2_index(height=self.map_.shape[1], x=inode_index_x, y=inode_index_y)

        return inode_index

    def get_inode(self, index):

        return self.inodes[index]

    def get_blocks_index(self, index):
        index = self.inodes[index].get_block_index()

        return index


class BlockManager(object):
    def __init__(self, sys_bit, block_size, block_num):

        self.block_size = block_size

        self.map_ = np.zeros((sys_bit, int(block_num / sys_bit)))

        self.block_s = [b''] * block_num

        ColorInfo("Block Manager initialized.")

    def set_data_to_blocks(self, data, index_s):

        for i in range(len(index_s)):
            self.block_s[index_s[i]] = data[i * 8192:(i + 1) * 8192]

    def get_data(self, index_s):

        return self.get_data_from_blocks(blocks=self.get_block_s(index_s=index_s))

    @staticmethod
    def get_data_from_blocks(blocks):

        binary_data = b''

        for block in blocks:
            binary_data += block

        return binary_data

    def get_block_s(self, index_s):

        blocks = []

        for index in index_s:
            blocks.append(self.block_s[index])

        return blocks

    def alloc_blocks(self, size):

        block_num = int(size / self.block_size) + 1

        blocks_index = []

        data_blocks_index = np.where(self.map_ == 0)

        for i in range(block_num):
            data_blocks_index_x = data_blocks_index[0][i]

            data_blocks_index_y = data_blocks_index[1][i]

            data_blocks_index_c = data_blocks_index_x * self.map_.shape[1] + data_blocks_index_y

            blocks_index.append(data_blocks_index_c)

            self.map_[data_blocks_index_x][data_blocks_index_y] = 1

        return blocks_index

    def reset(self, index_s):
        self.set_data_to_blocks(data=b'', index_s=index_s)

        for index in index_s:
            x, y = Methods.index_2_xy(width=self.map_.shape[0], height=self.map_.shape[1], index=index)
            self.map_[x][y] = 0

    def save(self, data):
        size = len(data)

        index_s = self.alloc_blocks(size=size)

        self.set_data_to_blocks(data=data, index_s=index_s)

        return index_s


class Methods:
    @staticmethod
    def index_2_xy(width, height, index):

        x = y = 0

        if index == 0:
            return x, y

        else:
            for i in range(width):
                for j in range(height):
                    index -= 1
                    y += 1

                    if index == 0:
                        return x, y

            x += 1

    @staticmethod
    def xy_2_index(height, x, y):

        index = x * height + y

        return index

    @staticmethod
    def transform_type(data, target_type=None):

        if isinstance(data, str):
            data = bytes(data, encoding='utf-8')

        elif isinstance(data, dict):
            data = bytes(str(data), encoding='utf-8')

        elif isinstance(data, bytes):
            if target_type == 'dir':
                data = eval(data)

            elif target_type == 'text':
                data = str(data, encoding='utf-8')

            else:
                data = data

        else:
            print(f'Data Transform Error')
            return

        return data


class ColorInfo:
    def __init__(self, content, display='default', fg='none', bg="none"):
        #   开头部分：\033[显示方式;前景色;背景色m + 结尾部分：\033[0m
        dp = {
            'default': 0,
            'highlight': 1,
            'underline': 4,
            'swing': 5,
        }
        font_color = {
            'none': '',
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
            'none': '',
            'black': 40,
            'red': 41,
            'green': 42,
            'yellow': 43,
            'blue': 44,
            'purple': 45,
            'indigo': 46,
            'white': 47,
        }
        print(f"\033[{dp[display]};{background_color[bg]};{font_color[fg]}m {content} \033[0m")
