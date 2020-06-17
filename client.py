from ftplib import FTP
import sys
import os
import argparse

toolbar_width = 40

# Exception raised when an error or invalid response is received


class Error(Exception):
    pass


class error_reply(Error):
    pass          # unexpected [123]xx reply


class error_temp(Error):
    pass                                # 4xx errors


class error_perm(Error):
    pass           # 5xx errors


class error_proto(Error):
    pass                                # response does not begin with [1-5]


FTP_HOST = ''
FTP_PORT = 21
FTP_USER = 'demo-user'
FTP_PWDS = 'demo-user'
FTP_UPLOAD = ''
FTP_DOWNLOAD = 'download'
DIR_DOWNLOAD = 'download'
DIR_UPLOAD = 'upload'


def showLogo():
    print('***********************************************************************************************')
    print("888b    888          888     .d8888b.                        8888888888 88888888888 8888888b.  ")
    print("8888b   888          888    d88P  Y88b                       888            888     888   Y88b ")
    print("88888b  888          888    888    888                       888            888     888    888 ")
    print("888Y88b 888  .d88b.  888888 888         .d88b.  88888b.      8888888        888     888   d88P ")
    print("888 Y88b888 d8P  Y8b 888    888        d8P  Y8b 888 '88b     888            888     8888888P'  ")
    print("888  Y88888 88888888 888    888    888 88888888 888  888     888            888     888        ")
    print("888   Y8888 Y8b.     Y88b.  Y88b  d88P Y8b.     888  888     888            888     888        ")
    print("888    Y888  'Y8888   'Y888  'Y8888P'   'Y8888  888  888     888            888     888        ")
    print('***********************************************************************************************')


def showMenu():
    print('******************************************** Menu *********************************************')
    print('Welcome to FTP Transferer. Select a job')
    print('0. Show session')
    print('1. Show FTP directory')
    print('2. Upload via FTP')
    print('3. Download via FTP')
    print('4. Say Goodbye!')


def showSession(session):
    print('****************************************** Sesssion *******************************************')
    global FTP_HOST, FTP_PORT, FTP_USER, FTP_PWDS
    print('Host: ' + FTP_HOST)
    print('Port: ' + str(FTP_PORT))
    print('User: ' + FTP_USER)
    print('Password: ' + FTP_PWDS)


def welcome(session):
    showLogo()
    while(True):
        showMenu()
        choosenIndex = int(input('Enter a number: ').split()[0])
        while (choosenIndex > 4):
            choosenIndex = int(
                input('Please input correct index: ').split()[0])
        if choosenIndex == 0:
            showSession(session)
        if choosenIndex == 1:
            getDirectory(session)
        if choosenIndex == 2:
            sendFile(session)
        if choosenIndex == 3:
            recvFile(session)
        if choosenIndex == 4:
            bye(session)
            return


def connect(user, password, host, port):
    server = FTP()
    server.connect(host, port)
    state = server.login(user, password)
    global FTP_HOST, FTP_PORT, FTP_USER, FTP_PWDS
    FTP_HOST = host
    FTP_PORT = port
    FTP_USER = user
    FTP_PWDS = password
    msg = '230 User ' + user + ' logged in.'
    if (state == msg):  # connect successfully
        return server
    print(state)
    return None


def bye(session):
    print("Good Bye! See You ...")
    session.quit()


def getDirectory(session):
    print('**************************************** FTP Directory ***************************************')
    data = []
    session.dir(data.append)
    for line in data:
        print(line)

# Data in 'upload' folder can be uploaded


def sendFile(session):
    print('*************************************** FTP Uploader ***************************************')
    files = os.listdir(DIR_UPLOAD)
    print('All files available:')
    i = 0
    while i < len(files):
        print('Press', i, 'to download', files[i])
        i += 1
    choosenFileIndex = int(input('Enter a number: ').split()[0])
    while (choosenFileIndex > i-1):
        choosenFileIndex = int(
            input('Please input correct index: ').split()[0])
    print('**** Start uploading ****')
    print("YOUR CHOICE: " + files[choosenFileIndex])
    sys.stdout.write("[%s]" % (" " * toolbar_width))  # set up progressbar
    sys.stdout.flush()
    # return to start of line, after '['
    sys.stdout.write("\b" * (toolbar_width+1))
    for i in range(toolbar_width):
        # set up path to upload file here
        dir = os.path.join(DIR_UPLOAD, files[choosenFileIndex])
        # print(dir)
        fhandle = open(dir, 'rb')
        session.storbinary(
            'STOR ' + FTP_UPLOAD, fhandle)
        fhandle.close()
        # update the bar
        sys.stdout.write(u"\u2588")
        sys.stdout.flush()
    print('\n**** Upload finished ****')


    # dir = os.path.join(FTP_UPLOAD, filename)
    # print(dir)
    # file = open(filename, "rb")
    # session.storbinary("STOR " + dir, file)
    # file.close()

# Data will be downloaded in 'download' folder


def recvFile(session):
    print('*************************************** FTP Downloader ***************************************')
    files = []
    try:
        files = session.nlst(FTP_DOWNLOAD)
    except FTP.error_perm as resp:
        if str(resp) == "550 No files found":
            print("No files in this directory")
        else:
            raise
    print('All files available:')
    i = 0
    while i < len(files):
        print('Press', i, 'to download', files[i])
        i += 1
    choosenFileIndex = int(input('Enter a number: ').split()[0])
    while (choosenFileIndex > i-1):
        choosenFileIndex = int(
            input('Please input correct index: ').split()[0])
    print('**** Start downloading ****')
    print("YOUR CHOICE: " + files[choosenFileIndex])
    sys.stdout.write("[%s]" % (" " * toolbar_width))  # set up progressbar
    sys.stdout.flush()
    # return to start of line, after '['
    sys.std4out.write("\b" * (toolbar_width+1))
    for i in range(toolbar_width):
        # set up path to download file here
        dir = os.path.join(DIR_DOWNLOAD, files[choosenFileIndex])
        # print(dir)
        fhandle = open(dir, 'wb')
        session.retrbinary(
            'RETR ' + dir, fhandle.write)
        fhandle.close()
        # update the bar
        sys.stdout.write(u"\u2588")
        sys.stdout.flush()
    print('\n**** Download finished ****')


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--user', default='demo-user',
        help="Username for FTP access")
    parser.add_argument('--password', default='demo-user',
                        help="Password for FTP user.")
    parser.add_argument('--host', default='demo.wftpserver.com')
    parser.add_argument('--port', type=int, default=21)

    args = parser.parse_args()
    session = connect(**vars(args))
    welcome(session)


if __name__ == '__main__':
    main()
