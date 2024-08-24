from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

BaseDeDatos = declarative_base()


class Estudiante(BaseDeDatos):

    __tablename__ = "estudiantesJuanGranada"

    id = Column(Integer, primary_key=True, index=True)
    nombre =  Column(String(50))
    apellido = Column(String(50))
    edad = Column(Integer)
    mail =  Column(String(50))
    matricula =  Column(String(50))
    carrera = Column(String(50))