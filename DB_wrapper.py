import psycopg2
from contextlib import closing


class DBWrapper:
    def __init__(self, dict_conn):
        self.db_connection = dict_conn

    def get_tables_sizes(self):
        query = """SELECT table_name, pg_size_pretty(pg_table_size(table_name))
                from information_schema.tables where table_schema = 'public'
                and table_catalog = 'db_bot';"""
        query_data = ""
        try:
            with closing(psycopg2.connect(**self.db_connection)) as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                query_data = cursor.fetchall()
        except psycopg2.OperationalError as e:
            pass

        msg = ""
        if query_data:
            for set_data in query_data:
                msg += ': '.join(set_data)
                msg += "\n"
        else:
            msg = "Sorry, now no data. Just try again later"
        return msg
