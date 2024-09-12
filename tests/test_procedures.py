from scripts.python import create_procedures as crprod

class_id = 1
member_ids = [2, 10, 11, 25, 37]

# Register the members with the IDs 2, 10, 11, 24 and 37 as new participants of the class with the 1
for member_id in member_ids:
    feedback = crprod.add_registration(member_id, class_id)
    print(feedback)
