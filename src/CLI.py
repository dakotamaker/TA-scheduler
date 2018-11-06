from src.DataAccess import DataAccess
from src.Account import Account
from src.Course import Course
from src.Lab import Lab
from src.CommandHandler import CommandHandler

if __name__ == '__main__':
    db = DataAccess()
    Account.LoadEntity(db)
    Course.LoadEntity(db)
    Lab.LoadEntity(db)
    ch = CommandHandler(db)
    try:
        while True:
            cmd = input('> ')
            ch.ProcessCommand(cmd)
    except KeyError:
        print('Invalid command')
        while True:
            cmd = input('> ')
            ch.ProcessCommand(cmd)
