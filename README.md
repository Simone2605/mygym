# Fitness Gym Database Project

This project demonstrates the creation and management of a database for a fictional fitness gym using **Python** and *
*SQLAlchemy**. The primary goal was to design and implement a relational database that simulates gym operations, while
translating SQL queries into Python code via SQLAlchemy in **PyCharm**.

## Project Overview

The database includes several tables representing key entities, such as **Members**, **Employees**, and **Classes**.
SQLAlchemy is used as the Object-Relational Mapping (ORM) tool to facilitate interactions between Python and the
database, making it easy to generate and manage SQL queries programmatically. The data in this project is entirely
fictional and serves demonstration purposes only.

## Entity Relationship Diagram

Below is the entity-relationship diagram (ERD), showing the structure and relationships between the
database tables.
![ER_diagram.png](diagrams%2FER_diagram.png)

## Key Components

- **Functions**: Defined in `create_functions.py`, these perform essential database operations, such as checking if a
  member is registered, retrieving trainer schedules, and counting available spots in classes.
- **Procedures**: Located in `create_procedures.py`, these handle more complex operations, like registering a member for
  a class and ensuring all necessary checks are performed.
- **Views**: The `create_views.py` script creates views that combine data from multiple tables for easier querying. For
  example, a view shows trainers are teaching specific classes and how many participants are registered.
- **Triggers**: The `create_trigger.py`script defines triggers, such as automatically updating the end date of a
  membership when a member's leave date changes.

## Directory Structure

The project is organized in a way to separate scripts, data, and tests for easier navigation and maintainability:

```
mygym/
│
├── data/                      # Contains the SQLite database and sample data
│ ├── example_data/            # CSV files with fictional data for loading into the database
│ ├── mygym.db                 # SQLite database file
│
├── diagrams/                  # ER Diagram showing the structure of the database
│ ├── ER_diagram.png           # The visual representation of the database
│
├── scripts/                   # Python scripts to manage the database
│ ├── python/                  # Python scripts using SQLAlchemy for database operations
│ │ ├── create_db.py           # Script to define and create the database structure
│ │ ├── create_functions.py    # Functions to interact with the database
│ │ ├── create_procedures.py   # Procedures for database operations
│ │ ├── create_trigger.py      # Triggers for automatic updates
│ │ ├── create_views.py        # SQL views for better querying
│
├── tests/                     # Test scripts to verify the database and its functions
│ ├── add_testdata.py          # Script to load fictional test data into the database
│ ├── test_functions.py        # Unit tests for functions interacting with the database
│ ├── test_procedures.py       # Unit tests for stored procedures
│
├── README.md                  # Project documentation (this file)
├── requirements.txt           # List of Python dependencies required for the project
```

## Getting Started

To get started, ensure you have **Python** installed and follow these steps to set up and run the project:

### 1. **Clone the repository**:

```bash
git clone https://github.com/Simone2605/mygym
```

### 2. **Install the required dependencies**:

```bash
pip install -r requirements.txt
```

### 3. **Set up the database**:

Create the database schema using `create_db.py`:

```bash
python scripts/python/create_db.py
```

Populate the database with fictional data using `add_testdata.py`:

```bash
python scripts/python/add_testdata.py
```

### 4. **Test the setup**:

Run the function tests using `test_functions.py`:

```bash
  python tests/test_functions.py
```

Run the procedure tests using `test_procedures.py`:

```bash
python tests/test_procedures.py
```

## Conclusion

This project serves as a practical example of using **Python** and **SQLAlchemy** to manage a database for a fitness
gym. The focus is on understanding how SQL queries can be translated into Python code within **PyCharm**, providing a
flexible, programmatic approach to database management.