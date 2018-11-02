from AbstractDataAccess import AbstractDataAccess


class Course():

    @staticmethod
    def LoadEntity(db: AbstractDataAccess):
        db.LoadCSVTable('courses', [
            ('course_id', 'integer primary key'),
            ('course_name', 'varchar(50) unique not null'),
            ('instructor_email', 'varchar(50)')
        ])
        db.LoadCSVTable('course_ta_xref', [
            ('course_id', 'integer not null'),
            ('ta_email', 'varchar(50) not null')
        ])

    def __init__(self, db: AbstractDataAccess):
        self.db = db
        self.course_id = -1
        self.course_name = ''
        self.instructor_email = ''

    def GetDetail(self):
        if self.course_id > -1:
            self.db.cur.execute(
                'select * from courses where course_id = ?', [self.course_id])
        else:
            self.db.cur.execute(
                'select * from courses where course_name like ?', [self.course_name])
        c = self.db.cur.fetchone()
        self.course_id = c['course_id']
        self.course_name = c['course_name']
        self.instructor_email = c['instructor_email']

    @staticmethod
    def PrintAll(db: AbstractDataAccess):
        db.cur.execute('select * from courses')
        rows = db.cur.fetchall()
        if len(rows) == 0:
            return
        for r in rows:
            print(' | '.join(map(str, r.values())))

    def Exists(self) -> bool:
        self.db.cur.execute('''
            select 1
            from courses
            where course_name like ?
        ''', [self.course_name])
        return self.db.cur.fetchone() is not None

    def Add(self):
        # needs to validate course name
        values = [self.course_name, self.instructor_email]
        self.db.cur.execute('''
            insert into courses (course_name, instructor_email)
            values (?, ?)
        ''', values)
        self.course_id = self.db.cur.lastrowid
        self.db.SaveCSVTable('courses')

    def Update(self):
        values = [self.course_name, self.instructor_email, self.course_id]
        self.db.cur.execute('''
            update courses set
            course_name = ?,
            instructor_email = ?
            where course_id = ?
        ''', values)
        self.db.SaveCSVTable('courses')

    def Delete(self):
        self.db.cur.execute('delete from courses where course_id = ?', [
            self.course_id])
        self.db.SaveCSVTable('courses')

    def AssignTA(self, ta_email):
        # needs validation to make sure ta_email exists and is a TA and that the TA isn't already assigned to this course
        self.db.cur.execute('insert into course_ta_xref (course_id, ta_email) values (?, ?)', [
            self.course_id, ta_email])
        self.db.SaveCSVTable('course_ta_xref')

    def UnassignTA(self, ta_email):
        # this should fail if the TA is still assigned to labs
        self.db.cur.execute('delete from course_ta_xref where course_id = ? and ta_email = ?', [
            self.course_id, ta_email])
        self.db.SaveCSVTable('course_ta_xref')

    def __str__(self) -> str:
        return (str(self.course_id) + ' | ' +
                self.course_name + ' | ' +
                self.instructor_email)
