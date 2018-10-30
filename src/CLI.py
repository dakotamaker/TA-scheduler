from DataAccess import DataAccess
from Account import Account
from Course import Course
from Lab import Lab
from CommandHandler import CommandHandler

if __name__ == '__main__':
    db = DataAccess()
    Account.LoadEntity(db)
    Course.LoadEntity(db)
    Lab.LoadEntity(db)
    ch = CommandHandler(db)
    while True:
        cmd = input('> ')
        ch.ProcessCommand(cmd)
