import os
import csv

import util as util

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
    for task in task_list:
        if task.id == task_id:
            return task

    exit(NO_TASK_WITH_ID + str(task_id))


def write_task_to_csv(file_name, field_names, task):
    # TODO Figure out how to get \n into csv file
    with open(file_name, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, dialect='excel-tab',
                                fieldnames=field_names)
        writer.writerow(task.to_dict())

