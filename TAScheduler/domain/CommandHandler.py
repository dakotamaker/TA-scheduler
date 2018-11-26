from ..models import *
from .Role import Role
from .ErrorMessages import ErrorMessages
import shlex


class CommandHandler:

    def __init__(self):
        self.currentUser = None
        Account.objects.get_or_create(act_email='supervisor@email.com', act_fname='supervisor', act_lname='user',
                                      act_password='password', act_address='1234 Main St., Milwaukee, WI',
                                      act_phone='123-123-1234', role_id=4, act_officelocation="none",
                                      act_officehours="none")

    def ProcessCommand(self, cmdString: str) -> str:
        try:
            cmd = shlex.split(cmdString)  # don't split quoted substrings
        except:
            return 'Badly formatted command'

        handler = {
            'help': self._HelpHandler,
            'login': self._LoginHandler,
            'logout': self._LogoutHandler,
            'notify': self._NotifyHandler,
            'edit': self._EditHandler,
            'create': {
                'user': self._CreateUserHandler,
                'course': self._CreateCourseHandler,
                'lab': self._CreateLabHandler
            },
            'assign': {
                'course': {
                    'ta': self._AssignCourseTAHandler,
                    'instructor': self._AssignCourseInstructorHandler
                },
                'lab': self._AssignLabHandler
            },
            'delete': {
                'user': self._DeleteUserHandler,
                'course': self._DeleteCourseHandler,
                'lab': self._DeleteLabHandler
            },
            'view': {
                'user': self._ViewUserHandler,
                'course': self._ViewCourseHandler,
                'lab': self._ViewLabHandler
            },
            'list': {
                'users': self._ListUsersHandler,
                'tas': self._ListTAsHandler,
                'courses': self._ListCoursesHandler,
                'labs': self._ListLabsHandler
            }
        }
        while type(handler) is dict:
            try:
                handler = handler[cmd[0].lower()]
            except Exception as e:
                return 'Invalid command'
            cmd.pop(0)
        try:
            return handler(cmd)
        except Exception as e:
            return 'Handler error - %s' % e

    def _HelpHandler(self, cmd: [str]):
        return 'this is the help\nmenu right here\nnew line'

    def _LoginHandler(self, cmd: [str]):
        if len(cmd) != 2:
            return ErrorMessages.INVALID_NUM_OF_ARGUMENTS
        try:
            a = Account.objects.get(act_email=cmd[0])
        except Exception:
            return 'Given email does not belong to an existing user'
        if a.act_password != '':
            if a.act_password == cmd[1]:
                self.currentUser = a
                return 'Logged in as %s' % cmd[0]
            else:
                return 'Invalid credentials'
        else:
            a.act_password = cmd[1]
            a.save()
            return 'Logged in as %s, your new password has been saved' % cmd[0]

    def _LogoutHandler(self, cmd: [str]):
        if not self.currentUser:
            return 'No user is logged in'
        self.currentUser = None
        return 'Logged out'

    def _EditHandler(self, cmd: [str]):
        if self.currentUser is None:
            return ErrorMessages.NOT_LOGGED_IN
        elif self.currentUser.RoleIn(Role.Supervisor) or self.currentUser.RoleIn(Role.Administrator):
            if len(cmd) != 1 and len(cmd) != 3:
                return ErrorMessages.INVALID_NUM_OF_ARGUMENTS
            try:
                a = Account.objects.get(
                    act_email=self.currentUser.act_email if cmd[0] != 'user' else cmd[1])
                attr = cmd[0] if cmd[0] != 'user' else cmd[2]
            except Exception:
                return "Given email does not belong to an existing user"
            new_value = attr.split(":")
            if len(new_value) != 2:
                return 'To edit an account you need a semicolon'
            a.__setattr__(new_value[0], new_value[1])
            a.save()
            return "Edit successful"
        else:
            if len(cmd) != 1:
                return 'Only supervisors or admins can edit another user'
            attr = cmd[0]
            new_value = attr.split(":")
            if len(new_value) != 2:
                return 'To edit an account you need a semicolon'
            self.currentUser.__setattr__(new_value[0], new_value[1])
            self.currentUser.save()
            return "Edit successful"

    def _NotifyHandler(self, cmd: [str]):
        if not self.currentUser or self.currentUser.RoleIn(Role.TA):
            return 'TAs cannot send notifications'
        elif self.currentUser.RoleIn(Role.Instructor):
            # Logic to look for TA that is in the instructor's class, to implement later
            return
        if len(cmd) != 3:
            return ErrorMessages.INVALID_NUM_OF_ARGUMENTS
        user = Account.objects.get(act_email=cmd[0])
        if user:
            return 'Notification email sent to %s!' % user.act_email
        else:
            return 'This user does not exist'

    def _CreateUserHandler(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return 'Must be logged in as an Administrator or Supervisor'
        if len(cmd) != 6 and len(cmd) != 8:
            return ErrorMessages.INVALID_NUM_OF_ARGUMENTS
        acc = Account.objects.filter(act_email=cmd[0])
        if acc:
            return 'User already exists'
        acc = Account()
        acc.act_email = cmd[0]
        acc.act_fname = cmd[1]
        acc.act_lname = cmd[2]
        acc.role_id = cmd[3]
        acc.act_phone = cmd[4]
        acc.act_address = cmd[5]

        if len(cmd) == 6:
            acc.act_officehours = "none"
            acc.act_officelocation = "none"
        else:
            acc.act_officelocation = cmd[6]
            acc.act_officehours = cmd[7]

        acc.save()
        return 'User added'

    def _CreateCourseHandler(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return 'Must be logged in as an Administrator or Supervisor'
        if len(cmd) != 1:
            return ErrorMessages.INVALID_NUM_OF_ARGUMENTS
        c = Course.objects.filter(course_name=cmd[0])
        if c:
            return 'Course already exists'
        c = Course(course_name=cmd[0])
        c.save()
        return 'Course added'

    def _CreateLabHandler(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return 'Must be logged in as an Administrator or Supervisor'
        if len(cmd) != 2:
            return ErrorMessages.INVALID_NUM_OF_ARGUMENTS
        c = Course.objects.filter(course_name=cmd[0]).first()
        if not c:
            return 'A course with that name does not exist'
        l = Lab.objects.filter(lab_name=cmd[1], course=c).first()
        if l:
            return 'A lab with that name already exists for this course'
        l = Lab()
        l.lab_name = cmd[1]
        l.course = c
        l.save()
        return 'Lab created'

    def _AssignCourseTAHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return 'Must be logged in as an Administrator or Supervisor'
        if len(cmd) != 2:
            return ErrorMessages.INVALID_NUM_OF_ARGUMENTS
        c = Course.objects.filter(course_name=cmd[0]).first()
        if not c:
            return 'A course with that name does not exist'
        a = Account.objects.filter(act_email=cmd[1]).first()
        if not a or not a.RoleIn(Role.TA):
            return 'Only existing TAs can be assigned to the course'
        c.tas.add(a)
        return 'TA assigned to course'

    def _AssignCourseInstructorHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return 'Must be logged in as an Administrator or Supervisor'
        if len(cmd) != 2:
            return ErrorMessages.INVALID_NUM_OF_ARGUMENTS
        try:
            c = Course.objects.get(course_name=cmd[0])
        except Exception:
            return 'This course does not exist'
        if c.instructor != None:
            return 'This course already has an instructor'
        try:
            a = Account.objects.get(act_email=cmd[1])
        except Exception:
            return 'This user does not exist'
        if a.role_id != 2:
            return 'Assignee must be an instructor'
        c.instructor = a
        c.save()
        return 'Instructor assigned to course'

    def _AssignLabHandler(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return 'Must be logged in as an Administrator or Supervisor'
        if len(cmd) != 3:
            return ErrorMessages.INVALID_NUM_OF_ARGUMENTS
        c = Course.objects.filter(course_name=cmd[0]).first()
        if not c:
            return 'A course with that name does not exist'
        l = Lab.objects.filter(lab_name=cmd[1], course=c).first()
        if not l:
            return 'Lab for that course does not exist'
        a = c.tas.filter(act_email=cmd[2]).first()
        if not a:
            return 'Only TAs assigned to the course can be assigned to the lab'
        l.ta = a
        l.save()
        return 'Assigned TA to lab'

    def _DeleteUserHandler(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return 'Must be logged in as an Administrator or Supervisor'
        if len(cmd) != 1:
            return ErrorMessages.INVALID_NUM_OF_ARGUMENTS
        try:
            a = Account.objects.get(act_email=cmd[0])
        except Exception:
            return 'Given email does not belong to an existing user'
        a.delete()
        return 'Deleted user %s' % cmd[0]

    def _DeleteCourseHandler(self, cmd: [str]):
        return 'Delete course:' + cmd

    def _DeleteLabHandler(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return 'Must be logged in as an Administrator or Supervisor'
        if len(cmd) != 2:
            return ErrorMessages.INVALID_NUM_OF_ARGUMENTS
        c = Course.objects.filter(course_name=cmd[0]).first()
        if not c:
            return 'A course with that name does not exist'
        l = Lab.objects.filter(lab_name=cmd[1], course=c).first()
        if not l:
            return 'A lab with that name does not exist for this course'
        l.delete()
        return 'Lab deleted'

    def _ViewUserHandler(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return 'Must be logged in as an Administrator or a Supervisor'
        if len(cmd) != 1:
            return ErrorMessages.INVALID_NUM_OF_ARGUMENTS

    def _ViewCourseHandler(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.RoleIn(Role.Instructor, Role.Administrator,
                                                               Role.Supervisor):
            return 'Must be logged in as an Instructor, Administrator, or a Supervisor'
        if len(cmd) != 1:
            return ErrorMessages.INVALID_NUM_OF_ARGUMENTS

    def _ViewLabHandler(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.RoleIn(Role.Instructor, Role.Administrator,
                                                               Role.Supervisor):
            return 'Must be logged in as an Instructor, Administrator, or a Supervisor'
        if len(cmd) != 1:
            return ErrorMessages.INVALID_NUM_OF_ARGUMENTS

    def _ListUsersHandler(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return 'Must be logged in as an Administrator or a Supervisor'

    def _ListTAsHandler(self, cmd: [str]):
        if not self.currentUser:
            return 'Must be logged in to access TA list.'
        a = Account.objects.filter(role_id=Role.TA)
        s = ""
        for ta in a:
            s += "\n" + ta.act_fname
            s += " " + ta.act_lname + ": "
            c = Course.objects.filter(tas__act_email=ta.act_email)
            for course in c:
                s += course.course_name + "\t"
            l = Lab.objects.filter(ta__act_email=ta.act_email)
            for lab in l:
                s += lab.lab_name + "\t"

        return 'List TAs: ' + s

    def _ListCoursesHandler(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.RoleIn(Role.Instructor, Role.Administrator,
                                                               Role.Supervisor):
            return 'Must be logged in as an Instructor, Administrator, or a Supervisor'

    def _ListLabsHandler(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.RoleIn(Role.Instructor, Role.Administrator,
                                                               Role.Supervisor):
            return 'Must be logged in as an Instructor, Administrator, or a Supervisor'
