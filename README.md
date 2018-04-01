# pBug
ToDo tracking system inspired by [bug](http://vicerveza.homeunix.net/~viric/soft/bug/)


## Usage  
Help message:
```bash
$ python pbug.py -h
usage: pbug.py [-h] [-i] [-a] [-l] [-e EDIT] [-v VIEW] [-d DELETE] [-c CLOSE]

optional arguments:
  -h, --help            show this help message and exit
  -i, --init            Initialize database
  -a, --add             Add new task
  -l, --list            List all available tasks
  -e EDIT, --edit EDIT  Edit the task specified by the ID nr. EDIT
  -v VIEW, --view VIEW  View the task specified by the ID nr. VIEW
  -d DELETE, --delete DELETE
                        Delete the task specified by the ID nr. DELETE
  -c CLOSE, --close CLOSE
                        Close the task specified by the ID nr. DELETE
```

1. Make sure the environment variable `PBUG_PROJECT` is set to a .db file
  * For your first time use, the file does not have to exist
2. If this is the first time running the program you have to initialize the database:
```bash
python pbug.py -i
```
3. Use the flags to set up a database


### Adding a task  
When adding a task run `python pbug.py -a`.
The program will read your `EDITOR` environment variable to determine which text editor will be used to write the task.
If `EDITOR` is not set it will guess at a default editor:
* `notepad.exe` for Windows
* `ed` for Mac and Linux

Use the editor to modify the task, and save the file.
When the editor is closed the task will be added to the database.


## Examples  
```bash
$ python pbug.py -l
Id      Prior.  State   Subject
1       10      open    test
2       4       open    eMed
```

```bash
$ python pbug.py -v 1
Id: 1
Priority: 10
State: open
Subject: test
-- Description Below --
this is
a
multiline
description
```
