from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Tenta pegar a URL do sistema (Railway/Supabase). Se não tiver, usa a local (MySQL)
# Substitua a URL abaixo pela sua local se precisar rodar offline
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:1234@localhost/audit_contabil_poc")

# Correção para o padrão do SQLAlchemy se a URL vier como "postgres://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Cria a conexão
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()