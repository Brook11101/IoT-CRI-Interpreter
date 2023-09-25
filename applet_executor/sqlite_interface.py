import sqlite3


class SqliteInterface:
    def __init__(self) -> None:
        # connect sqlite database
        self.conn = sqlite3.connect("../../data/rules.db")
        c = self.conn.cursor()

        c.execute("PRAGMA table_info(rule_table)")
        columns = c.fetchall()
        required_columns = {
            "trigger_device",
            "trigger_condition",
            "query_device",
            "query_content",
            "action_device",
            "action_execution",
            "is_pro",
            "priority",
        }
        actual_columns = {column[1] for column in columns}

        # check whether the database is valid
        if required_columns.issubset(actual_columns):
            print("The database is valid.")
        else:
            print("The database is invalid.")
            self.reconstruct()

    def reconstruct(self):
        # clear all content in the database
        c = self.conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = c.fetchall()
        for table in tables:
            c.execute(f"DROP TABLE IF EXISTS {table[0]}")
        c.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indices = c.fetchall()
        for index in indices:
            c.execute(f"DROP INDEX IF EXISTS {index[0]}")
        self.conn.commit()

        # construct new content
        c.execute(
            """CREATE TABLE rule_table(trigger_device text, trigger_condition text, query_device text, query_content text, action_device text, action_action text, is_pro integer, priority integer)"""
        )
        self.conn.commit()

    def query(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM rule_table")

        rows = c.fetchall()

        for row in rows:
            print(row)

    def add_applet(
        self,
        trigger_device,
        trigger_condition,
        query_device,
        query_content,
        action_device,
        action_action,
        is_pro,
        priority,
    ):
        if is_pro == "true":
            is_pro = 1
        else:
            is_pro = 0
        c = self.conn.cursor()
        c.execute(
            "INSERT INTO rule_table VALUES ('"
            + trigger_device
            + "','"
            + trigger_condition
            + "','"
            + query_device
            + "','"
            + query_content
            + "','"
            + action_device
            + "','"
            + action_action
            + "',"
            + str(is_pro)
            + ","
            + str(priority)
            + ")"
        )

        self.conn.commit()


if __name__ == "__main__":
    sql = SqliteInterface()
    sql.add_applet("a", "b", "c", "d", 1, 1)
    # sql.query()
