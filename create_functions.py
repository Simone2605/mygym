from sqlalchemy import create_engine, Table, MetaData, select, func, and_
from datetime import datetime

# create database engine
engine = create_engine('sqlite:///mygym.db')

# load metadata
metadata = MetaData()
persons = Table('persons', metadata, autoload_with=engine)
members = Table('members', metadata, autoload_with=engine)
employees = Table('employees', metadata, autoload_with=engine)
trainers = Table('trainers', metadata, autoload_with=engine)
classes = Table('classes', metadata, autoload_with=engine)
classtypes = Table('classtypes', metadata, autoload_with=engine)
classofferings = Table('classofferings', metadata, autoload_with=engine)
registrations = Table('registrations', metadata, autoload_with=engine)
weekdays = Table('weekdays', metadata, autoload_with=engine)

# generalized functions to check existence of records
def check_exists(table, record_id, engine):
    with engine.connect() as connection:
        query = select(table.c.id).where(table.c.id == record_id)
        result = connection.execute(query).fetchone()
        return result is not None


def check_member_exists(member_id):
    return check_exists(members, member_id, engine)


def check_trainer_exists(trainer_id):
    return check_exists(trainers, trainer_id, engine)


def check_class_exists(class_id):
    return check_exists(classes, class_id, engine)


def check_weekday_exists(weekday_id):
    return check_exists(weekdays, weekday_id, engine)


# generalized functions to get record information
def get_person_name(member_id=None, trainer_id=None):
    with engine.connect() as connection:
        if trainer_id:
            query = select(persons.c.surname, persons.c.forename
                           ).select_from(persons
                                         .join(employees, persons.c.id == employees.c.person_id)
                                         .join(trainers, employees.c.id == trainers.c.employee_id)
                                         ).where(trainers.c.id == trainer_id)

        elif member_id:
            query = select(persons.c.surname, persons.c.forename
                           ).select_from(persons
                                         .join(members, persons.c.id == members.c.person_id)
                                         ).where(members.c.id == member_id)

        result = connection.execute(query).fetchone()
        return result


def get_class_and_weekday(class_id):
    with engine.connect() as connection:
        query = select(classtypes.c.name, weekdays.c.name
                       ).select_from(classes
                                     .join(classofferings, classes.c.classoffering_id == classofferings.c.id)
                                     .join(classtypes, classofferings.c.classtype_id == classtypes.c.id)
                                     .join(weekdays, classes.c.weekday_id == weekdays.c.id)
                                     ).where(classes.c.id == class_id)

        result = connection.execute(query).fetchone()
        return result


# 1. How many persons registered in the year ### ?
def count_registrations_by_year(year):
    with engine.connect() as connection:
        query = select(func.count()
                       ).where(func.strftime('%Y', persons.c.enterdate) == str(year))

        result = connection.execute(query).fetchone()
        return result[0] if result else 0


# fetch and print registrations of the year 2021
year = 2021
registrations_2021 = count_registrations_by_year(year)

print(f"{registrations_2021} persons registered in the year {year}.")


# 2. Has the member with the ID ### already terminated its membership?
def is_membership_terminated(member_id):
    if not check_member_exists(member_id):
        raise ValueError(f"Member with ID {member_id} not found.")

    with engine.connect() as connection:
        query = select(persons.c.surname, persons.c.forename, persons.c.leavedate
                       ).join(members, persons.c.id == members.c.person_id
                              ).where(members.c.id == member_id)

        result = connection.execute(query).fetchone()
        surname, forename, leavedate = result
        return (leavedate is not None and leavedate < datetime.now().date()), forename, surname


# Check and print if the members with the IDs 10, 15 and 37 have already terminated their membership
member_ids = [10, 15, 37]

for member_id in member_ids:
    try:
        membership_terminated, forename, surname = is_membership_terminated(member_id)
        status = "has terminated his/her membership" if membership_terminated else "is still an active member"
        print(f"{forename} {surname} (ID: {member_id}) {status}.")

    except ValueError as e:
        print(e)


# 3. Which class(es) does the trainer with the ID ### teach on weekday ID ###?
def get_classes_by_trainer(trainer_id, weekday_id):
    if not check_trainer_exists(trainer_id):
        raise ValueError(f"Trainer with ID {trainer_id} not found.")

    if not check_weekday_exists(weekday_id):
        raise ValueError(f"Weekday with ID {weekday_id} doesn't exist!")

    surname, forename = get_person_name(trainer_id=trainer_id)

    with engine.connect() as connection:
        weekday_query = select(weekdays.c.name).where(weekdays.c.id == weekday_id)
        weekday = connection.execute(weekday_query).fetchone()[0]

        main_query = select(classtypes.c.name, classes.c.time
                            ).select_from(classtypes
                                          .join(classofferings, classtypes.c.id == classofferings.c.classtype_id)
                                          .join(classes, classofferings.c.id == classes.c.classoffering_id)
                                          ).where(
            and_(classofferings.c.trainer_id == trainer_id, classes.c.weekday_id == weekday_id))

        result = connection.execute(main_query).fetchall()
        return forename, surname, weekday, result


# fetch and print classes of the trainers with the ID 2 and 3 on weekday ID 2
trainer_ids = [2, 3]
weekday_id = 2

