from CommandHandler import CommandHandler

if __name__ == '__main__':
    ch = CommandHandler()
    while True:
        cmd = input('> ')
        ch.ProcessCommand(cmd)
