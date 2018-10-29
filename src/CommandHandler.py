import shlex


class CommandHandler:

    def ProcessCommand(self, cmdString):
        cmd = shlex.split(cmdString)  # don't split quoted substrings
        handler = {
            'login': self.LoginHandler,
            'logout': self.LogoutHandler,
            'notify': self.NotifyHandler,
            'create': {
                'user': self.CreateUserHandler,
                'course': self.CreateCourseHandler,
                'lab': self.CreateLabHandler
            },
            'assign': {
                'course': self.AssignCourseHandler,
                'lab': self.AssignLabHandler
            },
            'delete': {
                'user': self.DeleteUserHandler,
                'course': self.DeleteCourseHandler,
                'lab': self.DeleteLabHandler
            }
        }
        while type(handler) is dict:
            handler = handler[cmd[0]]
            cmd.pop(0)
        handler(cmd)

    def LoginHandler(self, cmd):
        print('Login:', cmd)

    def LogoutHandler(self, cmd):
        print('Log out:', cmd)

    def NotifyHandler(self, cmd):
        print('Nofity:', cmd)

    def CreateUserHandler(self, cmd):
        print('Create user:', cmd)

    def CreateCourseHandler(self, cmd):
        print('Create course:', cmd)

    def CreateLabHandler(self, cmd):
        print('Create lab:', cmd)

    def AssignCourseHandler(self, cmd):
        print('Assign course:', cmd)

    def AssignLabHandler(self, cmd):
        print('Assign lab:', cmd)

    def DeleteUserHandler(self, cmd):
        print('Delete user:', cmd)

    def DeleteCourseHandler(self, cmd):
        print('Delete course:', cmd)

    def DeleteLabHandler(self, cmd):
        print('Delete lab:', cmd)