from sqlalchemy import create_engine, text

# create database engine
engine = create_engine('sqlite:///mygym.db')

# create trigger via sql query
# Update enddate for class registrations based on leavedate changes
trigger_update_leaving = """
CREATE TRIGGER tr_update_leaving
AFTER UPDATE OF leavedate ON persons
FOR EACH ROW
BEGIN
    UPDATE registrations
    SET enddate = NEW.leavedate
    WHERE (enddate IS NULL OR enddate > NEW.leavedate)
    AND member_id = (SELECT id FROM members WHERE person_id = NEW.id);
END;
"""

# execute SQL query to create trigger
with engine.connect() as connection:
    connection.execute(text(trigger_update_leaving))