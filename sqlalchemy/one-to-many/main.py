from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import Company, Employee

url = 'postgresql://postgres:mysecretpassword@localhost/postgres'

engine = create_engine(url, echo=True)
Session = sessionmaker(bind=engine)

if True:
    with Session.begin() as session:
        company = Company()
        company.employees = [
            Employee(name='Magnus'),
            Employee(name='John')
        ]
        session.add(company)

if False:
    with Session.begin() as session:
        company = session.query(Company).get(1)
        company.employees = []

if True:
    with Session.begin() as session:
        session.add(Employee(name='Lisa', company_id=1))

if True:
    with Session.begin() as session:
        company = session.query(Company).get(1)

        session.add(Employee(name='Lisa\'s brother', company_id=1))
        for e in company.employees:
            print(e)
        # session.add(company)
        # print(company.employees)
        # company.employees = [
        #     Employee(name='Magnus'),
        #     Employee(name='John')
        # ]
        # session.add(company)
