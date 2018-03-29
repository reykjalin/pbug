import argparse
import os
import tempfile
import subprocess
import platform
import csv


# CONSTANTS #
DB_ENV_VAR = 'PBUG_PROJECT'

# EXIT MESSAGES #
MISSING_ENV_VARIABLE = '$' + DB_ENV_VAR + ' is not set in environment'
FILE_ALREADY_EXISTS = 'The database file specified in $' + DB_ENV_VAR + ' already exists'
NO_EDITOR = 'No sane default for an editor available'
INCORRECT_FORMAT = '''Task wasn't formatted correctly'''


def write_task_template(file_pointer):
    file_pointer.write(b'Id: 0' + bytes(os.linesep, 'utf-8'))
    file_pointer.write(b'Priority: ' + bytes(os.linesep, 'utf-8'))
    file_pointer.write(b'State: ' + bytes(os.linesep, 'utf-8'))
    file_pointer.write(b'Subject: ' + bytes(os.linesep, 'utf-8'))
    file_pointer.write(b'-- Description below --' + bytes(os.linesep, 'utf-8'))
    file_pointer.seek(0)


def get_editor():
    '''Attempt to find a sane default for text editor if $EDITOR environment
    variable is not defined'''
    if 'EDITOR' in os.environ.keys():
        return os.environ['EDITOR']
    else:
        if platform.system() == 'Windows':
            return 'notepad'
        elif platform.system() == 'Linux':
            return 'ed'
        else:
            exit(NO_EDITOR)


def get_new_task():
    '''Open temporary file to get task information'''
    # Open temporary file to get information on task
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        write_task_template(temp)

    # Start editor so user can edit informaiton
    subprocess.run([get_editor(), temp.name])

    # Get task information
    lines = []
    with open(temp.name, 'r') as temp:
        for line in temp:
            lines.append(line.strip())

    # Delete temporary file
    os.remove(temp.name)
    return lines


def add_task():
    '''Add task to database'''
    task_info = get_new_task()

    task_dict = {}
    try:
        task_dict['id'] = int(task_info[0].split(':')[1].strip())
        task_dict['priority'] = int(task_info[1].split(':')[1].strip())
        task_dict['state'] = task_info[2].split(':')[1].strip()
        task_dict['subject'] = task_info[3].split(':')[1].strip()
        task_dict['description'] = os.linesep.join(task_info[5:])
    except ValueError as e:
        exit(INCORRECT_FORMAT)

    # TODO save to file


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

    if DB_ENV_VAR not in os.environ.keys():
        exit(MISSING_ENV_VARIABLE)
    parse_args(args)
    return


if __name__ == '__main__':
    main()

