import os
import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv()

# Getting database url
URL = os.environ['URL']

# Create a database engine using the specified URL
engine = create_engine(URL)

# Create a session factory using the engine
Session = sessionmaker(bind=engine)

# Open a session using the session factory
session = Session()