import argparse
import os
import sys

from database_service import DatabaseService
import task_service as task_service


# CONSTANTS #
DB_ENV_VAR = 'PBUG_PROJECT'

# EXIT MESSAGES #
MISSING_ENV_VARIABLE = '$' + DB_ENV_VAR + ' is not set in environment'
FILE_ALREADY_EXISTS = 'The database file specified in $' + DB_ENV_VAR + ' already exists'


def parse_args(args):
    '''Parse arguments given to program and decide what to do'''
    if args.init:
        db = os.environ[DB_ENV_VAR]
        if os.path.isfile(db):
            sys.exit(FILE_ALREADY_EXISTS)
        DatabaseService(db)
        print('Successfully initialized database')
    elif args.add:
        task_service.add_task()
    elif args.list:
        task_service.list_tasks()
    elif args.edit is not None:
        task_service.edit_task(args.edit)
        print('Successfully edited task with ID: ' + str(args.edit))
    elif args.view is not None:
        task_service.view_task(args.view)
    elif args.delete is not None:
        task_service.delete_task(args.delete)
        print('Successfully deleted task with ID: ' + str(args.delete))
    elif args.close is not None:
        task_service.close_task(args.close)
        print('Successfully closed task with ID: ' + str(args.close))


def main():
    '''Main function'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--init', action='store_true',
                        help='Initialize database')
    parser.add_argument('-a', '--add', action='store_true',
                        help='Add new task')
    parser.add_argument('-l', '--list', action='store_true',
                        help='List all available tasks')
    parser.add_argument('-e', '--edit', type=int,
                        help='Edit the task specified by the ID nr. EDIT')
    parser.add_argument('-v', '--view', type=int,
                        help='View the task specified by the ID nr. VIEW')
    parser.add_argument('-d', '--delete', type=int,
                        help='Delete the task specified by the ID nr. DELETE')
    parser.add_argument('-c', '--close', type=int,
                        help='Close the task specified by the ID nr. DELETE')
    args = parser.parse_args()

    if DB_ENV_VAR not in os.environ.keys():
        sys.exit(MISSING_ENV_VARIABLE)
    parse_args(args)
    return


if __name__ == '__main__':
    main()

