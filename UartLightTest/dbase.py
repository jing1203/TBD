
#coding:utf-8
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker,mapper
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
"""
光机测试数据存储
"""
class PRecord(Base):
	__tablename__ = 'PRecord'
	id = Column(Integer, primary_key=True)
	lvalue = Column(String(64))
	ltmp = Column(String(64))
	ldate=Column(String(64))

	def __repr__(self):
		return "<PRecord(lvalue='%s', ltmp='%s', ldate='%s')>" \
			% (self.lvalue, self.ltmp,self.ldate)
		
class xmldbhelpper():
	def __init__(self,base,dburl):
		self.db=create_engine(dburl)
		self.base=base
		self.db.echo=False
		self.base.metadata.create_all(self.db)
		Session = sessionmaker(bind=self.db)
		self.session = Session()
		
	def AddPRecord(self,precode):
		s=''
		try:
			self.session.add(precode)
			self.session.commit()
			s='aok'
		except Exception as e:
			s=str(e)
		return s
		
	def QueryP(self,p):
		ilist = self.session.query(PRecord).filter(PRecord.pname==p).all()
		return ilist

	def QueryAll(self):
		pagination = self.session.query(PRecord).order_by(PRecord.id.desc()).all()
		return pagination
		
	def closeall(self):
		s=''
		try:
			self.session.close()
			s='cok'
		except Exception as e:
			s=str(e)
		return s
		
def InitDb(url):
	db=xmldbhelpper(Base,url)
	return db
	
def AddP(pcode,db):
	s=db.AddPRecord(pcode)
	return s

def CloseDb(db):
	s=db.closeall()
	return s

def QueryAll(db):
	p=db.QueryAll()
	return p

"""
import time
#from exhelpper import Exhelp
spath="sqlite:///test.db"
db=InitDb(spath)
rl=QueryAll(db)
print(rl)
ex=Exhelp()
ex.MakeSaveEx("光机",rl)
"""

