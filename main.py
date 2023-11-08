import os
import nltk
from nltk.metrics import jaccard_distance
from unicodedata import normalize
from database import Atendimento
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from pprint import pprint


nltk.download('punkt')
os.system('cls')

# Criar sessão com o banco
engine = create_engine('postgresql+psycopg2://postgres:dpmg2022@10.100.64.55:5432/bohr_estagiarios_2')
Session = sessionmaker(bind=engine)
session = Session()

print('Conexão com o banco estabelecida.')


def comparar_textos(textos):
    texto_1 = set(nltk.word_tokenize(textos[0].lower()))
    texto_2 = set(nltk.word_tokenize(textos[1].lower()))

    similaridade = 1 - jaccard_distance(texto_1, texto_2)

    return similaridade * 100

def converte_dicionario(dado):
    if dado:
        return {
            coluna.name: getattr(dado, coluna.name)
            for coluna in Atendimento.__table__.columns
        }


# Consulta dados da tabela tb_atendimento
with session as sessao:
    try:
        consulta_completa = sessao.query(Atendimento).filter(Atendimento.st_ativo == True).order_by(Atendimento.co_caso).order_by(Atendimento.dh_criacao)
        atendimento_duplicados = [converte_dicionario(dado) for dado in consulta_completa.all()]

        consulta_casos = sessao.query(Atendimento.co_caso)
        casos_duplicados = [dado[0] for dado in consulta_casos.all()]
    except SQLAlchemyError as e:
        session.rollback()
        raise e 

casos = list(set(casos_duplicados))

print('Consulta dos dados duplicados retornada.')

for caso in casos:
    atendimentos_do_caso = []
    for atendimento in atendimento_duplicados:
        if atendimento['co_caso'] == caso:
            atendimentos_do_caso.append(atendimento)

    if len(atendimentos_do_caso) > 1:

        textos_unicos = set()
        atendimentos_excluidos = []

        for atendimento in atendimentos_do_caso:
            texto = atendimento['ds_atendimento']
            if texto not in textos_unicos:
                textos_unicos.add(texto)
            else:
                atendimentos_excluidos.append(atendimento)
        if atendimentos_excluidos:
            for dado in atendimentos_excluidos:
                with open('atualizacao_atendimento.txt', 'a+') as arquivo:
                    texto = f"UPDATE public.tb_atendimento SET st_ativo = FALSE WHERE co_seq_atendimento = {dado['co_seq_atendimento']}; \n"
                    arquivo.write(texto)


print('Processo finalizado. Arquivo com os Updates gerado com sucesso!')
    
