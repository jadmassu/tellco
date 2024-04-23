from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

class DatabaseManager:
    def __init__(self, db_uri):
        try:
            self.engine = create_engine(db_uri)
            self.Session = sessionmaker(bind=self.engine)
            self.meta = MetaData()
            print("Database connection established successfully.")
        except SQLAlchemyError as e:
            print(f"Error connecting to database: {e}")

    def create_session(self):
        try:
            return self.Session()
        except SQLAlchemyError as e:
            print(f"Error creating session: {e}")
            return None

    # def close_session(self, session):
    #     try:
    #         session.close()
    #         print("Session closed successfully.")
    #     except SQLAlchemyError as e:
    #         print(f"Error closing session: {e}")

    def execute_sql_file(self, sql_file):
        try:
            with open(sql_file, 'r') as file:
                sql_script = file.read()
            with self.engine.connect() as connection:
                trans = connection.begin()  # Begin a transaction
                connection.execute(sql_script)
                trans.commit()  # Commit the transaction
            print("SQL script imported successfully")
        except SQLAlchemyError as e:
            print("Error while importing SQL script:", e)
            trans.rollback() 
    def execute_query(self, query):
        try:
            with self.engine.connect() as connection:
                result = connection.execute(query)
                return result.fetchall()
        except SQLAlchemyError as e:
            print(f"Error executing query: {e}")
            return None

    def create_table(self, table_name, columns):
        try:
            table = Table(table_name, self.meta, *columns)
            table.create(self.engine)
            print(f"Table '{table_name}' created successfully.")
        except SQLAlchemyError as e:
            print(f"Error creating table: {e}")

    def drop_table(self, table_name):
        try:
            table = Table(table_name, self.meta, autoload=True)
            table.drop(self.engine)
            print(f"Table '{table_name}' dropped successfully.")
        except SQLAlchemyError as e:
            print(f"Error dropping table: {e}")


    