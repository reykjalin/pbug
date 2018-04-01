import os
import sys
import tempfile
import subprocess

import util
from database_service import DatabaseService
from task import Task

# CONSTANTS #
DB_ENV_VAR = 'PBUG_PROJECT'

# EXIT MESSAGES #
INCORRECT_FORMAT = '''Task wasn't formatted correctly'''
NOT_INT = '''Value provided was not an integer'''
NO_SUCH_TASK = '''No task with ID: '''


def get_new_task():
    '''Open temporary file to get task information'''
    # Prepare task
    task = Task()
    # task.id = db_service.get_next_id()
    task.id = 0
    task.priority = 0

    # Open temporary file to get information on task
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        util.write_task_to_binary_file(temp, task)

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

    # field_names = ['id', 'priority', 'state', 'subject', 'description']
    db = os.environ[DB_ENV_VAR]
    db_service = DatabaseService(db)
    print(new_task.to_tuple())
    db_service.add_task(new_task)
    # db_service.write_task_to_csv(db, field_names, new_task)


def print_task_list(task_list):
    '''Print list of tasks given a list of dicts with task information'''
    print('Id\tPrior.\tState\tSubject')
    for task in task_list:
        print(task.to_task_list_row())


def list_tasks():
    '''Print list of tasks in database'''
    # Read DB
    db = os.environ[DB_ENV_VAR]
    db_service = DatabaseService(db)
    print_task_list(db_service.get_all_tasks())


def edit_task():
    return


def view_task(task_id):
    # Read DB
    db = os.environ[DB_ENV_VAR]
    db_service = DatabaseService(db)

    task = db_service.find_task_by_id(task_id)
    if task is not None:
        print(task)
    else:
        sys.exit(NO_SUCH_TASK + str(task_id))


def delete_task(task_id):
    return

