import os
import csv
from operator import attrgetter


import util as util

# CONSTANTS #
DB_ENV_VAR = 'PBUG_PROJECT'

# EXIT MESSAGES #
NO_TASK_WITH_ID = '''No task with ID: '''


def create_database(db):
    '''Initialize empty database'''
    directory = os.path.dirname(db)
    if not os.path.exists(directory):
        os.mkdir(directory)
    util.touch(db)
    return


def find_task_by_id(task_list, task_id):
    '''Find task by a given ID'''
    for task in task_list:
        if task.id == task_id:
            return task

    exit(NO_TASK_WITH_ID + str(task_id))


def get_tasks_from_db():
    '''Read tasks from CSV file in no particular order'''
    db = os.environ[DB_ENV_VAR]
    field_names = ['id', 'priority', 'state', 'subject', 'description']
    return util.read_csv_file(db, field_names)


def sort_by_attr(list_to_sort, attr, reverse=True):
    '''Sorts task list by specific field'''
    return sorted(list_to_sort, key=attrgetter(attr), reverse=reverse)


def get_task_list():
    '''Returns sorted list of tasks'''
    return sort_by_attr(get_tasks_from_db(), 'priority')


def get_biggest_id():
    '''Get highest ID in CSV file'''
    return sort_by_attr(get_tasks_from_db(), 'id')[0].id


def get_next_id():
    '''Return next ID for a task'''
    return get_biggest_id() + 1


def write_task_to_csv(file_name, field_names, task):
    # TODO Figure out how to get \n into csv file
    with open(file_name, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, dialect='excel-tab',
                                fieldnames=field_names)
        writer.writerow(task.to_dict())

