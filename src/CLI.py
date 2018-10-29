from CommandHandler import CommandHandler

if __name__ == '__main__':
    ch = CommandHandler()
    cmd = input('> ')
    ch.ProcessCommand(cmd)