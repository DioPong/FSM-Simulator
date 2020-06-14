import yaml
"""
>>> 定义基本的文件目录
"""


class SuperBlock(object):
    def __init__(self):
        # 读取文件配置
        try:
            config = load_config()
            for key in config:
                if key not in ['version', 'system_name']:
                    if not type(config[key]) != "<class 'int'>":
                        EXIT(0)

            self.bit = config['bit']
            self.version = config['version']
            self.system_name = config['system_name']
            self.system_size = int(config['system_size'] * 1024 * 1024)
            self.data_block_size = config['data_block_size'] * 1024
            self.data_block_index_size = config['data_block_index_size']
            self.data_block_num = config['data_block_num']
            self.inode_size = config['inode_size']
            self.inode_density = config['inode_density']
            self.inode_num = int(self.system_size / self.inode_density)
            self._address_size_ = 4

            print(self.data_block_size)

        except IOError as exc:
            print(exc)
            EXIT(0)


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
        }

    def get_info(self):
        return {'size': self.file_size, 'block_num': self.block_num}

    def get_block_index(self):
        index_ = self.block_index
        block_index_ = []

        count = 0
        for i in range(self.block_num):

            count += 1

            if count < 11:
                block_index_.append(self.block_index[count])
            elif count >= 11 and count < 2048 + 13:
                block_index_.append(self.block_index[11][count - 10])
            else:
                pass

        return block_index_

    def set_file_size(self, size):
        self.file_size = size

    def set_blocks_index(self, blocks_index):

        self.block_num = len(blocks_index)

        count = 0
        for index in blocks_index:

            count += 1

            if count < 11:
                self.block_index[count] = index
            elif 11 <= count < 2048 + 13:
                self.block_index[11][count - 10] = index
            else:
                pass


# 用户目录
class User(object):
    def __init__(self):
        self.dir_index = 0

    def set_dir_index(self, dir_index):
        self.dir_index = dir_index


class EXIT:
    """
    0  | 0x0    : I/O error
    1  | 0x1    : one of configs out of range
    """
    def __init__(self, status_code):
        print('ERROR ', status_code)
        exit(0)


# 读取配置文件
def load_config():
    f = open('../config.yml', 'r', encoding='utf-8')
    content = f.read()
    f.close()
    return yaml.load(content, Loader=yaml.SafeLoader)
