from ftplib import FTP
import time
import sys

toolbar_width = 40

# Exception raised when an error or invalid response is received
class Error(Exception): pass
class error_reply(Error): pass          # unexpected [123]xx reply
class error_temp(Error): pass           # 4xx errors
class error_perm(Error): pass           # 5xx errors
class error_proto(Error): pass          # response does not begin with [1-5]

HOST = 'localhost'
PORT = 2121
server = FTP()
server.connect(HOST,PORT)
if (server.login('user', 'password') == '230 Login successful.'):  #connect successfully
    files = []
    try:
        files = server.nlst()
    except FTP.error_perm as resp:
        if str(resp) == "550 No files found":
            print ("No files in this directory")
        else:
            raise
    print('All files available:')
    i=0
    while i < len(files):
        print ('Press',i, 'to download', files[i])
        i+=1
    choosenFileIndex = input().split()
    print(choosenFileIndex)
    while (choosenFileIndex > i-1) :
        choosenFileIndex = int(input('Please input correct index\n').split()[0])
    print('**** Start downloading ****')
    sys.stdout.write("[%s]" % (" " * toolbar_width)) #set up progressbar
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['
    for i in range(toolbar_width):
        fhandle = open(files[choosenFileIndex], 'wb')      #set up path to download file here
        server.retrbinary('RETR ' + files[choosenFileIndex], fhandle.write)
        fhandle.close()
        # update the bar
        sys.stdout.write("=")
        sys.stdout.flush()
    print('\n**** Download finished ****')