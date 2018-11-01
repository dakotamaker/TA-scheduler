from AbstractDataAccess import AbstractDataAccess


class Lab():

    @staticmethod
    def LoadEntity(db: AbstractDataAccess):
        db.LoadCSVTable('labs', [
            ('lab_id', 'integer primary key'),
            ('lab_name', 'varchar(50) not null'),
            ('course_id', 'varchar(50) not null'),
            ('ta_email', 'varchar(50)')
        ])

    def __init__(self, db: AbstractDataAccess):
        self.db = db
        self.lab_id = -1
        self.lab_name = ''
        self.course_id = -1
        self.ta_email = ''

    def GetDetail(self):
        self.db.cur.execute(
            'select * from labs where lab_id like ?', [self.lab_id])
        l = self.db.cur.fetchone()
        self.lab_name = l['lab_name']
        self.course_id = l['course_id']
        self.ta_email = l['ta_email']

    
    @staticmethod
    def PrintAll(db: AbstractDataAccess):
        db.cur.execute('select * from labs')
        rows = db.cur.fetchall()
        if len(rows) == 0:
            return
        for r in rows:
            print(' | '.join(map(str, r.values())))

    def Add(self):
        # needs validation to make sure course and TA exist (and that the TA is in fact a TA)
        values = [self.lab_name, self.course_id, self.ta_email]
        self.db.cur.execute('''
            insert into labs (lab_name, course_id, ta_email)
            values (?, ?, ?)
        ''', values)
        self.lab_id = self.db.cur.lastrowid
        self.db.SaveCSVTable('labs')

    def Update(self):
        values = [self.lab_name, self.course_id, self.ta_email, self.lab_id]
        self.db.cur.execute('''
            update labs set
            lab_name = ?,
            course_id = ?,
            ta_email = ?
            where lab_id = ?
        ''', values)
        self.db.SaveCSVTable('labs')

    def Delete(self):
        self.db.cur.execute('delete from labs where lab_id = ?', [self.lab_id])
        self.db.SaveCSVTable('labs')

    def __str__(self) -> str:
        return (str(self.lab_id) + ' - ' +
                self.lab_name + ' - ' +
                str(self.course_id) + ' - ' +
                self.ta_email)
