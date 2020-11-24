import socket
import os
import time



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
                mode='wb'
                ts = str(time.time())
                # fileSize=os.path.getsize(file_name)
                write_name = file_name
                # print(write_name)
                # exit()
                if os.path.exists(write_name):
                    #os.remove(write_name)
                    mode='ab'                    
                file=open(write_name, mode)
                bytes_read = 0
                print('Startng position is '+str(file.tell())+'\n\n')
                if(mode == 'wb'):
                    pos=file.tell()
                    file.seek(pos,0) 
                    #file=open(write_name, mode)                       
                    print('Resuming download.........')
                    print('Startng position is '+str(pos)+'\n\n')


                with file:
                    while 1:
                        data = self.s.recv(1024)
                        bytes_read += len(data)
                        #print("File "+str(write_name)+" is "+str(fileSize)+" bytes total.")
                        print('\r'+"Total bytes read: " +
                              str(bytes_read), end='')
                        #total_per = 100 * float(bytes_read)/float(long(audioSize)+long(videoSize))
                        if not data:
                            break

                        file.write(data)

                print('\n'+file_name, 'successfully downloaded.')
                if(os.rename(file_name,'completed_'+file_name)):
                    print('File successfully renamed.')

                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
                self.reconnect()


client = Client()
