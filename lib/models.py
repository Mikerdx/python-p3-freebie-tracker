from sqlalchemy import Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    founding_year = Column(Integer)

    freebies = relationship('Freebie', back_populates='company')

    def give_freebie(self, session: Session, dev, item_name: str, value: int):
        """Create a new Freebie given to a dev."""
        new_freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        session.add(new_freebie)
        session.commit()
        return new_freebie

    def freebies_given(self, session: Session):
        """Return total number of freebies this company has given."""
        return session.query(func.count(Freebie.id)).filter(Freebie.company_id == self.id).scalar()

    def total_value_given(self, session: Session):
        """Return total value of all freebies given by this company."""
        return session.query(func.coalesce(func.sum(Freebie.value), 0)).filter(Freebie.company_id == self.id).scalar()


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    freebies = relationship('Freebie', back_populates='dev')

    def freebies_received(self, session: Session):
        """Return total number of freebies received by this dev."""
        return session.query(func.count(Freebie.id)).filter(Freebie.dev_id == self.id).scalar()

    def total_value_received(self, session: Session):
        """Return total value of all freebies received by this dev."""
        return session.query(func.coalesce(func.sum(Freebie.value), 0)).filter(Freebie.dev_id == self.id).scalar()

    def freebies_by_company(self, session: Session, company):
        """Return list of freebies received from a specific company."""
        return session.query(Freebie).filter(Freebie.dev_id == self.id, Freebie.company_id == company.id).all()


class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    value = Column(Integer)

    dev_id = Column(Integer, ForeignKey('devs.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

    dev = relationship('Dev', back_populates='freebies')
    company = relationship('Company', back_populates='freebies')
