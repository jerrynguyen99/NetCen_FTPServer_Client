NetCen_FTPServer_Client

Run client.py with the following command line arguments:
    python client.py [--host] hostname [--port] portname [--user] username [--password] password

By default:
    python client.py

FTP server default: 
    FTP_HOST = ''
    FTP_PORT = 21
    FTP_USER = 'demo-user'
    FTP_PWDS = 'demo-user'

Directory default:
    For FTP source folder directory:
        FTP_UPLOAD = 'upload'
        FTP_DOWNLOAD = 'download'
    For FTP destination folder directory:
        DIR_DOWNLOAD = 'download'
        DIR_UPLOAD = 'upload'