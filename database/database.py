from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, Numeric, Text, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Atendimento(Base):
    __tablename__ = 'tb_atendimento'
    __table_args__ = {'schema': 'public'}
    
    co_seq_atendimento = Column(Integer, primary_key=True)
    co_caso = Column(Integer, nullable=False)
    co_uuid_3 = Column(String(255))
    fl_atendimento_restrito = Column(Boolean, nullable=False, default=False)
    ds_atendimento = Column(Text)
    dh_inicio_atendimento = Column(DateTime)
    dh_fim_atendimento = Column(DateTime)
    st_ativo = Column(Boolean, nullable=False)
    dh_criacao = Column(DateTime)
    dh_alteracao = Column(DateTime)
    tp_operacao = Column(String(50), nullable=False)
    nu_versao = Column(Numeric(10), nullable=False)
    co_uuid = Column(String(255), nullable=False)
    co_uuid_1 = Column(String(255))
    co_uuid_4 = Column(String(255))
    no_protocolo = Column(String(100))
    co_uuid_5 = Column(String(255))
    sg_projeto_modificador = Column(String(15))
    sg_acao_modificadora = Column(String(15))
    no_end_point_modificador = Column(String(255))
    fl_atendimento_por_cooperacao = Column(Boolean)
    tp_atividade_atendimento = Column(String(30))
    co_uuid_6 = Column(String(255))