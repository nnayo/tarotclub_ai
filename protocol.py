"""
tarotclub game python AI

this is the try to make a python AI for the tarotclub game
"""

import paul
import identity
import socket
import struct

class Protocol(object):
    """tarotclub network protocol"""

    VERSION = 2
    LOBBY_UUID = 1

    CLIENT_JOIN_TABLE = 0x31
    CLIENT_REPLY_LOGIN = 0x33

    LOBBY_CHAT_MESSAGE = 0x40
    LOBBY_REQUEST_LOGIN = 0x41
    LOBBY_LOGIN_RESULT = 0x42
    LOBBY_PLAYERS_LIST = 0x43

    def __init__(self, server_ip, server_port, table):
        """set AI env"""

        print('starting tarotclub python protocol on server %s:%d at table %d' % (server_ip, server_port, table))

        self.sock = socket.create_connection((server_ip, server_port))

        self.uuid = 0
        self.ai = paul.PaulAi()
        self.ai_identity = identity.Identity('Paul', '', identity.Identity.GENDER_ROBOT, 'Paul AI')
        self.players = []

        self._command = {
            Protocol.LOBBY_CHAT_MESSAGE : self._lobby_chat_message,
            Protocol.LOBBY_REQUEST_LOGIN : self._lobby_request_login,
            Protocol.LOBBY_LOGIN_RESULT : self._lobby_login_result,
            Protocol.LOBBY_PLAYERS_LIST : self._lobby_players_list,
        }

    def _resp(self, cmd, src_uuid, dst_uuid, data):
        """return a formated response"""

        header_end = struct.pack('<BIIB', Protocol.VERSION, src_uuid, dst_uuid, cmd)
        size = len(struct.pack('<H', 0) + header_end + data)

        return struct.pack('<H', size) + header_end + data

    def _client_reply_login(self):
        """send AI identity"""

        identity = self.ai_identity.to_bytes()
        print(identity)
        self.sock.send(self._resp(Protocol.CLIENT_REPLY_LOGIN, self.uuid, Protocol.LOBBY_UUID, identity))

    def _lobby_chat_message(self, src_uuid, dst_uuid, data):
        """lobby send a chat message"""
        
        (s_size, ) = struct.unpack('<I', data[0:4])
        print('s_size = %d' % s_size)
        
        (s_msg, ) = struct.unpack('<%ds' % s_size, data[4:])
        print('s_msg = %s' % s_msg)

    def _lobby_request_login(self, src_uuid, dst_uuid, data):
        """server assign a place to a client and it must reply back its identity"""
        print('_lobby_request_login')

        (self.uuid, ) = struct.unpack('<I', data[0:4])
        print('self uuid = 0x%08x' % self.uuid)
 
        self._client_reply_login()

    def _lobby_login_result(self, src_uuid, dst_uuid, data):
        """server gives the login result"""
        print('_lobby_login_result')

        (accepted, ) = struct.unpack('<B', data[0:1])
        print('accepted = %d' % accepted)

        if accepted:
            (table_size, ) = struct.unpack('<I', data[1:5])
            print('table_size = %d' % table_size)

            offset = struct.calcsize('B') + struct.calcsize('I')
            print('offset = %d' % offset)

            for i in range(table_size):
                (s_size, ) = struct.unpack('<I', data[offset:offset + 4])
                print('s_size = %d' % s_size)
                (t_name, t_id) = struct.unpack('<%dsI' % s_size, data[offset + 4:offset + 4 + s_size + 4])
                print('t_name = %s, t_id = 0x%08x' % (t_name, t_id))

                offset += struct.calcsize('I') + s_size + struct.calcsize('I')

    def _lobby_players_list(self, src_uuid, dst_uuid, data):
        """lobby sends the player list"""
        print('_lobby_players_list')

        (nb_players, ) = struct.unpack('<B', data[0:1])
        print('nb players = %d' % nb_players)
        offset = struct.calcsize('B')

        for i in range(nb_players):
            print('player #%d' % i)

            # player uuid
            (uuid, ) = struct.unpack('<I', data[offset:offset + 4])
            print('\tuuid = 0x%08x' % uuid)
            offset += struct.calcsize('I')

            ident = identity.Identity()
            offset += ident.from_bytes(data[offset:])
            print('\t%s' % ident)

    def run(self):
        """infinite loop handling communication with server"""

        while (True):
            # read server msg
            data = self.sock.recv(1024)

            # parse it
            print('parse: %s' % data)

            header_size = struct.calcsize('<HBIIB')
            (msg_len, version, src_uuid, dst_uuid, cmd) = struct.unpack('<HBIIB', data[:header_size])
            data = data[header_size:]

            print('msg len : %d (%d)' % (msg_len, len(data)))
            print('version : %d' % version)
            print('src uuid: 0x%08x' % src_uuid)
            print('dst uuid: 0x%08x' % dst_uuid)
            print('command : 0x%02x' % cmd)
            print('data    : %s %s' % (data, type(data)))

            self._command[cmd](src_uuid, dst_uuid, data)

            print('\n')
