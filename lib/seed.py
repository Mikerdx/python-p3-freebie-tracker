#!/usr/bin/env python3

# Script goes here!
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Company, Dev, Freebie

engine = create_engine('sqlite:///freebies.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Create sample data
c1 = Company(name="Google", founding_year=1998)
c2 = Company(name="Microsoft", founding_year=1975)

d1 = Dev(name="Alice")
d2 = Dev(name="Bob")

f1 = Freebie(item_name="Sticker", value=1, dev=d1, company=c1)
f2 = Freebie(item_name="T-Shirt", value=10, dev=d2, company=c2)

session.add_all([c1, c2, d1, d2, f1, f2])
session.commit()
