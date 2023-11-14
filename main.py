from database.conn import session
from database.database import Atendimento
from sqlalchemy.exc import SQLAlchemyError


def query_cases():
    '''
    Queries all active cases in the database.

    Returns:
        list: List of unique active cases.
    '''
    with session as sess:
        try:
            query_cases = sess.query(Atendimento.co_caso).filter(Atendimento.st_ativo == True)
            cases = [case[0] for case in query_cases.all()]
            return list(set(cases))
        except SQLAlchemyError as e:
            sess.rollback()
            raise e

def query_service(case):
    '''
    Queries all services in the provided case.

    Args:
        case (int): Case identifier.

    Returns:
        list: List of services in the specified case.
    '''
    with session as sess:
        try:
            query_service = sess.query(Atendimento.co_seq_atendimento, Atendimento.ds_atendimento).filter(Atendimento.co_caso == case)
            services = [service[0] for service in query_service.all()]
            return query_service.all()
        except SQLAlchemyError as e:
            sess.rollback()
            raise e 

def create_file(services_list, file_name):
    '''
    Creates an SQL file with UPDATE statements to deactivate services.

    Args:
        services_list (list): List of services to be deactivated.
        file_name (str): Name of the SQL file to be created.
    '''
    if services_list:
        for service in services_list:
            with open(file_name, 'a+') as file:
                text = f"UPDATE public.tb_atendimento SET st_ativo = FALSE WHERE co_seq_atendimento = {service[0]}; \n"
                file.write(text)

def create_list_excluded(services_list):
    '''
    Creates a list of excluded services based on duplicate texts.

    Args:
        services_list (list): List of services to check for duplicates.

    Returns:
        list: List of excluded services.
    '''
    unique_texts = set()
    services_excluded = []

    if services_list:
        for service in services_list:
            text = service[1]

            if text not in unique_texts:
                unique_texts.add(text)
            else:
                services_excluded.append(service)
        return services_excluded


def duplicate_services(services_of_case):
    if len(services_of_case) > 1:
        services_excluded = create_list_excluded(services_of_case)
        create_file(services_excluded, 'update_services.sql')

def main():
    '''
    Main function to perform the workflow:

    1. Query all active cases.
    2. For each case, query its services.
    3. Identify and create a list of excluded services with duplicate texts.
    4. Create an SQL file with UPDATE statements to deactivate excluded services.
    '''
    cases = query_cases()

    for case in cases:
        services_of_case = query_service(case)
        duplicate_services(services_of_case)

if __name__ == '__main__':
    main()
