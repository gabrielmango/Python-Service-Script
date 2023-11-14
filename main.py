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

def query_service(case):
    ''' Queries all services in the case provided. '''
    with session as sess:
        try:
            # Query active cases in the database
            query_service = sess.query(Atendimento.co_seq_atendimento, Atendimento.ds_atendimento).filter(Atendimento.co_caso == case)

            services = [service[0] for service in query_service.all()]

            return query_service.all()
        except SQLAlchemyError as e:
            # Rollback the transaction in case of an error
            sess.rollback()
            raise e 

def create_file(services_list, file_name):
    if services_list:
        for service in services_list:
            with open(file_name, 'a+') as file:
                text = f"UPDATE public.tb_atendimento SET st_ativo = FALSE WHERE co_seq_atendimento = {service[0]}; \n"
                file.write(text)


cases = query_cases()

for case in cases:
    services_of_case = query_service(case)

    if len(services_of_case) > 1:

        unique_texts = set()

        services_excluded = []

        for service in services_of_case:
            text = service[1]

            if text not in unique_texts:
                unique_texts.add(text)
            else:
                services_excluded.append(service)
        
        create_file(services_excluded, 'update_services.sql')