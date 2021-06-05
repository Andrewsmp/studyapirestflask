from sqlalchemy import create_engine, Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///activity.db' , echo=True)
db_session = scoped_session(sessionmaker(bind=engine, autocommit=False))

Base = declarative_base()
Base.query = db_session.query_property()

class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    name = Column(String(60), index=True)
    age = Column(Integer)

    def save(self):
        db_session.add(self)
        db_session.commit()
    
    def remove(self):
        db_session.delete(self)
        db_session.commit()


    def __repr__(self) -> str:
        return 'Id: {} - Name: {} - Age: {}'.format(self.id, self.name, self.age)

class Activity(Base):
    __tablename__ = 'activity'

    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    status = Column(String(10))
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship('Person')

    def save(self):
        db_session.add(self)
        db_session.commit()
    
    def remove(self):
        db_session.delete(self)
        db_session.commit()

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__=='__main__':
    init_db()
