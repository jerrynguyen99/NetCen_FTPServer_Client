import logging
import os.path
import os
import argparse

from hashlib import md5
from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

FTP_ROOT = os.path.join(os.getcwd(),'ftp_root')
LOG_PATH = os.path.join(os.getcwd(),'log/pyftpd.log')

# class DummyMD5Authorizer(DummyAuthorizer):

#     def validate_authentication(self, username, password, handler):
#         if sys.version_info >= (3, 0):
#             password = md5(password.encode('latin1'))
#         hash = md5(password).hexdigest()
#         try:
#             if self.user_table[username]['pwd'] != hash:
#                 raise KeyError
#         except KeyError:
#             raise AuthenticationFailed


def run_ftpd(user, password, host, port, passive, anon):
    
    # user_dir = '.'
    user_dir = os.path.join(FTP_ROOT, user)
    print(os.getcwd)
    if not os.path.isdir(user_dir):
        os.mkdir(user_dir)
    
    # Instantiate a dummy authorizer    
    authorizer = DummyAuthorizer()
    if anon:
        authorizer.add_anonymous(os.getcwd())
    else: 
        authorizer.add_user(user, password, user_dir, perm="elradfmw")

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer
    handler.permit_foreign_addresses = True
    # Define string returned when client connects
    handler.banner = "!~~ pyftpdlib based ftpd ready. Welcome ~~!"
   
    # Redefine logline prefix
    handler.log_prefix = 'XXX [%(username)s]@%(remote_ip)s'

    passive_ports = passive.split('-')
    handler.passive_ports = range(int(passive_ports[0]), int(passive_ports[1]))

    # Log to file
    logging.basicConfig(filename=LOG_PATH, level=logging.DEBUG)

    # Specify a masquerade address and the range of ports to use for passive connections.
    server = FTPServer((host, port), handler)

    # Set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # Start ftp server 
    server.serve_forever()


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--user', default='user',
        help="Username for FTP acess (user will be created)")
    parser.add_argument('--password', default='password',
                        help="Password for FTP user.")
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=21)
    parser.add_argument('--passive', default='3000-3010',
                        help="Range of passive ports")
    parser.add_argument('--anon', action='store_true',
                        help="Allow anonymous access")
    args = parser.parse_args()
    run_ftpd(**vars(args))


if __name__ == '__main__':
    main()
