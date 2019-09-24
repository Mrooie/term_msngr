import sys

from clcrypto import generate_salt, check_password
from models import User, make_connection
import argparse

def configure_parser():
    new_parser = argparse.ArgumentParser(prog='python manage_user.py')
    new_parser.add_argument('-u', '--username')
    new_parser.add_argument('-p', '--password')
    new_parser.add_argument('-l', '--list', action='store_true', help='żądanie wylistowania wszystkich wiadomości')
    new_parser.add_argument('-s', '--send', dest='message', help='treść wiadomości')
    new_parser.add_argument('-t', '--to', dest='to', help='adresat awiadomości')
    return new_parser


def print_all_message(args, cursor):
    pass


def send_message_to_user(args, cursor):
    pass


if __name__ == '__main__':
    parser = configure_parser()
    args = parser.parse_args(sys.argv[1:])
    cnx = make_connection()
    cursor = cnx.cursor()
    try:
        if args.username and args.password and args.list:
            '''
            Jeśli użytkownik zażądał wylistowania komunikatów ( -l), należy sprawdzić jego login i hasło pobrane z 
            parametrów -u oraz -p, następnie pobrać z bazy wszystkie komunikaty do tego użytkownika i pokazać je w 
            kolejności od najnowszego do najstarszego.
            '''
            print_all_message(args, cursor)
        elif args.username and args.password and args.message and args.to:
            '''
            Jeśli użytkownik chce wysłać komunikat do innego ( -s), należy sprawdzić jego login i hasło pobrane z 
            parametrów -u i -p, następnie sprawdzić, czy podano adresata i czy adresat istnieje ( -t), następnie 
            zapisać w bazie danych komunikat pobrany parametrem -s).
            '''
            send_message_to_user(args, cursor)
        else:
            '''
            Jeśli użytkownik wprowadził parametry w konfiguracji innej niż podane na slajdach, ma mu się wyświetlić
            komunikaty pomocy.
            '''
            parser.print_help()
    finally:
        cursor.close()
        cnx.close()
