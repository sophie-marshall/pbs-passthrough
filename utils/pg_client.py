import psycopg2
from pgvector.psycopg2 import register_vector

class PGClient: 
    """
    Adapted from Useff's PGClient in AI-search-applications 
    """

    def __init__(self, host, db_name, user, password):
        self.host = host 
        self.db_name = db_name
        self.user = user
        self.password = password
        self.conn = self._make_connection()
        register_vector(self.conn)

    def _make_connection(self):
        conn = psycopg2.connect(
            host=self.host, user=self.user, password=self.password, dbname=self.db_name
        )
        return conn
    
    def execute_query(self, query):
        """
        Execute a provided query in the database 

        Args:
            query (str): SQL query as a string

        Returns:
            result (list): List of tuples representing query results
        """
        cur = self.conn.cursor()
        try:
            cur.execute(query)
            result = cur.fetchall()
            self.conn.commit()
            return result 
        except Exception as e:
            self.conn.rollback()
            return(str(e))
        finally:
            cur.close()
    
    def insert_embeddings_for_assets(self, table, assets):
        """
        Accepts a list of asset dictionaries and inserts them into an embedding enabled table

        Args:
            table (str): Name of table to query
            assets (list): List of dictionaries with data to insert into table 
        """
        cur = self.conn.cursor()
        try:
            for asset in assets:
                cur.execute (
                    f"""INSERT INTO {table}
                        (actor_actress, character, link, about, face, facial_embedding)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        asset["actor_actress"],
                        asset["character"],
                        asset["link"],
                        asset["about"],
                        asset["face"],
                        asset["facial_embedding"],
                    ),
                )
            self.conn.commit()
        except Exception as e:
            return(str(e))
        finally:
            cur.close()