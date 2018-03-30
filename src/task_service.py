import os
import tempfile
import subprocess
from operator import attrgetter

import util
import database_service as db_service
from task import Task

# CONSTANTS #
DB_ENV_VAR = 'PBUG_PROJECT'

# EXIT MESSAGES #
INCORRECT_FORMAT = '''Task wasn't formatted correctly'''


def write_task_template(file_pointer):
    file_pointer.write(b'Id: ' +
                       util.str_to_bytes(str(db_service.get_next_id())) +
                       util.str_to_bytes(os.linesep))
    file_pointer.write(b'Priority: 0' + util.str_to_bytes(os.linesep))
    file_pointer.write(b'State: open' + util.str_to_bytes(os.linesep))
    file_pointer.write(b'Subject: ' + util.str_to_bytes(os.linesep))
    file_pointer.write(b'-- Description below --' +
                       util.str_to_bytes(os.linesep))
    file_pointer.seek(0)


def get_new_task():
    '''Open temporary file to get task information'''
    # Open temporary file to get information on task
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        write_task_template(temp)

    # Start editor so user can edit informaiton
    subprocess.run([util.get_editor(), temp.name])

    # Get task information
    lines = []
    with open(temp.name, 'r') as temp:
        for line in temp:
            lines.append(line.strip())

    # Delete temporary file
    os.remove(temp.name)
    new_task = Task()
    new_task.from_list(lines)
    return new_task


def add_task():
    '''Add task to database'''
    new_task = get_new_task()

    field_names = ['id', 'priority', 'state', 'subject', 'description']
    db = os.environ[DB_ENV_VAR]
    db_service.write_task_to_csv(db, field_names, new_task)


def print_task_list(task_list):
    '''Print list of tasks given a list of dicts with task information'''
    print('Id\tPrior.\tState\tSubject')
    for task in task_list:
        print(task.to_task_list_row())


def list_tasks():
    '''Print list of tasks in database'''
    # Read DB
    db = os.environ[DB_ENV_VAR]
    field_names = ['id', 'priority', 'state', 'subject', 'description']
    task_list = util.read_csv_file(db, field_names)

    # Sort items in DB by priority
    sorted_task_list = sorted(task_list, key=attrgetter('priority'), reverse=True)

    # Print items in DB
    print_task_list(sorted_task_list)


def edit_task():
    return


def view_task(task_id):
    # Read DB
    db = os.environ[DB_ENV_VAR]
    field_names = ['id', 'priority', 'state', 'subject', 'description']
    task_list = util.read_csv_file(db, field_names)

    task = db_service.find_task_by_id(task_list, task_id)
    print(task)

    return


def delete_task(task_id):
    return

