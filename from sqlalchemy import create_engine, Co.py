from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Connexion à la base de données source
source_engine = create_engine('source_database_connection_string')
source_session = sessionmaker(bind=source_engine)()

# Connexion à la base de données cible
target_engine = create_engine('target_database_connection_string')
target_session = sessionmaker(bind=target_engine)()

Base = declarative_base()

# Définir une classe de modèle pour la table source
class SourceTable(Base):
    __tablename__ = 'source_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # ... d'autres colonnes

# Définir une classe de modèle pour la table cible
class TargetTable(Base):
    __tablename__ = 'target_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # ... d'autres colonnes

# Créer les tables dans la base de données cible
Base.metadata.create_all(target_engine)

# Récupérer les données de la table source
source_data = source_session.query(SourceTable).all()

# Migrer les données vers la table cible
for row in source_data:
    target_row = TargetTable(name=row.name)
    target_session.add(target_row)

# Commit des changements dans la base de données cible
target_session.commit()

# Fermer les sessions
source_session.close()
target_session.close()
