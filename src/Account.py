from DataAccess import DataAccess

class Account():

    def __init__(self, db):
        self.db = db
        self.act_email = ''
        self.act_fname = ''
        self.act_lname = ''
        self.act_password = ''
        self.act_phone = ''
        self.role_id = -1

    def GetDetail(self):
        db.cur.execute('select * from accounts where act_email like ?', [self.act_email])
        act = db.cur.fetchall()[0]
        self.act_email = act['act_email']
        self.act_fname = act['act_fname']
        self.act_lname = act['act_lname']
        self.act_password = act['act_password']
        self.act_phone = act['act_phone']
        self.role_id = act['role_id']

    def Update(self):
        values = [self.act_fname, self.act_lname, self.act_password, self.act_phone, self.role_id]
        db.cur.execute("update accounts set act_fname = ?, act_lname = ?, act_password = ?, act_phone = ?, role_id = ? where act_email = '%s'" % self.act_email, values)
        db.SaveCSVTable('accounts')

    def __str__(self):
        return (self.act_email + ' - ' + 
                self.act_fname + ' - ' + 
                self.act_lname + ' - ' + 
                self.act_password + ' - ' + 
                self.act_phone + ' - ' + 
                str(self.role_id))

if __name__ == '__main__':
    db = DataAccess()
    db.LoadCSVTable('accounts', [('act_email', 'varchar(50) primary key'),
                                    ('act_fname', 'varchar(50) not null'),
                                    ('act_lname', 'varchar(50) not null'),
                                    ('act_password', 'varchar(20)'),
                                    ('act_phone', 'varchar(12) unique not null'),
                                    ('role_id', 'integer not null')])
    act = Account(db)
    act.act_email = 'email@gmail.com'
    act.GetDetail()
    act.act_fname = 'asdfasdasdads'
    act.Update()

    db.SaveCSVTable('accounts')