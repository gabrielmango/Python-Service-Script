import os
import dotenv
from database import Atendimento
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

dotenv.load_dotenv()

# Getting database url
URL = os.environ['URL']

# Create a database engine using the specified URL
engine = create_engine(URL)

# Create a session factory using the engine
Session = sessionmaker(bind=engine)

# Open a session using the session factory
session = Session()

print('Connection with the database established.')


def convert_dictionary(data):
    ''' Converts an 'dado' object into a dictionary, mapping attributes to column names based on the 'Atendimento' table structure.'''
    if data:
        return {
            column.name: getattr(data, column.name)
            for column in Atendimento.__table__.columns
        }


# Query data from the tb_atendimento table
with session as sessao:
    try:
        # Query active services and order them by case and creation date
        services_query = sessao.query(Atendimento).filter(Atendimento.st_ativo == True).order_by(Atendimento.co_caso).order_by(Atendimento.dh_criacao)
        
        # Convert the result to a list of dictionaries using the `convert_dictionary` function
        services_duplicates = [convert_dictionary(data) for data in services_query.all()]

        # Query cases and store the case numbers in a list
        case_query = sessao.query(Atendimento.co_caso)
        cases_duplicates = [data[0] for data in case_query.all()]

    except SQLAlchemyError as e:
        # Rollback the transaction in case of an error
        session.rollback() 

        raise e 

# Create a list of unique case numbers by converting the duplicates to a set and back to a list
cases = list(set(cases_duplicates))

print('Duplicate data query returned.')

for case in cases:
    # Create an empty list to store services related to a case
    services_of_case = []  

    # Add services related to the case to the list
    for service in services_duplicates:
        if service['co_caso'] == case:
            services_of_case.append(service)

    # Check if there are duplicate services
    if len(services_of_case) > 1: 

        # Create a set to store unique service texts
        unique_texts = set() 

        # Create a list to store duplicate services to be excluded
        services_excluded = []  

        for service in services_of_case:
            text = service['ds_atendimento']
            if text not in unique_texts:
                # Add the service's text to the set of unique texts
                unique_texts.add(text)  
            else:
                # Add duplicate services to the list
                services_excluded.append(service)  

        # Check if there are duplicate services to be excluded
        if services_excluded:  
            for dado in services_excluded:
                with open('update_services.txt', 'a+') as arquivo:
                    text = f"UPDATE public.tb_atendimento SET st_ativo = FALSE WHERE co_seq_atendimento = {dado['co_seq_atendimento']}; \n"
                    
                    # Write SQL statements to mark services as inactive
                    arquivo.write(text)  


print('Process finished. File with Updates generated successfully!')
    
