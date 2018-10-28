from DataAccess import DataAccess


class Course():

    @staticmethod
    def LoadEntity(db):
        db.LoadCSVTable('courses', [('course_id', 'integer primary key'),
                                    ('course_name', 'varchar(50) not null'),
                                    ('instructor_email', 'varchar(50)')])

    def __init__(self, db):
        self.db = db
        self.course_id = -1
        self.course_name = ''
        self.instructor_email = ''

    def GetDetail(self):
        db.cur.execute(
            'select * from courses where course_id like ?', [self.course_id])
        c = db.cur.fetchone()
        self.course_name = c['course_name']
        self.instructor_email = c['instructor_email']

    def Add(self):
        values = [self.course_name, self.instructor_email]
        db.cur.execute('''
            insert into courses (course_name, instructor_email)
            values (?, ?)
        ''', values)
        db.SaveCSVTable('courses')

    def Update(self):
        values = [self.course_name, self.instructor_email, self.course_id]
        db.cur.execute('''
            update courses set
            course_name = ?,
            instructor_email = ?
            where course_id = ?
            ''', values)
        db.SaveCSVTable('courses')

    def __str__(self):
        return (str(self.course_id) + ' - ' +
                self.course_name + ' - ' +
                self.instructor_email)


if __name__ == '__main__':
    db = DataAccess()
    Course.LoadEntity(db)
    c = Course(db)
    c.course_id = 1
    c.GetDetail()
    print(c)
    c.course_name = 'Data Structures'
    c.Update()
    c = Course(db)
    c.course_name = 'My course asdfg'
    c.instructor_email = 'instruct@school.edu'
    c.Add()
