import os
from sqlalchemy import create_engine

connection_string = os.environ['CONNECTION_STRING']

engine = create_engine(connection_string)
