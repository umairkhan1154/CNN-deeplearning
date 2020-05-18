import os
import sqlite3


def show_menu():
    print("1. Add an employee to the database")
    print("2. Archive an Employee")
    print("3. List all the Employees")
    print("4. Show all unarchived employees")
    print("5. Show all new employees who started their job on/or after 1/1/2017")
    print("6. Exit")


def get_connection():
    connection = sqlite3.connect("Employee.db")
    cursor = connection.cursor()

    return connection, cursor


def add_employee():
    try:
        first_name = input("\nEnter First Name: ")
        last_name = input("Enter Last Name: ")
        salary = float(input("Enter Salary: "))
        year_started = int(input("Enter Year Started: "))
        date_of_birth = input("Enter Date of Birth (yyyy-mm-dd): ")
        print()

        connection, cursor = get_connection()

        insert_query = f'''INSERT INTO tblEmployee
                        (FirstName, LastName, Salary, YearStarted, DateOfBirth, Archived) VALUES
                        ("{first_name}", "{last_name}", {salary}, {year_started}, "{date_of_birth}", "N");'''

        cursor.execute(insert_query)

        if cursor.rowcount > 0:
            print("\n\tEmployee added successfully!\n")
        else:
            print("\n\tData not saved!\n")

        connection.commit()

        cursor.close()

    except Exception as e:
        print(f"\n\tInvalid Input! {e}\n")

    finally:
        if connection:
            connection.close()


def archive_employee():
    first_name = input("\nEnter First Name: ")
    last_name = input("Enter Last Name: ")

    try:
        connection, cursor = get_connection()

        employee_exists = False

        for f_name, l_name in cursor.execute("SELECT FirstName, LastName FROM tblEmployee"):
            if f_name == first_name and l_name == last_name:
                employee_exists = True
                break

        if employee_exists:
            cursor.execute(
                f"UPDATE tblEmployee SET Archived = 'Y' WHERE FirstName = '{first_name}' AND LastName = '{last_name}';")

            if cursor.rowcount > 0:
                print("\n\tEmployee archived successfully!\n")
        else:
            print(f"\n\tThere is no employee with name, '{first_name} {last_name}'\n")

        connection.commit()

        cursor.close()

    except sqlite3.Error as error:
        print(f"\n\tError occurred! {error}\n")

    finally:
        if connection:
            connection.close()


def show_employees():
    try:
        connection, cursor = get_connection()

        data = cursor.execute(
            "SELECT EmployeeID, FirstName, LastName, Salary, YearStarted, DateOfBirth FROM tblEmployee;")

        print()

        for emp_id, f_name, l_name, salary, year, dob in data:
            formatted_row = f"{emp_id:3} {f_name:10} {l_name:10} ${salary:10,}  {year}  {dob}"
            print(formatted_row)

        print()

        cursor.close()

    except sqlite3.Error as e:
        print(f"\n\tError occurred! {e}\n")

    finally:
        if connection:
            connection.close()


def show_unarchived_employees():
    try:
        connection, cursor = get_connection()

        data = cursor.execute(
            "SELECT EmployeeID, FirstName, LastName, Salary, YearStarted, DateOfBirth FROM tblEmployee WHERE Archived = 'N';")

        print()

        for emp_id, f_name, l_name, salary, year, dob in data:
            formatted_row = f"{emp_id:3} {f_name:10} {l_name:10} ${salary:10,}  {year}  {dob}"
            print(formatted_row)

        print()

        cursor.close()

    except sqlite3.Error as e:
        print(f"\n\tError occurred! {e}\n")

    finally:
        if connection:
            connection.close()


def show_new_employees():
    try:
        connection, cursor = get_connection()

        data = cursor.execute(
            "SELECT EmployeeID, FirstName, LastName, Salary, YearStarted, DateOfBirth FROM tblEmployee WHERE YearStarted >= 2017;")

        print()

        for emp_id, f_name, l_name, salary, year, dob in data:
            formatted_row = f"{emp_id:3} {f_name:10} {l_name:10} ${salary:10,}  {year}  {dob}"
            print(formatted_row)

        print()

        cursor.close()

    except sqlite3.Error as e:
        print(f"\n\tError occurred! {e}\n")

    finally:
        if connection:
            connection.close()


def create_database():
    exists = os.path.exists(rf"{os.getcwd()}\Employee.db")

    if not exists:
        try:
            connection = sqlite3.connect("Employee.db")
            cursor = connection.cursor()
            create_table_query = '''CREATE TABLE tblEmployee
                                        (
                                            EmployeeID INTEGER PRIMARY KEY,
                                            FirstName TEXT,
                                            LastName TEXT,
                                            Salary FLOAT,
                                            YearStarted INTEGER,
                                            DateOfBirth DATE,
                                            Archived TEXT
                                        );'''
            cursor.execute(create_table_query)

            connection.commit()

            cursor.close()

        except sqlite3.Error as error:
            print(f"\n\tError while creating a sqlite table! {error}\n")

        finally:
            if connection:
                connection.close()


def main():
    create_database()

    while True:
        show_menu()

        user_choice = input("Enter choice: ")

        if user_choice == "1":
            add_employee()

        elif user_choice == "2":
            archive_employee()

        elif user_choice == "3":
            show_employees()

        elif user_choice == "4":
            show_unarchived_employees()

        elif user_choice == "5":
            show_new_employees()

        elif user_choice == "6":
            print("\n\tTHANK YOU!\n")
            break

        else:
            print("\n\tInvalid Choice!\n")


main()
