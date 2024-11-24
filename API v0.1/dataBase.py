
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Text, LargeBinary, create_engine, Float
from sqlalchemy.orm import relationship, DeclarativeBase
import psycopg2


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=True)
    phone = Column(String(12), nullable=False)
    dateBirthday = Column(Date, nullable=False)
    password = Column(String(50), nullable=False)
    login = Column(String(50), nullable=False)
    addressResidential = Column(String(100), nullable=False)
    bancAccountNumber = Column(Integer, nullable=False)
    roleId = Column(Integer, ForeignKey('Role.id'), nullable=False)

    roles = relationship("Role", back_populates="users")
    userCars = relationship("UserCar", back_populates="user")
    repairs = relationship("Repair", back_populates="user")
    reports = relationship("Report", back_populates="user")


class Role(Base):
    __tablename__ = 'Role'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    roleName = Column(String(50), nullable=False)

    users = relationship("User", back_populates="role")


class CarPark(Base):
    __tablename__ = 'CarPark'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    stateNumber = Column(String(8), nullable=False)
    model = Column(String(50), nullable=False)
    stamp = Column(String(50), nullable=False)

    userCars = relationship("UserCar", back_populates="carPark")


class UserCar(Base):
    __tablename__ = 'UserCar'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    carId = Column(Integer, ForeignKey('CarPark.id'), nullable=False)
    userId = Column(Integer, ForeignKey('User.id'), nullable=False)

    carParks = relationship("carPark", back_populates="userCars")
    users = relationship("User", back_populates="userCars")


class Repair(Base):
    __tablename__ = 'Repair'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    descriptionBreakdown = Column(String, nullable=False)
    dateAndTimeRepair = Column(Date, nullable=False)
    addressPointRepair = Column(String(100), nullable=False)

    userId = Column(Integer, ForeignKey('User.id'), nullable=False)

    users = relationship("User", back_populates="repairs")


class Report(Base):
    __tablename__ = 'Report'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    pointDeparture = Column(String(50), nullable=False)
    typePointDeparture = Column(String(50), nullable=False)
    sender = Column(String(100), nullable=False)
    pointDestination = Column(String(50), nullable=False)
    typePointDestination = Column(String(50), nullable=False)
    recipient = Column(String(100), nullable=False)
    viewWood = Column(String(50), nullable=False)
    lengthWood = Column(Integer, nullable=False)
    volumeWood = Column(Float, nullable=False)
    reportDateTime = Column(Date, nullable=False)
    assortmentWoodTypeId = Column(Integer, ForeignKey('AssortmentWoodType.id'), nullable=False)
    varietyWoodTypeId = Column(Integer, ForeignKey('VarietyWoodType.id'), nullable=False)
    userId = Column(Integer, ForeignKey('User.id'), nullable=False)

    assortmentWoodTypes = relationship("AssortmentWoodType", back_populates="reports")
    varietyWoodTypes = relationship("VarietyWoodType", back_populates="reports")
    users = relationship("User", back_populates="reports")


engine = create_engine("postgresql://postgres:8696@localhost:5432/baseUchet", echo=True)

Base.metadata.create_all(engine)
