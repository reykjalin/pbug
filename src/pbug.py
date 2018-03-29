import argparse
import os
import tempfile
import subprocess


# CONSTANTS #
DB_ENV_VAR = 'PBUG_PROJECT'

# EXIT MESSAGES #
MISSING_ENV_VARIABLE = '$' + DB_ENV_VAR + ' is not set in environment'
FILE_ALREADY_EXISTS = 'The database file specified in $' + DB_ENV_VAR + ' already exists'


def write_task_template(file_pointer):
    file_pointer.write('Id: 0')
    file_pointer.write('Priority: ')
    file_pointer.write('State: ')
    file_pointer.write('Subject: ')
    file_pointer.write('-- Description below --')


def add_task():
    with tempfile.TemporaryFile() as temp:
        temp.write(b'Id: 0\n')
        temp.write(b'Priority: \n')
        temp.write(b'State: \n')
        temp.write(b'Subject: \n')
        temp.write(b'-- Description below --\n')
        temp.seek(0)
        subprocess.run(['nvim', temp.name])
        for line in temp.read().decode():
            print(line, end='')
    return


def edit_task():
    return


def view_task():
    return


def delete_task(id):
    return


def list_tasks(id):
    return


def touch(path):
    '''Create empty file'''
    with open(path, 'a'):
        os.utime(path, None)


def create_database(db):
    '''Initialize empty database'''
    directory = os.path.dirname(db)
    if not os.path.exists(directory):
        os.mkdir(directory)
    touch(db)
    return


def parse_args(args):
    '''Parse arguments given to program and decide what to do'''
    if args.cmd == 'create':
        if DB_ENV_VAR not in os.environ.keys():
            exit(MISSING_ENV_VARIABLE)
        db = os.environ[DB_ENV_VAR]
        if os.path.isfile(db):
            exit(FILE_ALREADY_EXISTS)
        create_database(db)
    elif args.cmd == 'add':
        add_task()
    elif args.cmd == 'edit':
        print('edit')
    elif args.cmd == 'view':
        print('view')
    elif args.cmd == 'delete':
        print('delete')
    elif args.cmd == 'list':
        print('list')


def main():
    '''Main function'''
    choice_list = ['create', 'add', 'edit', 'delete', 'list', 'view']
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', choices=choice_list,
                        help='command stating which action to take: create ' +
                        'database, add task, edit task, delete task')
    args = parser.parse_args()

    parse_args(args)
    return


if __name__ == '__main__':
    main()