for trainer_id in trainer_ids:
    try:
        forename, surname, weekday, classes_by_trainer = get_classes_by_trainer(trainer_id, weekday_id)
        if not classes_by_trainer:
            print(f"No classes found for trainer {forename} {surname} (ID: {trainer_id}) on {weekday}s.")
        else:
            print(f"Classes for trainer {forename} {surname} (ID: {trainer_id}) on {weekday}s:")
            for class_ in classes_by_trainer:
                classtype, time = class_
                print(f" - {classtype} at {time.strftime('%H:%M')}")
    except ValueError as e:
        print(e)


# 4. Is the trainer with the ID ### instructor of class ID ###?
def is_trainer_instructor(trainer_id, class_id):
    if not check_trainer_exists(trainer_id):
        raise ValueError(f"Trainer with ID {trainer_id} not found.")

    if not check_class_exists(class_id):
        raise ValueError(f"Class with ID {class_id} not found.")

    surname, forename = get_person_name(trainer_id=trainer_id)
    class_, weekday = get_class_and_weekday(class_id)

    with engine.connect() as connection:
        query = select(classes.c.id
                       ).select_from(classes
                                     .join(classofferings, classes.c.classoffering_id == classofferings.c.id)
                                     ).where(and_(classofferings.c.trainer_id == trainer_id, classes.c.id == class_id))

        result = connection.execute(query).fetchone()
        return forename, surname, class_, weekday, bool(result)


# Check and print if the trainer with the ID 2 is instructor of classes with the IDs 1 and 6
class_ids = [1, 6]

for class_id in class_ids:
    try:
        forename, surname, class_, weekday, instructor = is_trainer_instructor(trainer_ids[0], class_id)
        status = "is the instructor" if instructor else "is not the instructor"
        print(f"Trainer {forename} {surname} (ID: {trainer_ids[0]}) {status} of {class_} on {weekday}s.")
    except ValueError as e:
        print(e)


# 5. How many members are registered for class ID ###?
def get_registrations_by_class(class_id):
    if not check_class_exists(class_id):
        raise ValueError(f"Class with ID {class_id} not found.")

    class_, weekday = get_class_and_weekday(class_id)

    with engine.connect() as connection:
        query = select(func.count()
                       ).select_from(registrations
                                     .join(members, members.c.id == registrations.c.member_id)
                              ).where(registrations.c.class_id == class_id)

        result = connection.execute(query).fetchone()

        return class_, weekday, result[0] if result else 0


# Check and print number of members registered for classes with the IDs 1 and 6
for class_id in class_ids:
    try:
        class_, weekday, registration_count = get_registrations_by_class(class_id)
        print(f"{registration_count} persons are registered for {class_} on {weekday}s.")
    except ValueError as e:
        print(e)


# 6. Is the member with the ID ### registered for class ID ###?
def is_member_registered(member_id, class_id):
    if not check_member_exists(member_id):
        raise ValueError(f"Member with ID {member_id} not found.")

    if not check_class_exists(class_id):
        raise ValueError(f"Class with ID {class_id} not found.")

    surname, forename = get_person_name(member_id=member_id)
    class_, weekday = get_class_and_weekday(class_id)

    with engine.connect() as connection:
        query = select(registrations.c.id
                       ).select_from(registrations
                                     .join(members, members.c.id == registrations.c.member_id)
                                     .join(classes, registrations.c.class_id == classes.c.id)
                                     ).where(and_(members.c.id == member_id, registrations.c.class_id == class_id))

        result = connection.execute(query).fetchone()
        return forename, surname, class_, weekday, bool(result)


# Check and print if the members with the IDs 10, 15 and 37 are registered for class ID 6
for member_id in member_ids:
    try:
        forename, surname, class_, weekday, member_registered = is_member_registered(member_id, class_ids[0])
        status = "is registered" if member_registered else "is not registered"
        print(f"Member {forename} {surname} (ID: {member_id}) {status} for {class_} on {weekday}s.")
    except ValueError as e:
        print(e)


# 7. How many free spots are available for class ID ###?
def count_free_spots_by_class(class_id):
    if not check_class_exists(class_id):
        raise ValueError(f"Class with ID {class_id} not found.")

    class_, weekday = get_class_and_weekday(class_id)

    with engine.connect() as connection:
        query_occupied_spots = select(func.count()
                                      ).select_from(registrations
                                                    ).where(registrations.c.class_id == class_id)

        occupied_spots = connection.execute(query_occupied_spots).fetchone()[0]

        query_max_spots = select(classtypes.c.maxparticipants
                                 ).select_from(classes
                                               .join(classofferings, classes.c.classoffering_id == classofferings.c.id)
                                               .join(classtypes, classofferings.c.classtype_id == classtypes.c.id)
                                               ).where(classes.c.id == class_id)

        max_spots = connection.execute(query_max_spots).fetchone()[0]

        free_spots = max(max_spots - occupied_spots, 0)

        return class_, weekday, free_spots


# Check and print the number of free spots for the classes with the IDs 1 and 6
for class_id in class_ids:
    try:
        class_, weekday, free_spots = count_free_spots_by_class(class_id)
        print(f"{free_spots} free spots are available for {class_} on {weekday}s.")
    except ValueError as e:
        print(e)
