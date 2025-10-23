import json
import sqlite3

from agents import function_tool

DB_PATH = "employees_db.sqlite"


@function_tool
def query_employee_db_tool(query: str) -> str:
    """
    Executes a raw SQL query against the employee database.

    Args:
        query: The SQL query to execute.

    Returns:
        A JSON string of the query results.
    """
    print(f"[SQL Tool] Executing query: {query}")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(query)

            rows = cursor.fetchall()

            results = [dict(row) for row in rows]

            if not results:
                return "Query executed successfully, but returned no results."

            return json.dumps(results, indent=2)

    except sqlite3.Error as e:
        print(f"[SQL Tool] Error: {e}")
        return f"An error occurred: {e}"
    except Exception as e:
        print(f"[SQL Tool] General Error: {e}")
        return f"A general error occurred: {e}"
