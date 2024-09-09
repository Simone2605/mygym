
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db import Base, Country, City, Person, Member, Employee, Trainer, Room, ClassType, ClassOffering, Weekday, Class, Registration
import csv
from datetime import datetime

# create database engine
engine = create_engine('sqlite:///mygym.db')

# drop and recreate all existing tables
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# create session
Session = sessionmaker(bind=engine)
session = Session()

# open csv-files and add each entry into corresponding table
with open('example data/countries.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    countries = [Country(name=row[0],
                         abbreviation=row[1],
                         code=row[2]) for row in reader]

session.add_all(countries)

with open('example data/cities.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    cities = [City(postcode=row[0],
                   name=row[1],
                   country_id=row[2]) for row in reader]

session.add_all(cities)

with open('example data/persons.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    persons = [Person(surname=row[0],
                      forename=row[1],
                      birthdate=datetime.strptime(row[2], '%Y-%m-%d').date(),
                      street=row[3],
                      housenumber=row[4],
                      city_id=row[5],
                      landline=row[6],
                      mobile=row[7],
                      email=row[8],
                      enterdate=datetime.strptime(row[9], '%Y-%m-%d').date(),
                      leavedate=datetime.strptime(row[10], '%Y-%m-%d').date() if row[10] and row[10] != 'NULL' else None) for row in reader]

session.add_all(persons)

with open('example data/members.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    members = [Member(person_id=row[0]) for row in reader]

session.add_all(members)

with open('example data/employees.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    employees = [Employee(person_id=row[0]) for row in reader]

session.add_all(employees)

with open('example data/trainers.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    trainers = [Trainer(employee_id=row[0]) for row in reader]

session.add_all(trainers)

with open('example data/rooms.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    rooms = [Room(name=row[0]) for row in reader]

session.add_all(rooms)

with open('example data/classtypes.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    classtypes = [ClassType(name=row[0],
                            room_id=row[1],
                            maxparticipants=row[2]) for row in reader]

session.add_all(classtypes)

with open('example data/classofferings.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    classofferings = [ClassOffering(classtype_id=row[0],
                                    trainer_id=row[1]) for row in reader]

session.add_all(classofferings)

with open('example data/weekdays.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    weekdays = [Weekday(name=row[0], abbreviation=row[1]) for row in reader]

session.add_all(weekdays)


with open('example data/classes.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    classes = [Class(classoffering_id=row[0],
                     weekday_id=row[1],
                     time=datetime.strptime(row[2], '%H:%M:%S').time()) for row in reader]

session.add_all(classes)

with open('example data/registrations.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    registrations = [Registration(class_id=row[0],
                                  member_id=row[1],
                                  startdate=datetime.strptime(row[2], '%Y-%m-%d').date(),
                                  enddate=datetime.strptime(row[3], '%Y-%m-%d').date() if row[3] and row[3] != 'NULL' else None)
                     for row in reader]

session.add_all(registrations)

# save changes
session.commit()
