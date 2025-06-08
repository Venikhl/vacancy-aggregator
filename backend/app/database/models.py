from app.database.database import Base
from sqlalchemy import Column, Integer, String, Text, Numeric, TIMESTAMP, ForeignKey, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


vacancy_employment_type = Table(
    'Vacancy_EmploymentType',
    Base.metadata,
    Column('vacancy_id', Integer, ForeignKey('Vacancy.vacancy_id'), primary_key=True),
    Column('employment_type_id', Integer, ForeignKey('EmploymentType.employment_type_id'), primary_key=True)
)

user_favorite_vacancies = Table(
    'User_Favorite_Vacancies',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('User.user_id'), primary_key=True),
    Column('vacancy_id', Integer, ForeignKey('Vacancy.vacancy_id'), primary_key=True)
)

user_favorite_resumes = Table(
    'User_Favorite_Resumes',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('User.user_id'), primary_key=True),
    Column('resume_id', Integer, ForeignKey('Resume.resume_id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'User'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(200))
    hashed_password = Column(String(100))
    
    favorite_vacancies = relationship("Vacancy", secondary=user_favorite_vacancies, backref="users_who_favorited")
    favorite_resumes = relationship("Resume", secondary=user_favorite_resumes, backref="users_who_favorited")

class Vacancy(Base):
    __tablename__ = 'Vacancy'
    
    vacancy_id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String(100), nullable=False)
    source_id = Column(Integer, ForeignKey('Source.source_id'))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    company_id = Column(Integer, ForeignKey('Company.company_id'))
    salary_type_id = Column(Integer, ForeignKey('SalaryType.salary_type_id'))
    salary_currency = Column(String(50))
    salary_value = Column(Numeric(10, 2))
    experience_category_id = Column(Integer, ForeignKey('ExperienceCategory.category_id'))
    location_id = Column(Integer, ForeignKey('Location.location_id'))
    specialization_id = Column(Integer, ForeignKey('Specialization.specialization_id'))
    published_at = Column(TIMESTAMP(timezone=True))
    contacts = Column(Text)
    url = Column(String(255))
    
    employment_types = relationship("EmploymentType", secondary=vacancy_employment_type, backref="vacancies")
    company = relationship("Company", backref="vacancies")
    source = relationship("Source", backref="vacancies")
    salary_type = relationship("SalaryType", backref="vacancies")
    experience_category = relationship("ExperienceCategory", backref="vacancies")
    location = relationship("Location", backref="vacancies")
    specialization = relationship("Specialization", backref="vacancies")

class Location(Base):
    __tablename__ = 'Location'
    
    location_id = Column(Integer, primary_key=True, autoincrement=True)
    region = Column(String(100))

class Specialization(Base):
    __tablename__ = 'Specialization'
    
    specialization_id = Column(Integer, primary_key=True, autoincrement=True)
    specialization = Column(String(255))

class EmploymentType(Base):
    __tablename__ = 'EmploymentType'
    
    employment_type_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

class Company(Base):
    __tablename__ = 'Company'
    
    company_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

class ExperienceCategory(Base):
    __tablename__ = 'ExperienceCategory'
    
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

class Source(Base):
    __tablename__ = 'Source'
    
    source_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

class SalaryType(Base):
    __tablename__ = 'SalaryType'
    
    salary_type_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

class Resume(Base):
    __tablename__ = 'Resume'
    
    resume_id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String(100), nullable=False)
    source_id = Column(Integer, ForeignKey('Source.source_id'))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    salary_type_id = Column(Integer, ForeignKey('SalaryType.salary_type_id'))
    salary_currency = Column(String(50))
    salary_value = Column(Numeric(10, 2))
    skills_text = Column(Text)
    location_id = Column(Integer, ForeignKey('Location.location_id'))
    experience_category_id = Column(Integer, ForeignKey('ExperienceCategory.category_id'))
    education = Column(Text)
    specialization_id = Column(Integer, ForeignKey('Specialization.specialization_id'))
    first_name = Column(String(100))
    last_name = Column(String(100))
    middle_name = Column(String(100))
    email = Column(String(255))
    phone_number = Column(String(50))
    published_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    
    source = relationship("Source", backref="resumes")
    salary_type = relationship("SalaryType", backref="resumes")
    location = relationship("Location", backref="resumes")
    experience_category = relationship("ExperienceCategory", backref="resumes")
    specialization = relationship("Specialization", backref="resumes")