"""
tarotclub game python AI

this is a try to make a python AI for the tarotclub game
"""

import struct

class Identity(object):
    """clone of the tarotclub Identity class"""

    GENDER_INVALID = 0
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_ROBOT = 3
    GENDER_DUMMY = 4

    def __init__(self, nickname='', avatar='', gender=GENDER_INVALID, username=''):
        self.nickname = nickname
        self.avatar = avatar
        self.gender = gender
        self.username = username

    def to_bytes(self):
        """encode to a bytes object"""
        byte = b''

        s_size = len(self.nickname)
        byte += struct.pack('<I%ds' % s_size, s_size, self.nickname.encode('ascii'))

        s_size = len(self.avatar)
        byte += struct.pack('<I%ds' % s_size, s_size, self.avatar.encode('ascii'))

        byte += struct.pack('<B', self.gender)

        s_size = len(self.username)
        byte += struct.pack('<I%ds' % s_size, s_size, self.username.encode('ascii'))

        return byte

    def from_bytes(self, byte):
        """decode a bytes object"""
        offset = 0

        (s_size, ) = struct.unpack('<I', byte[offset:offset + 4])
        offset += struct.calcsize('I')
        (self.nickname, ) = struct.unpack('<%ds' % s_size, byte[offset:offset + s_size])
        offset += s_size

        (s_size, ) = struct.unpack('<I', byte[offset:offset + 4])
        offset += struct.calcsize('I')
        (self.avatar, ) = struct.unpack('<%ds' % s_size, byte[offset:offset + s_size])
        offset += s_size

        (self.gender, ) = struct.unpack('<B', byte[offset:offset + 1])
        offset += struct.calcsize('B')

        (s_size, ) = struct.unpack('<I', byte[offset:offset + 4])
        offset += struct.calcsize('I')
        (self.username, ) = struct.unpack('<%ds' % s_size, byte[offset:offset + s_size])
        offset += s_size

        return offset

    def __str__(self):
        return 'nickname = %s, ' % self.nickname \
                + 'avatar = %s, ' % self.avatar \
                + 'gender = %d, ' % self.gender \
                + 'username = %s' % self.username

