from sqlalchemy import create_engine, Table, MetaData, select, func, and_
from datetime import datetime

# create database engine
engine = create_engine('sqlite:///data/mygym.db')

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


# create (table-valued / scalar-valued) functions
# 1. How many persons registered in the year ### ?
def count_registrations_by_year(year):
    with engine.connect() as connection:
        query = select(func.count()
                       ).where(func.strftime('%Y', persons.c.enterdate) == str(year))

        result = connection.execute(query).fetchone()
        return result[0] if result else 0


# 2. Has the member with the ID ### terminated its membership?
def is_membership_terminated(member_id):
    # check existence of member_id
    if not check_member_exists(member_id):
        raise ValueError(f"Member with ID {member_id} not found.")

    with engine.connect() as connection:
        query = select(persons.c.surname, persons.c.forename, persons.c.leavedate
                       ).join(members, persons.c.id == members.c.person_id
                              ).where(members.c.id == member_id)

        result = connection.execute(query).fetchone()
        surname, forename, leavedate = result
        return (leavedate is not None and leavedate < datetime.now().date()), forename, surname


# 3. Which class(es) does the trainer with the ID ### teach on weekday ID ###?
def get_classes_by_trainer(trainer_id, weekday_id):
    # check existence of trainer_id
    if not check_trainer_exists(trainer_id):
        raise ValueError(f"Trainer with ID {trainer_id} not found.")

    # check existence of weekday_id
    if not check_weekday_exists(weekday_id):
        raise ValueError(f"Weekday with ID {weekday_id} doesn't exist!")

    # get surname and forename of the trainer
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


# 4. Is the member with the ID ### instructor of class ID ###?
def is_member_instructor(member_id, class_id):
    # check existence of member_id
    if not check_member_exists(member_id):
        raise ValueError(f"Member with ID {member_id} not found.")

    # check existence of class_id
    if not check_class_exists(class_id):
        raise ValueError(f"Class with ID {class_id} not found.")

    # get surname and forename of the member
    surname, forename = get_person_name(member_id=member_id)

    # get the names of class and weekday
    class_, weekday = get_class_and_weekday(class_id)

    with engine.connect() as connection:
        query = select(classes.c.id
                       ).select_from(classofferings
                                     .join(trainers, classofferings.c.trainer_id == trainers.c.id)
                                     .join(employees, trainers.c.employee_id == employees.c.id)
                                     .join(members, employees.c.person_id == members.c.person_id)
                                     .join(classes, classofferings.c.id == classes.c.classoffering_id)
                                     ).where(and_(members.c.id == member_id, classes.c.id == class_id))

        result = connection.execute(query).fetchone()
        return forename, surname, class_, weekday, bool(result)


# 5. How many members are registered for class ID ###?
def get_registrations_by_class(class_id):
    # check existence of class_id
    if not check_class_exists(class_id):
        raise ValueError(f"Class with ID {class_id} not found.")

    # get the names of class and weekday
    class_, weekday = get_class_and_weekday(class_id)

    with engine.connect() as connection:
        query = select(func.count()
                       ).select_from(registrations
                                     .join(members, members.c.id == registrations.c.member_id)
                                     ).where(registrations.c.class_id == class_id)

        result = connection.execute(query).fetchone()

        return class_, weekday, result[0] if result else 0


# 6. Is the member with the ID ### registered for class ID ###?
def is_member_registered(member_id, class_id):
    # check existence of member_id
    if not check_member_exists(member_id):
        raise ValueError(f"Member with ID {member_id} not found.")

    # check existence of class_id
    if not check_class_exists(class_id):
        raise ValueError(f"Class with ID {class_id} not found.")

    # get surname and forename of the member
    surname, forename = get_person_name(member_id=member_id)

    # get the names of class and weekday
    class_, weekday = get_class_and_weekday(class_id)

    with engine.connect() as connection:
        query = select(registrations.c.id
                       ).select_from(registrations
                                     ).where(
            and_(registrations.c.member_id == member_id, registrations.c.class_id == class_id))

        result = connection.execute(query).fetchone()
        return forename, surname, class_, weekday, bool(result)


# 7. How many free spots are available for class ID ###?
def count_free_spots_by_class(class_id):
    # check existence of class_id
    if not check_class_exists(class_id):
        raise ValueError(f"Class with ID {class_id} not found.")

    # get the names of class and weekday
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
