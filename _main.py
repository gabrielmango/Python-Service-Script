from database.conn import session
from database.database import Atendimento
from sqlalchemy.exc import SQLAlchemyError


def query_cases():
    ''' Queries all active cases in the database. '''
    with session as s:
        try:
            query_cases = s.query(Atendimento.co_caso).distinct().filter(Atendimento.st_ativo == True).all()
            return [case[0] for case in query_cases]
        except SQLAlchemyError as e:
            s.rollback()
            raise e


def query_services(case):
    ''' Queries all services in the provided case. '''
    with session as s:
        try:
            query_service = s.query(
                Atendimento.co_seq_atendimento, 
                Atendimento.ds_atendimento, 
                Atendimento.dh_criacao
                ).filter(Atendimento.co_caso == case)
            return query_service.all()
        except SQLAlchemyError as e:
            s.rollback()
            raise e


def main():
    """ Executes all functionalities of this script. """
    cases = query_cases()
    for case in cases:
        services = query_services(case)
        print(f'The case {case} has {len(services)} services.')


if __name__ == '__main__':
    main()