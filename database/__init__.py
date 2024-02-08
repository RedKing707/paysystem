from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Путь к бд
SQLALCHEMY_DATABASE_URI = 'sqlite:///pay.db'
# Двигатель
engine = create_engine(SQLALCHEMY_DATABASE_URI)
# Соединения
SessionLocal = sessionmaker(bind=engine)
# Класс для наследования в таблицах
Base = declarative_base()


# функция-генератор соединений в базе
def get_db():
    db = SessionLocal()
    # Пробуем сгенерировать подключение к базе
    try:
        yield db

    except Exception:
        db.rollback()
        raise

    # Для любых событий закрываем соединение
    finally:
        db.close()
