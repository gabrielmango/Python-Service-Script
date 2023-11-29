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
                ).filter(Atendimento.co_caso == case, Atendimento.st_ativo == True)
            return query_service.all()
        except SQLAlchemyError as e:
            s.rollback()
            raise e


def duplicate_services_created(services, timeout=59):
    """ Check duplicate services by difference in creation date. """
    if len(services) > 1:
        for index in range(len(services) - 1):
            duplicate_services = []
            diff = services[index + 1][2] - services[index][2]

            if diff.total_seconds() > -timeout and diff.total_seconds() < timeout:
                duplicate_services.append(services[index])
                duplicate_services.append(services[index + 1])
        return duplicate_services


def duplicate_services_description(services):
    """ Check duplicate services for repeated description. """
    unique_texts = set()
    services_excluded = []

    if services:
        for service in services:
            description = service[1]

            if description not in unique_texts:
                unique_texts.add(description)
            else:
                services_excluded.append(service)
        return services_excluded


def create_file(services, file_name, schema='public'):
    """ Create file with update services. """
    if services:
        for service in services:
            with open(file_name, 'a+') as file:
                text = f"UPDATE {schema}.tb_atendimento SET st_ativo = FALSE WHERE co_seq_atendimento = {service[0]}; \n" 
                file.write(text)


def main():
    """ Executes all functionalities of this script. """
    cases = query_cases()
    for case in cases:
        services = query_services(case)
        duplicate_services = duplicate_services_created(services)
        services_excluded = duplicate_services_description(duplicate_services)
        create_file(services_excluded, 'services_excluded.sql')


if __name__ == '__main__':
    main()