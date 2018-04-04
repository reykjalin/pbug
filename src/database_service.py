import os
import sys
import csv
from operator import attrgetter
import sqlite3


import util as util
from task import Task

# CONSTANTS #
DB_ENV_VAR = 'PBUG_PROJECT'

# EXIT MESSAGES #
NO_TASK_WITH_ID = '''No task with ID: '''


class DatabaseService():
    def __init__(self, db):
        '''Database service constructer. Connects to the specified DB'''
        self.conn = sqlite3.connect(db)
        self.init_db()

    def init_db(self):
        '''Initializes new database'''
        cmd = 'create table if not exists tasks('
        cmd += 'id integer primary key, '
        cmd += 'priority integer not null on conflict fail, '
        cmd += 'status text not null on conflict fail, '
        cmd += 'subject text not null on conflict fail, '
        cmd += 'description text)'
        self.conn.execute(cmd)
        self.conn.commit()

    def add_task(self, task):
        '''Add the given task to the DB'''
        cmd = 'insert into tasks values (NULL, ?, ?, ?, ?)'
        self.conn.execute(cmd, task.to_tuple())
        self.conn.commit()

    def get_all_tasks(self):
        '''Return a list of all tasks stored in DB'''
        task_list = []
        cmd = 'select id, priority, status, subject, description from tasks '
        cmd += 'order by priority desc'
        for row in self.conn.execute(cmd):
            task = Task()
            task.from_tuple(row)
            task_list.append(task)
        return task_list

    def get_open_tasks(self):
        '''Return a list of all open tasks stored in DB'''
        task_list = []
        cmd = 'select id, priority, status, subject, description from tasks '
        cmd += 'where status = ? '
        cmd += 'order by priority desc'
        status_tuple = ('open', )
        for row in self.conn.execute(cmd, status_tuple):
            task = Task()
            task.from_tuple(row)
            task_list.append(task)
        return task_list

    def get_tasks_with_priority(self, priority):
        '''Return a list of all tasks with priority "priority" stored in DB'''
        task_list = []
        cmd = 'select id, priority, status, subject, description from tasks '
        cmd += 'where priority = ? '
        cmd += 'order by id asc'
        priority_tuple = (priority, )
        for row in self.conn.execute(cmd, priority_tuple):
            task = Task()
            task.from_tuple(row)
            task_list.append(task)
        return task_list


    def find_task_by_id(self, task_id):
        cmd = 'select id, priority, status, subject, description from tasks '
        cmd += 'where id = ?'
        id_tuple = (task_id, )
        for row in self.conn.execute(cmd, id_tuple):
            task = Task()
            task.from_tuple(row)
            return task

    def update_task(self, task):
        cmd = 'update tasks '
        cmd += 'set priority = ?, '
        cmd += 'status = ?, '
        cmd += 'subject = ?, '
        cmd += 'description = ? '
        cmd += 'where id = ?'
        cmd_tuple = task.to_tuple() + (task.id, )
        self.conn.execute(cmd, cmd_tuple)
        self.conn.commit()

    def delete_task_by_id(self, task_id):
        cmd = 'delete from tasks where id = ?'
        id_tuple = (task_id, )
        self.conn.execute(cmd, id_tuple)
        self.conn.commit()

    def close(self):
        self.conn.close()

