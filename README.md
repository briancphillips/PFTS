# Bittorrent like client
A bittorrent like file transfer server written in Python 3, that allows the user to download files located on the server. The server can handle and serve multiple clients at the same time and send files in the same/child directories. The client can also resume broken downloads.  Simply click CTRL-C while downloading a file in the client, then just restart the client and enter the filename that was interrupted and the download will resume.

## Usage
- Run the server.py file, entering the port you wish for the server to run on.
- Users can run the client.py file and connect to the server by entering the IP address and port displayed on your server.
- A user can enter the name of a file on the server (in the same folder as the server.py) and download that file - the file will appear in the same directory as the client.py file, named completed_+filename.

## Requirements
- Python 3.7+
- Socket Module (standard library)
- Threading Module (standard library)
- OS Module (standard library)


