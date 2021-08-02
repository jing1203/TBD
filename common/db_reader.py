#coding:utf-8
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker,mapper
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class print_record(Base):
    __tablename__ = 'print_record'
    id = Column(INTEGER, primary_key=True)
    act_material = Column(REAL)
    act_time = Column(INTEGER)
    est_material=Column(REAL)
    est_time=Column(INTEGER)
    fail_num=Column(INTEGER)
    filename=Column(TEXT)
    material=Column(TEXT)
    object_num=Column(INTEGER)
    print_id=Column(TEXT)
    start_time=Column(INTEGER)
    thickness=Column(INTEGER)

    def __repr__(self):
        return "<print_record(id='%s', act_material='%s', act_time='%s')>" \
			% (self.id, self.act_material,self.act_time)

class dbhellper():
    def __init__(self,base,dburl):
        self.db=create_engine(dburl)
        self.base=base
        self.db.echo=False
        self.base.metadata.create_all(self.db)
        Session = sessionmaker(bind=self.db)
        self.session = Session()

    def Get_counts(self):
        scount=self.session.query(func.count(print_record.id)).scalar()
        print(scount)

    def closeall(self):
        s=''
        try:
            self.session.close()
            s='cok'
        except Exception as e:
            s=str(e)
        return s

spath="sqlite://///home//heygears//.ds//db//hg_record.db"
dh=dbhellper(Base,spath)
dh.Get_counts()