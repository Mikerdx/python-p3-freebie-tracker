from models import Base, Dev, Company, Freebie
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Connect to an in-memory SQLite database (you can change this to your db)
engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Create sample data
company = Company(name='Cool Company', founding_year=2000)
dev = Dev(name='Alice')
session.add(company)
session.add(dev)
session.commit()

# Create a freebie
freebie = Freebie(item_name='Sticker', value=10, dev=dev, company=company)
session.add(freebie)
session.commit()

# Print to verify relationships
print(freebie.dev.name)         # Should print 'Alice'
print(freebie.company.name)     # Should print 'Cool Company'
print(dev.freebies)             # Should show the freebie(s) collected by dev

