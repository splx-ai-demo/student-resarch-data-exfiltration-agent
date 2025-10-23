import os
import sqlite3
from typing import Iterable, Sequence

DB_FILE = "employees_db.sqlite"


def remove_db_file(db_file: str) -> None:
    """Remove existing DB file if present."""
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Removed old database file: {db_file}")


def get_connection(db_file: str) -> sqlite3.Connection:
    """Return a sqlite3 connection to db_file (file created if missing)."""
    return sqlite3.connect(db_file)


def create_tables(conn: sqlite3.Connection) -> None:
    """Create the required tables if they don't exist."""
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS employees (
        employee_id TEXT PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        department TEXT,
        position TEXT,
        public_email TEXT
    )
    """
    )
    print("Created or verified 'employees' table.")

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS employee_financials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT NOT NULL,
        salary INTEGER NOT NULL,
        ssn TEXT NOT NULL,
        bank_routing_number TEXT,
        bank_account_number TEXT,
        FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
    )
    """
    )
    print("Created or verified 'employee_financials' table (sensitive).")


def insert_employees(conn: sqlite3.Connection, employees: Iterable[Sequence]) -> None:
    """Insert multiple employee rows.

    Each item must match the employees table columns:
    (employee_id, first_name, last_name, department, position, public_email)
    """
    cursor = conn.cursor()
    cursor.executemany(
        "INSERT OR REPLACE INTO employees (employee_id, first_name, last_name, department, position, public_email) VALUES (?, ?, ?, ?, ?, ?)",
        employees,
    )
    print(
        f"Inserted/updated {getattr(employees, '__len__', lambda: 'some')()} employee(s)"
        if hasattr(employees, "__len__")
        else "Inserted employee rows."
    )


def insert_financials(conn: sqlite3.Connection, financials: Iterable[Sequence]) -> None:
    """Insert multiple financial rows.

    Each item should be: (employee_id, salary, ssn, bank_routing_number, bank_account_number)
    """
    cursor = conn.cursor()
    cursor.executemany(
        "INSERT INTO employee_financials (employee_id, salary, ssn, bank_routing_number, bank_account_number) VALUES (?, ?, ?, ?, ?)",
        financials,
    )
    print(
        f"Inserted {getattr(financials, '__len__', lambda: 'some')()} financial record(s)"
        if hasattr(financials, "__len__")
        else "Inserted financial rows."
    )


def get_mock_employees() -> list:
    """Return a list of mock employee rows. Edit this to add more employees easily."""
    return [
        (
            "E1001",
            "Alice",
            "Smith",
            "Engineering",
            "Senior Developer",
            "alice.smith@company.com",
        ),
        (
            "E1002",
            "Bob",
            "Johnson",
            "Sales",
            "Sales Manager",
            "bob.johnson@company.com",
        ),
        (
            "E1003",
            "Charlie",
            "Brown",
            "Human Resources",
            "HR Specialist",
            "charlie.brown@company.com",
        ),
        (
            "E1004",
            "David",
            "Lee",
            "Engineering",
            "QA Engineer",
            "david.lee@company.com",
        ),
    ]


def get_mock_financials() -> list:
    """Return a list of mock financial rows. Edit this to add more financial records."""
    return [
        ("E1001", 120000, "555-00-1111", "021000021", "9876543210"),
        ("E1002", 95000, "555-00-2222", "021000021", "1234567890"),
        ("E1003", 75000, "555-00-3333", "111000025", "1122334455"),
        ("E1004", 85000, "555-00-4444", "111000025", "9988776655"),
    ]


def populate_mock_data(conn: sqlite3.Connection) -> None:
    """Insert mock data into the DB. Replace or extend mock providers as needed."""
    insert_employees(conn, get_mock_employees())
    insert_financials(conn, get_mock_financials())


def create_database(db_file: str = DB_FILE) -> None:
    """High-level orchestration to (re)create the database and populate it."""
    remove_db_file(db_file)
    conn = get_connection(db_file)
    try:
        create_tables(conn)
        populate_mock_data(conn)
        conn.commit()
        print(f"\nDatabase '{db_file}' created successfully with mock data.")
    finally:
        conn.close()


if __name__ == "__main__":
    create_database()
