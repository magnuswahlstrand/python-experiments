from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)


class IdempotencyKey(Base):
    __tablename__ = 'idempotency_keys'
    id = Column(UUID(as_uuid=True), primary_key=True)


class HelloContextManager:
    def __enter__(self):
        print("Entering the context...")
        return "Hello, World!"

    def __exit__(self, exc_type, exc_value, exc_tb):
        print("Leaving the context...")
        print(exc_type, exc_value, exc_tb, sep="\n")
        if isinstance(exc_value, Exception):
            # Handle IndexError here...
            print(f"An exception occurred in your with block: {exc_type}")
            print(f"Exception message: {exc_value}")
            return True


with HelloContextManager() as hello:
    print(hello)
    # raise ValueError("hej")
    raise Exception("other")
