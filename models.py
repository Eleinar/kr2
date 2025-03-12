from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, CheckConstraint, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(40))
    last_name = Column(String(40))
    position = Column(String(20))
    salary = Column(Float)
    hire_date = Column(Date)
    
    tasks = relationship("Task", back_populates="assignee")
    departments = relationship("Department", back_populates="manager")

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    dep_name = Column(String(20))
    manager_id = Column(Integer, ForeignKey('employees.id'))
    
    manager = relationship("Employee", back_populates="departments")

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    project_name = Column(String(50))
    start_date = Column(Date)
    end_date = Column(Date)
    budget = Column(Float)
    
    tasks = relationship("Task", back_populates="project")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    task_name = Column(String(40))
    description = Column(String(255))
    status = Column(String(20), CheckConstraint("status IN ('В процессе', 'Завершена', 'Отменена')"))
    project_id = Column(Integer, ForeignKey('projects.id'))
    assignee_id = Column(Integer, ForeignKey('employees.id'))
    
    project = relationship("Project", back_populates="tasks")
    assignee = relationship("Employee", back_populates="tasks")

class EmployeeProject(Base):
    __tablename__ = 'employee_projects'
    employee_id = Column(Integer, ForeignKey('employees.id'), primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), primary_key=True)
    employee_role = Column(String(20), CheckConstraint("employee_role IN ('Руководитель', 'Разработчик', 'Тестировщик')"))
    
def create_connection():
    engine = create_engine("postgresql://admin:root@localhost:5432/kr2", echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session(bind=engine)
    return session
