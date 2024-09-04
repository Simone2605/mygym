from sqlalchemy import create_engine, Column, Integer, String, Date, Time, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

# create a base class
Base = declarative_base()


# define tables
class Person(Base):
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True, nullable=False)
    surname = Column(String(50), nullable=False)
    forename = Column(String(50), nullable=False)
    birthdate = Column(Date, nullable=False)
    street = Column(String(50), nullable=False)
    housenumber = Column(String(5), nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    landline = Column(String(20))
    mobile = Column(String(20), unique=True)
    email = Column(String(254), unique=True)
    enterdate = Column(Date, nullable=False, default=datetime.today)
    leavedate = Column(Date)

    city = relationship('City', back_populates='persons')
    member = relationship('Member', back_populates='person')
    employee = relationship('Employee', back_populates='person')

    __table_args__ = (
        CheckConstraint('leavedate IS NULL OR leavedate > enterdate', name='check_leavedate')
    )

    def __repr__(self):
        return f"<Person(id={self.id}, forename='{self.forename}', surname='{self.surname}', email='{self.email}')>"


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, nullable=False)
    postcode = Column(String(10), nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)

    country = relationship('Country', back_populates='cities')
    persons = relationship('Person', back_populates='city')

    def __repr__(self):
        return f"<City(id={self.id}, name='{self.name}', postcode='{self.postcode}')>"


class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False, unique=True)
    abbreviation = Column(String(2), unique=True)
    code = Column(String(5), unique=True)

    cities = relationship('City', back_populates='country')

    def __repr__(self):
        return f"<Country(id={self.id}, name='{self.name}', abbreviation='{self.abbreviation}')>"


class Member(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True, nullable=False)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False, unique=True)

    person = relationship('Person', back_populates='member')
    registrations = relationship('Registration', back_populates='member')

    def __repr__(self):
        return f"<Member(id={self.id}, person_id={self.person_id})>"


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, nullable=False)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False, unique=True)

    person = relationship('Person', back_populates='employee')
    trainer = relationship('Trainer', back_populates='employee')

    def __repr__(self):
        return f"<Employee(id={self.id}, person_id={self.person_id})>"


class Trainer(Base):
    __tablename__ = 'trainers'

    id = Column(Integer, primary_key=True, nullable=False)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False, unique=True)

    employee = relationship('Employee', back_populates='trainer')
    classofferings = relationship('ClassOffering', back_populates='trainer')

    def __repr__(self):
        return f"<Trainer(id={self.id}, employee_id={self.employee_id})>"


class ClassType(Base):
    __tablename__ = 'classtypes'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False, unique=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    maxparticipants = Column(Integer, nullable=False)

    room = relationship('Room', back_populates='classtypes')
    classofferings = relationship('ClassOffering', back_populates='classtype')

    def __repr__(self):
        return f"<ClassType(id={self.id}, name='{self.name}', maxparticipants={self.maxparticipants})>"


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(20), nullable=False, unique=True)

    classtypes = relationship('ClassType', back_populates='room')

    def __repr__(self):
        return f"<Room(id={self.id}, name='{self.name}')>"


class ClassOffering(Base):
    __tablename__ = 'classofferings'

    id = Column(Integer, primary_key=True, nullable=False)
    classtype_id = Column(Integer, ForeignKey('classtypes.id'), nullable=False)
    trainer_id = Column(Integer, ForeignKey('trainers.id'), nullable=False)

    classtype = relationship('ClassType', back_populates='classofferings')
    trainer = relationship('Trainer', back_populates='classofferings')
    classes = relationship('Class', back_populates='classoffering')

    __table_args__ = (
        UniqueConstraint('classtype_id', 'trainer_id', name='uix_classtype_trainer')
    )

    def __repr__(self):
        return f"<ClassOffering(id={self.id}, classtype_id={self.classtype_id}, trainer_id={self.trainer_id})>"


class Class(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True, nullable=False)
    classoffering_id = Column(Integer, ForeignKey('classofferings.id'), nullable=False)
    weekday_id = Column(Integer, ForeignKey('weekdays.id'), nullable=False)
    time = Column(Time, nullable=False)

    classoffering = relationship('ClassOffering', back_populates='classes')
    weekday = relationship('Weekday', back_populates='classes')
    registrations = relationship('Registrations', back_populates='class_')

    __table_args__ = (
        UniqueConstraint('classoffering_id', 'weekday_id', 'time', name='uix_classoffering_weekday_time')
    )

    def __repr__(self):
        return (f"<Class(id={self.id}, classoffering_id={self.classoffering_id}, weekday_id={self.weekday_id},"
                f"time={self.time})>")


class Weekday(Base):
    __tablename__ = 'weekdays'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(10), nullable=False, unique=True)
    abbreviation = Column(String(2), nullable=False, unique=True)

    classes = relationship('Class', back_populates='weekday')

    def __repr__(self):
        return f"<Weekday(id={self.id}, name='{self.name}', abbreviation='{self.abbreviation}')>"


class Registration(Base):
    __tablename__ = 'registrations'

    id = Column(Integer, primary_key=True, nullable=False)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=False)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=False)
    startdate = Column(Date, nullable=False)
    enddate = Column(Date)

    class_ = relationship('Class', back_populates='registrations')
    member = relationship('Member', back_populates='registrations')

    __table_args__ = (
        UniqueConstraint('class_id', 'member_id', name='uix_class_member'),
        CheckConstraint('enddate IS NULL OR enddate > startdate', name='check_enddate')
    )

    def __repr__(self):
        return (f"<Registration(id={self.id}, class_id={self.class_id}, member_id={self.member_id},"
                f"startdate={self.startdate}, enddate={self.enddate})>")


# create database engine
engine = create_engine('sqlite:///mygym.db')

# create tables
Base.metadata.create_all(engine)

# %%
