from AbstractDataAccess import AbstractDataAccess
from Role import Role


class Account():

    @staticmethod
    def LoadEntity(db: AbstractDataAccess):
        db.LoadCSVTable('accounts', [
            ('act_email', 'varchar(50) primary key'),
            ('act_fname', 'varchar(50) not null'),
            ('act_lname', 'varchar(50) not null'),
            ('act_password', 'varchar(20)'),
            ('act_phone', 'varchar(12) unique not null'),
            ('act_address', 'varchar(255) not null'),
            ('role_id', 'integer not null')
        ])

    def __init__(self, db: AbstractDataAccess):
        self.db = db
        self.act_email = ''
        self.act_fname = ''
        self.act_lname = ''
        self.act_password = ''
        self.act_phone = ''
        self.act_address = ''
        self.role_id = -1

    def GetDetail(self):
        self.db.cur.execute(
            'select * from accounts where act_email like ?', [self.act_email])
        act = self.db.cur.fetchone()
        self.act_fname = act['act_fname']
        self.act_lname = act['act_lname']
        self.act_password = act['act_password']
        self.act_phone = act['act_phone']
        self.act_address = act['act_address']
        self.role_id = act['role_id']
    
    @staticmethod
    def PrintAll(db: AbstractDataAccess):
        db.cur.execute('select * from accounts')
        rows = db.cur.fetchall()
        if len(rows) == 0:
            return None
        for r in rows:
            print(' | '.join(map(str, r.values())))

    def Exists(self):
        self.db.cur.execute('''
            select 1
            from accounts
            where act_email like ?
        ''', [self.act_email])
        return self.db.cur.fetchone() is not None

    def Add(self):
        # must validate email and phone
        values = [self.act_email, self.act_fname, self.act_lname, self.act_password,
                  self.act_phone, self.act_address, self.role_id]
        self.db.cur.execute('''
            insert into accounts (act_email, act_fname, act_lname, act_password, act_phone, act_address, role_id)
            values (?, ?, ?, ?, ?, ?, ?)
        ''', values)
        self.db.SaveCSVTable('accounts')

    def Update(self):
        values = [self.act_fname, self.act_lname, self.act_password,
                  self.act_phone, self.act_address, self.role_id, self.act_email]
        self.db.cur.execute('''
            update accounts set
            act_fname = ?,
            act_lname = ?,
            act_password = ?,
            act_phone = ?,
            act_address = ?,
            role_id = ?
            where act_email like ?
        ''', values)
        self.db.SaveCSVTable('accounts')

    def Delete(self):
        self.db.cur.execute('delete from accounts where act_email like ?', [
            self.act_email])
        self.db.SaveCSVTable('accounts')

    def RoleIn(self, *roles: [Role]) -> bool:
        return Role(self.role_id) in roles

    def __str__(self) -> str:
        return (self.act_email + ' | ' +
                self.act_fname + ' | ' +
                self.act_lname + ' | ' +
                self.act_password + ' | ' +
                self.act_phone + ' | ' +
                self.act_address + ' | ' +
                Role(self.role_id))
