import socket
import os
import time
import requests


class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

    def connect_to_server(self):
        self.target_ip = input('Enter ip --> ')
        self.target_port = input('Enter port --> ')

        self.s.connect((self.target_ip, int(self.target_port)))

        self.main()

    def reconnect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.target_ip, int(self.target_port)))

    def main(self):
        while 1:
            file_name = input('Enter file name on server --> ')
            self.s.send(file_name.encode())

            confirmation = self.s.recv(1024)
            if confirmation.decode() == "file-doesn't-exist":
                print("File doesn't exist on server.")

                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
                self.reconnect()

            else:

                write_name = file_name
                url = 'http://bucketvids.com/serve/'+write_name

                if os.path.exists(write_name):
                    # os.stat('somefile.txt')
                    #os.stat_result(st_mode=33188, st_ino=6419862, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=1564, st_atime=1584299303, st_mtime=1584299400, st_ctime=1584299400)
                    # os.stat(write_name).st_size
                    resume_header = (
                        {'Range': f'bytes={os.stat(write_name).st_size}-'})

                    r = requests.get(url, stream=True, headers=resume_header)
                    file_size = int(r.headers.get('content-length', 0))
                    print(f'Size of file: {file_size}'+'\n\n')
                    with open(write_name, 'ab') as f:
                        for chunk in r.iter_content(32 * 1024):
                            f.write(chunk)
                            print('\r'+'Resuming download.........', end="")

                else:
                    r = requests.get(url, stream=True)
                    file_size = int(r.headers.get('content-length', 0))
                    print(f'Size of file: {file_size}'+'\n\n')
                    with open(write_name, 'wb') as f:
                        for chunk in r.iter_content(32 * 1024):
                            f.write(chunk)
                            print('\r'+'Beginning download.........', end="")

                print('\n'+file_name, 'successfully downloaded.')
                if(os.rename(file_name, 'completed_'+file_name)):
                    print('File successfully renamed.')

                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
                self.reconnect()


client = Client()
