from sqlalchemy import create_engine, text
from datetime import datetime
import create_functions as crfunc

# create database engine
engine = create_engine('sqlite:///data/mygym.db')


# create procedures
# Register the member with the ID ### as new participant of class ID ###
def add_registration(member_id, class_id):
    try:
        # check existence of member_id
        if not crfunc.check_member_exists(member_id):
            raise ValueError(f"Member with ID {member_id} not found.")

        # check existence of class_id
        if not crfunc.check_class_exists(class_id):
            raise ValueError(f"Class with ID {class_id} not found.")

        # check if member is still active
        membership_terminated, forename, surname = crfunc.is_membership_terminated(member_id)
        if membership_terminated:
            return f"{forename} {surname} (ID: {member_id}) has already terminated his/her membership!"

        # check if member is not already registered for this class
        forename, surname, class_, weekday, member_registered = crfunc.is_member_registered(member_id, class_id)
        if member_registered:
            return f"{forename} {surname} (ID: {member_id}) is already registered for {class_} on {weekday}s!"

        # check if member is not the instructor of this class
        forename, surname, class_, weekday, member_instructor = crfunc.is_member_instructor(member_id, class_id)
        if member_instructor:
            return f"{forename} {surname} (ID: {member_id}) is the instructor of {class_} on {weekday}s!"

        # check if there are free spots available for this class
        class_, weekday, free_spots = crfunc.count_free_spots_by_class(class_id)
        if free_spots == 0:
            return f"There are no more free spots in {class_} on {weekday}s!"

        with engine.connect() as connection:
            connection.execute(
                text("""
                INSERT INTO registrations (class_id, member_id, startdate)
                VALUES (:class_id, :member_id, :startdate)
                """),
                {'class_id': class_id, 'member_id': member_id, 'startdate': datetime.now()}
            )
        return ("New participant has registered!")

    except ValueError as e:
        return str(e)
