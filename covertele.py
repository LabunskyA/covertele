# LabunskyA wrote this file
# Distributed under the Simplified BSD License

import socks, sys, getpass, string

from telethon import functions, errors, sync
from cochannel import CovertChannel, CoverChannelStateAPI

api_id = 0
api_hash = ''

proxy = None
# proxy = (socks.HTTP, "163.172.220.221", 8888)


class TelegramBlockingAPI(CoverChannelStateAPI):
    def __init__(self, user, phone: string = None, on_code=None, on_2fa=None, proxy=None):
        client = sync.TelegramClient(user, api_id, api_hash, proxy=proxy)
        client.connect()

        if not client.is_user_authorized():
            if phone is None:
                phone = input("Enter your phone number: ")
            client.send_code_request(phone)

            try:
                if on_code is None:
                    client.sign_in(phone, input("Enter auth code: "))
                else:
                    client.sign_in(phone, on_code())
            except errors.SessionPasswordNeededError:
                if on_2fa is None:
                    client.sign_in(password=getpass.getpass())
                else:
                    client.sign_in(password=on_2fa())
        self.__client = client

    def send_bit(self, bit: bool, dest: string):
        if bit:
            return self.__client(functions.contacts.BlockRequest(id=dest))
        else:
            return self.__client(functions.contacts.UnblockRequest(id=dest))

    def receive_bit(self, src: string) -> bool:
        status = self.__client(functions.users.GetUsersRequest([src]))[0].status
        if status is None:
            return True
        else:
            return False

    def get_state(self, dest) -> bool:
        return self.__client(functions.users.GetFullUserRequest(dest)).blocked


def usage():
    print("Usage: python3", sys.argv[0], "[-s/-r] [your username] [other username] [message]")
    print("If there is no connection (nothing is happening), try setting proxy in the scrypt file")


if len(sys.argv) != 4 and sys.argv[1] == "-r" or len(sys.argv) < 5 and sys.argv[1] == "-s":
    usage()
    exit(-1)

user = sys.argv[2]
friend = sys.argv[3]

channel = CovertChannel(TelegramBlockingAPI(user, proxy=proxy), friend, verbose=True)

if sys.argv[1] == "-s":
    message = ""
    i = 4
    while i < len(sys.argv) - 1:
        message += sys.argv[i] + " "
        i += 1
    message += sys.argv[i]

    print("Started message transmission...")
    channel.send(message)
    print("Done, exiting...")
elif sys.argv[1] == '-r':
    print("Listening for the message...")
    message = channel.receive()
    print("Automatically decoded:", message)

exit(0)
