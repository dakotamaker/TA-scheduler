from DataAccess import DataAccess


class Lab():

    @staticmethod
    def LoadEntity(db):
        db.LoadCSVTable('labs', [('lab_id', 'integer primary key'),
                                 ('lab_name', 'varchar(50) not null'),
                                 ('course_id', 'varchar(50) not null'),
                                 ('ta_email', 'varchar(50)')])

    def __init__(self, db):
        self.db = db
        self.lab_id = -1
        self.lab_name = ''
        self.course_id = -1
        self.ta_email = ''

    def GetDetail(self):
        db.cur.execute(
            'select * from labs where lab_id like ?', [self.lab_id])
        l = db.cur.fetchone()
        self.lab_name = l['lab_name']
        self.course_id = l['course_id']
        self.ta_email = l['ta_email']

    def Add(self):
        values = [self.lab_name, self.course_id, self.ta_email]
        db.cur.execute('''
            insert into labs (lab_name, course_id, ta_email)
            values (?, ?, ?)
        ''', values)
        db.SaveCSVTable('labs')

    def Update(self):
        values = [self.lab_name, self.course_id, self.ta_email, self.lab_id]
        db.cur.execute('''
            update labs set
            lab_name = ?,
            course_id = ?,
            ta_email = ?
            where lab_id = ?
            ''', values)
        db.SaveCSVTable('labs')

    def __str__(self):
        return (str(self.lab_id) + ' - ' +
                self.lab_name + ' - ' +
                self.course_id + ' - ' +
                self.ta_email)


if __name__ == '__main__':
    db = DataAccess()
    Lab.LoadEntity(db)
    l = Lab(db)
    l.lab_id = 1
    l.GetDetail()
    print(l)
    l.lab_name = 'Ayyy Lab'
    l.Update()
    l = Lab(db)
    l.lab_name = 'Test Lab Add'
    l.course_id = 3
    l.ta_email = 'hhhh@hhhh.com'
    l.Add()
