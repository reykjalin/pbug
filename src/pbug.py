import argparse
import os

import database_service as db_service
import task_service as task_service


# CONSTANTS #
DB_ENV_VAR = 'PBUG_PROJECT'

# EXIT MESSAGES #
MISSING_ENV_VARIABLE = '$' + DB_ENV_VAR + ' is not set in environment'
FILE_ALREADY_EXISTS = 'The database file specified in $' + DB_ENV_VAR + ' already exists'


def parse_args(args):
    '''Parse arguments given to program and decide what to do'''
    if args.create:
        db = os.environ[DB_ENV_VAR]
        if os.path.isfile(db):
            exit(FILE_ALREADY_EXISTS)
        db_service.create_database(db)
    elif args.add:
        task_service.add_task()
    elif args.list:
        task_service.list_tasks()
    elif args.edit is not None:
        print('Work in progress...')
    elif args.view is not None:
        task_service.view_task(args.view)
    elif args.delete is not None:
        print('Work in progress...')


def main():
    '''Main function'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--create', action='store_true')
    parser.add_argument('-a', '--add', action='store_true')
    parser.add_argument('-l', '--list', action='store_true')
    parser.add_argument('-e', '--edit', type=int)
    parser.add_argument('-v', '--view', type=int)
    parser.add_argument('-d', '--delete', type=int)
    args = parser.parse_args()

    if DB_ENV_VAR not in os.environ.keys():
        exit(MISSING_ENV_VARIABLE)
    parse_args(args)
    return


if __name__ == '__main__':
    main()

