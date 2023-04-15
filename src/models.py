import os
import sys
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(50), nullable=False)
    correo_electronico = Column(String(100), nullable=False, unique=True)
    contrasena = Column(String(100), nullable=False)
    fecha_creacion = Column(DateTime, server_default='CURRENT_TIMESTAMP')

    perfiles = relationship('Perfil', back_populates='usuario')
    publicaciones = relationship('Publicacion', back_populates='usuario')
    comentarios = relationship('Comentario', back_populates='usuario')
    seguidores = relationship('Seguidor', back_populates='usuario')

class Perfil(Base):
    __tablename__ = 'perfiles'

    id_perfil = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), nullable=False)
    nombre_completo = Column(String(100), nullable=False)
    nombre_usuario = Column(String(50), nullable=False, unique=True)
    biografia = Column(String(500))
    avatar = Column(String(200))

    usuario = relationship('Usuario', back_populates='perfiles')

class Publicacion(Base):
    __tablename__ = 'publicaciones'

    id_publicacion = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), nullable=False)
    imagen = Column(String(200))
    descripcion = Column(String(500))
    fecha_publicacion = Column(DateTime, server_default='CURRENT_TIMESTAMP')

    usuario = relationship('Usuario', back_populates='publicaciones')
    comentarios = relationship('Comentario', back_populates='publicacion')

class Comentario(Base):
    __tablename__ = 'comentarios'

    id_comentario = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), nullable=False)
    id_publicacion = Column(Integer, ForeignKey('publicaciones.id_publicacion', ondelete='CASCADE'), nullable=False)
    texto = Column(String(500), nullable=False)
    fecha_comentario = Column(DateTime, server_default='CURRENT_TIMESTAMP')

    usuario = relationship('Usuario', back_populates='comentarios')
    publicacion = relationship('Publicacion', back_populates='comentarios')

class Seguidor(Base):
    __tablename__ = 'seguidores'

    id_seguidor = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), nullable=False)
    id_usuario_seguido = Column(Integer, ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), nullable=False)
    fecha_seguimiento = Column(DateTime, server_default='CURRENT_TIMESTAMP')

    usuario = relationship('Usuario', back_populates='seguidores')
    usuario_seguido = relationship('Usuario', foreign_keys=[id_usuario_seguido], back_populates='seguidores')


## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
