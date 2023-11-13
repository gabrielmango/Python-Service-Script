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

# Create a list of unique case numbers by converting the duplicates to a set and back to a list
cases = query_cases()
