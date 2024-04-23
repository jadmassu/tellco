from sqlalchemy import MetaData, Table
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from sqlalchemy import text


from utils.database_manager import DatabaseManager

class DataManager:
    def __init__(self, db_uri):
        self.session_manager = DatabaseManager(db_uri)
        self.engine = self.session_manager.engine
        self.meta = self.session_manager.meta
    
  
    def create_table_from_dataframe(self, df, table_name):
        session = self.session_manager.create_session()
        if session:
            try:
                df.to_sql(table_name, self.engine, index=False, if_exists='replace')
                print(f"Dataframe successfully written to the '{table_name}' table.")
            except SQLAlchemyError as e:
                print("Error while writing dataframe to table:", e)
            finally:
                self.session_manager.close_session(session)
    def read_table_to_dataframe(self, table_name):
        """
        Reads a PostgreSQL table into a pandas dataframe.
        """
        session = self.session_manager.create_session()
        if session:
            try:
                query = text(f"SELECT * FROM {table_name};")
               
                result = session.execute(query)
                df = pd.DataFrame(result.fetchall(), columns=result.keys())
                return df
            except SQLAlchemyError as e:
                print("Error while writing dataframe to table:", e)
        else:
            print("Error, no connection detected!")
            return None

    def append_dataframe_to_table(self, df, table_name):
        session = self.session_manager.create_session()
        if session:
            try:
                df.to_sql(table_name, self.engine, index=False, if_exists='append')
                print(f"Dataframe successfully appended to the '{table_name}' table.")
            except SQLAlchemyError as e:
                print("Error while appending dataframe to table:", e)
            finally:
                self.session_manager.close_session(session)

    def delete_table(self, table_name):
        session = self.session_manager.create_session()
        if session:
            try:
                table = Table(table_name, self.meta, autoload=True)
                table.drop(self.engine)
                print(f"Table '{table_name}' successfully deleted.")
            except SQLAlchemyError as e:
                print("Error while deleting table:", e)
            finally:
                self.session_manager.close_session(session)

