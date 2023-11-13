from database.conn import session
from database.database import Atendimento
from sqlalchemy.exc import SQLAlchemyError

from pprint import pprint

def convert_dictionary(data):
    ''' Converts an data object into a dictionary, mapping attributes to column names based on the 'Atendimento' table structure.'''
    if data:
        return {
            column.name: getattr(data, column.name)
            for column in Atendimento.__table__.columns
        }


def query_cases():
    ''' Queries all active cases in the database.'''
    with session as sess:
        try:
            # Query active cases in the database
            query_cases = sess.query(Atendimento.co_caso).filter(Atendimento.st_ativo == True)

            cases = [case[0] for case in query_cases.all()]

            return list(set(cases))
        except SQLAlchemyError as e:
            # Rollback the transaction in case of an error
            sess.rollback()
            raise e

# Create a list of unique case numbers by converting the duplicates to a set and back to a list
cases = query_cases()

pprint(len(cases))
input()

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
    
