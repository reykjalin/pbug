import os
import sys

# EXIT MESSAGES #
INCORRECT_FORMAT = '''Task wasn't formatted correctly'''


class Task():
    '''Class that defines the Task object'''
    def __init__(self):
        self.id = 0
        self.priority = 0
        self.state = ''
        self.subject = ''
        self.description = ''

    def __str__(self):
        out = 'Id: ' + str(self.id) + os.linesep
        out += 'Priority: ' + str(self.priority) + os.linesep
        out += 'State: ' + self.state + os.linesep
        out += 'Subject: ' + self.subject + os.linesep
        out += '-- Description Below --' + os.linesep
        out += self.description
        return out

    def from_list(self, task_list):
        try:
            self.id = int(task_list[0].split(':')[1].strip())
            self.priority = int(task_list[1].split(':')[1].strip())
            self.state = task_list[2].split(':')[1].strip()
            self.subject = task_list[3].split(':')[1].strip()
            self.description = os.linesep.join(task_list[5:])
        except ValueError as err:
            sys.exit(INCORRECT_FORMAT)

        if self.state == '' or self.subject == '':
            sys.exit(INCORRECT_FORMAT)

    def from_dict(self, task_dict):
        try:
            self.id = int(task_dict['id'])
            self.priority = int(task_dict['priority'])
            self.state = task_dict['state']
            self.subject = task_dict['subject']
            self.description = task_dict['description']
        except ValueError as err:
            sys.exit(INCORRECT_FORMAT)

        if self.state == '' or self.subject == '':
            sys.exit(INCORRECT_FORMAT)

    def to_task_list_row(self):
        ret = str(self.id) + '\t' + str(self.priority) + '\t'
        ret += self.state + '\t' + self.subject
        return ret

    def to_dict(self):
        ret = {}
        ret['id'] = self.id
        ret['priority'] = self.priority
        ret['state'] = self.state
        ret['subject'] = self.subject
        ret['description'] = self.description
        return ret

