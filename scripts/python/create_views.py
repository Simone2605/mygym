from sqlalchemy import create_engine
from sqlalchemy.sql import text

# create database engine
engine = create_engine('sqlite:///data/mygym.db')

# drop and recreate views via SQL queries
# 1. Who is teaching which class, and at what time and day?
drop_view_classes = """
DROP VIEW IF EXISTS vw_classes
"""

view_classes = """
CREATE VIEW vw_classes AS
SELECT
    weekdays.name AS weekday,
    classes.time,
    persons.surname,
    persons.forename,
    classtypes.name AS classtype,
    rooms.name AS room
FROM
    persons
    INNER JOIN employees ON persons.id = employees.person_id
    INNER JOIN trainers ON employees.id = trainers.employee_id
    INNER JOIN classofferings ON trainers.id = classofferings.trainer_id
    INNER JOIN classes ON classofferings.id = classes.classoffering_id
    INNER JOIN weekdays ON classes.weekday_id = weekdays.id
    INNER JOIN classtypes ON classofferings.classtype_id = classtypes.id
    INNER JOIN rooms ON classtypes.room_id = rooms.id
ORDER BY
    weekdays.id,
    classes.time;    
"""

# 2. How many participants are registered for each class, and what is the maximum number of participants?
drop_view_registrations = """
DROP VIEW IF EXISTS vw_registrations
"""

view_registrations = """
CREATE VIEW vw_registrations AS
SELECT
    weekdays.name AS weekday,
    classes.time,
    classtypes.name AS classtype,
    COUNT(registrations.id) AS registrations,
    classtypes.maxparticipants AS "max. participants"
FROM
    classes
    INNER JOIN weekdays ON classes.weekday_id = weekdays.id
    INNER JOIN registrations ON classes.id = registrations.class_id
    INNER JOIN classofferings ON classes.classoffering_id = classofferings.id
    INNER JOIN classtypes ON classofferings.classtype_id = classtypes.id
GROUP BY
    weekdays.name,
    classes.time,
    classtypes.name,
    classes.weekday_id,
    classtypes.maxparticipants
ORDER BY
    classes.weekday_id,
    classes.time;    
"""

# 3. Which trainers are participating as students in classes led by other trainers?
drop_view_trainersasparticipants = """
DROP VIEW IF EXISTS vw_trainersasparticipants
"""

view_trainersasparticipants = """
CREATE VIEW vw_trainersasparticipants AS
SELECT
    attending_persons.surname,
    attending_persons.forename,
    classtypes.name AS classtype,
    weekdays.name AS weekday,
    classes.time,
    instructor_persons.forename AS trainer
FROM
    registrations
    INNER JOIN members ON registrations.member_id = members.id
    INNER JOIN persons AS attending_persons ON members.person_id = attending_persons.id
    INNER JOIN employees AS attending_employees ON attending_persons.id = attending_employees.person_id
    INNER JOIN trainers AS attending_trainers ON attending_employees.id = attending_trainers.employee_id
    INNER JOIN classes ON registrations.class_id = classes.id
    INNER JOIN classofferings ON classes.classoffering_id = classofferings.id
    INNER JOIN classtypes ON classofferings.classtype_id = classtypes.id
    INNER JOIN weekdays ON classes.weekday_id = weekdays.id
    INNER JOIN trainers AS instructor_trainers ON classofferings.trainer_id = instructor_trainers.id
    INNER JOIN employees AS instructor_employees ON instructor_trainers.employee_id = instructor_employees.id
    INNER JOIN persons AS instructor_persons ON instructor_employees.person_id = instructor_persons.id
ORDER BY
    attending_persons.surname;    
"""

# 4. Who is currently employed as an instructor and leading classes?
drop_view_employeesasinstructors = """
DROP VIEW IF EXISTS vw_employeesasinstructors
"""

view_employeesasinstructors = """
CREATE VIEW vw_employeesasinstructors AS
SELECT
    persons.surname,
    persons.forename,
    classtypes.name AS classtype,
    weekdays.name AS weekday,
    classes.time
FROM
    classes
    INNER JOIN classofferings ON classes.classoffering_id = classofferings.id
    INNER JOIN classtypes ON classofferings.classtype_id = classtypes.id
    INNER JOIN weekdays ON classes.weekday_id = weekdays.id
    LEFT JOIN trainers ON classofferings.trainer_id = trainers.id
    LEFT JOIN employees ON trainers.employee_id = employees.id
    INNER JOIN persons ON employees.person_id = persons.id
WHERE
    persons.leavedate IS NULL
ORDER BY
    persons.surname,
    classtypes.name;    
"""

# 5. Who is participating in the yoga classes, and since when?
drop_view_yogaparticipants = """
DROP VIEW IF EXISTS vw_yogaparticipants
"""

view_yogaparticipants = """
CREATE VIEW vw_yogaparticipants AS
SELECT
    persons.surname,
    persons.forename,
    classtypes.name AS classtype,
    weekdays.name AS weekday,
    classes.time,
    registrations.startdate AS "participant since"
FROM
    persons
    INNER JOIN members ON persons.id = members.person_id
    INNER JOIN registrations ON members.id = registrations.member_id
    INNER JOIN classes ON registrations.class_id = classes.id
    INNER JOIN classofferings ON classes.classoffering_id = classofferings.id
    INNER JOIN classtypes ON classofferings.classtype_id = classtypes.id
    INNER JOIN weekdays ON classes.weekday_id = weekdays.id
WHERE
    classtypes.name = "Yoga"
    AND (registrations.enddate IS NULL OR registrations.enddate < DATE('now'))
ORDER BY
    weekdays.id,
    classes.time,
    registrations.startdate;    
"""

# execute SQL queries to create/drop views
with engine.connect() as connection:
    connection.execute(text(drop_view_classes))
    connection.execute(text(view_classes))
    connection.execute(text(drop_view_registrations))
    connection.execute(text(view_registrations))
    connection.execute(text(drop_view_trainersasparticipants))
    connection.execute(text(view_trainersasparticipants))
    connection.execute(text(drop_view_employeesasinstructors))
    connection.execute(text(view_employeesasinstructors))
    connection.execute(text(drop_view_yogaparticipants))
    connection.execute(text(view_yogaparticipants))

# %%
