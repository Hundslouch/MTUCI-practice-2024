from database.db import Base
from sqlalchemy import Column, Integer, String


class JobVacancy(Base):
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True)
    hh_id = Column(Integer)
    name = Column(String)
    city = Column(String)
    experience = Column(String)
    employment = Column(String)
    requirement = Column(String)
    responsibility = Column(String)
    salary = Column(String)
    link = Column(String)

    def __repr__(self):
        return f"<JobVacancy(name={self.name}, city={self.city}, experience={self.experience}, employment={self.employment}, requirement={self.requirement}, responsibility={self.responsibility}, salary={self.salary}, link={self.link})>"

    def to_dict(self):
        return {
            "hh_id": self.hh_id,
            "name": self.name,
            "city": self.city,
            "experience": self.experience,
            "employment": self.employment,
            "requirement": self.requirement,
            "responsibility": self.responsibility,
            "salary": self.salary,
            "link": self.link,
        }
