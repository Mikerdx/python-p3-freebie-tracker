from sqlalchemy import Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    founding_year = Column(Integer)

    freebies = relationship('Freebie', back_populates='company')

    def give_freebie_to_dev(self, session: Session, dev, item_name: str, value: int):
        new_freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        session.add(new_freebie)
        session.commit()
        return new_freebie

    def freebies_given(self, session: Session):
        return session.query(func.count(Freebie.id)).filter(Freebie.company_id == self.id).scalar()

    def total_value_given(self, session: Session):
        return session.query(func.coalesce(func.sum(Freebie.value), 0)).filter(Freebie.company_id == self.id).scalar()

    @classmethod
    def oldest_company(cls, session: Session):
        return session.query(cls).order_by(cls.founding_year.asc()).first()


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    freebies = relationship('Freebie', back_populates='dev')

    def freebies_received(self, session: Session):
        return session.query(func.count(Freebie.id)).filter(Freebie.dev_id == self.id).scalar()

    def total_value_received(self, session: Session):
        return session.query(func.coalesce(func.sum(Freebie.value), 0)).filter(Freebie.dev_id == self.id).scalar()

    def freebies_from_company(self, session: Session, company):
        return session.query(Freebie).filter(Freebie.dev_id == self.id, Freebie.company_id == company.id).all()

    def received_one(self, session: Session, item_name: str):
        return session.query(Freebie).filter(
            Freebie.dev_id == self.id,
            Freebie.item_name == item_name
        ).first() is not None

    def has_freebie(self, freebie):
        return freebie.dev_id == self.id

    def give_away(self, session: Session, freebie, other_dev):
        if self.has_freebie(freebie):
            freebie.dev = other_dev
            session.commit()
            return freebie
        return None


class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    value = Column(Integer)

    dev_id = Column(Integer, ForeignKey('devs.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

    dev = relationship('Dev', back_populates='freebies')
    company = relationship('Company', back_populates='freebies')

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"
