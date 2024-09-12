from scripts.python import create_functions as crfunc

year = 2021
member_ids = [2, 10, 11, 25, 37]
trainer_ids = [2, 3]
weekday_id = 2
class_ids = [1, 6]

# 1. How many persons registered in the year 2021 ?
registrations_2021 = crfunc.count_registrations_by_year(year)
print(f"{registrations_2021} persons registered in the year {year}.")

# 2. Have the members with the IDs 2, 10, 11, 25 and 37 terminated their membership?
for member_id in member_ids:
    try:
        membership_terminated, forename, surname = crfunc.is_membership_terminated(member_id)
        status = "has terminated his/her membership" if membership_terminated else "is still an active member"
        print(f"{forename} {surname} (ID: {member_id}) {status}.")

    except ValueError as e:
        print(e)

# 3. Which class(es) do the trainers with the IDs 2 and 3 teach on Tuesdays?
for trainer_id in trainer_ids:
    try:
        forename, surname, weekday, classes_by_trainer = crfunc.get_classes_by_trainer(trainer_id, weekday_id)
        if not classes_by_trainer:
            print(f"No classes found for trainer {forename} {surname} (ID: {trainer_id}) on {weekday}s.")
        else:
            print(f"Classes of trainer {forename} {surname} (ID: {trainer_id}) on {weekday}s:")
            for class_ in classes_by_trainer:
                classtype, time = class_
                print(f" - {classtype} at {time.strftime('%H:%M')}")
    except ValueError as e:
        print(e)

# 4. Is the member with the ID 2 instructor of the classes with the IDs 1 and 6?
for class_id in class_ids:
    try:
        forename, surname, class_, weekday, member_instructor = crfunc.is_member_instructor(member_ids[0], class_id)
        status = "is the instructor" if member_instructor else "is not the instructor"
        print(f"{forename} {surname} (ID: {member_ids[0]}) {status} of {class_} on {weekday}s.")
    except ValueError as e:
        print(e)

# 5. How many members are registered for the classes with the IDs 1 and 6?
for class_id in class_ids:
    try:
        class_, weekday, registration_count = crfunc.get_registrations_by_class(class_id)
        print(f"{registration_count} persons are registered for {class_} on {weekday}s.")
    except ValueError as e:
        print(e)

# 6. Are the members with the IDs 2, 10, 11, 25 and 37 registered for the class with the ID 6?
for member_id in member_ids:
    try:
        forename, surname, class_, weekday, member_registered = crfunc.is_member_registered(member_id, class_ids[0])
        status = "is registered" if member_registered else "is not registered"
        print(f"{forename} {surname} (ID: {member_id}) {status} for {class_} on {weekday}s.")
    except ValueError as e:
        print(e)

# 7. How many free spots are available for the classes with IDs 1 and 6?
for class_id in class_ids:
    try:
        class_, weekday, free_spots = crfunc.count_free_spots_by_class(class_id)
        print(f"{free_spots} free spots are available for {class_} on {weekday}s.")
    except ValueError as e:
        print(e)
