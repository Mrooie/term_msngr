# manage_user.py
import sys

from clcrypto import generate_salt, check_password
from models import User, make_connection
import argparse


def configure_parser():
    new_parser = argparse.ArgumentParser(prog='python manage_user.py')
    new_parser.add_argument('-u', '--username')
    new_parser.add_argument('-p', '--password')
    new_parser.add_argument('-n', '--new-pass')
    new_parser.add_argument('-l', '--list', action='store_true', help='show all users')
    new_parser.add_argument('-d', '--delete', action='store_true', help='delete user')
    new_parser.add_argument('-e', '--edit', action='store_true', help='change password')
    return new_parser


def add_new_user(args, cursor):
    new_user = User.find_by_email(cursor, args.username)
    if not new_user:
        new_user = User()
        new_user.email = args.username
        new_user.username = args.username
        new_user.set_password(args.password, generate_salt())
        new_user.save_to_db(cursor)
    else:
        raise Exception('User exists')


def change_user_password(args, cursor):
    user_to_edit = User.find_by_email(cursor, args.username)
    if user_to_edit and check_password(args.password, user_to_edit.hashed_password):
        user_to_edit.set_password(args.new_pass, generate_salt())
        user_to_edit.save_to_db(cursor)
    else:
        raise Exception('Invalid password or user doesn\'t exist')


def delete_me(args, cursor):
    user_to_delete = User.find_by_email(cursor, args.username)
    if user_to_delete and check_password(args.password, user_to_delete.hashed_password):
        user_to_delete.delete(cursor)
    else:
        raise Exception('Invalid login or password')


def print_all_users(cursor):
    users = User.find_all(cursor)
    print('All users:')
    for user in users:
        print(user.email)


if __name__ == '__main__':
    parser = configure_parser()
    args = parser.parse_args(sys.argv[1:])
    cnx = make_connection()
    cursor = cnx.cursor()
    try:
        if args.username and args.password and not args.edit and not args.delete:
            '''
            If user used -u and -p parameters, but did not use -e or -d parameter - check if user email already exists.
            If not, create new user and password.
            If exists, raise exception.
            '''
            add_new_user(args, cursor)

        elif args.username and args.password and args.edit and args.new_pass:
            '''
            If user used -u and -p parameters, combined with -e parameter - check if password is correct.
            If password is correct - create new password (from param. -n).
            '''
            change_user_password(args, cursor)

        elif args.username and args.password and args.delete:
            '''
            If user used -u and -p parameters, combined with -d parameter - check if password is correct.
            If password is correct - delete user from database.
            '''
            delete_me(args, cursor)

        elif args.list:
            '''
            If user used -l parameter, show all users (without passwords, ofc.!).
            '''
            print_all_users(cursor)

        else:
            '''
            If user used undefined parameters or command, show help screen.
            '''
            parser.print_help()

    finally:
        cursor.close()
        cnx.close()
