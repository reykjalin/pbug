import os
import platform
import csv

from task import Task

# EXIT MESSAGES #
NO_EDITOR = 'No sane default for an editor available'


def touch(path):
    '''Create empty file'''
    with open(path, 'a'):
        os.utime(path, None)


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


def read_csv_file(file_name, field_names):
    '''Read CSV file and return a list of dicts with CSV data'''
    task_list = []
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=field_names,
                                dialect='excel-tab')
        for row in reader:
            task = Task()
            task.from_dict(row)
            task_list.append(task)
    return task_list


def str_to_bytes(string):
    return bytes(string, 'utf-8')

