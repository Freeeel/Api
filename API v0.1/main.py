import os
import shutil
from msilib.schema import File

import aiofiles
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session, sessionmaker
from dataBase import *
from datetime import datetime
import pydantic
from pydantic import BaseModel
from typing import Dict, List, Optional

app = FastAPI()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class NameCreate(BaseModel):
    name: str

class UserLogin(BaseModel):
    login: str
    password: str

class RepairCreate(BaseModel):
    description_breakdown: str
    date_and_time_repair: str  # Формат: YYYY-MM-DD
    address_point_repair: str
    user_id: int

class ReportCreate(BaseModel):
    point_departure: str
    type_point_departure: str
    sender: str
    point_destination: str
    type_point_destination: str
    recipient: str
    view_wood: str
    length_wood: int
    volume_wood: float
    report_date_time: str
    assortment_wood_type_id: int
    variety_wood_type_id: int
    user_id: int



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.post("/login")
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    # Check user login against the database
    db_user = db.query(User).filter(User.login == user_login.login, User.password == user_login.password).first()

    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid login or password")

    # Return user information except password
    return {
        "id": db_user.id,
        "name": db_user.name,
        "surname": db_user.surname,
        "patronymic": db_user.patronymic,
        "phone": db_user.phone,
        "date_of_birthday": db_user.date_of_birthday,
        "address_residential": db_user.address_residential,
        "bank_account_number": db_user.bank_account_number,
        "role_id": db_user.role_id,
    }


@app.post("/repairs/")
async def create_repair(repair: RepairCreate, db: Session = Depends(get_db)):

    new_repair = Repair(

        description_breakdown=repair.description_breakdown,
        date_and_time_repair=repair.date_and_time_repair,
        address_point_repair=repair.address_point_repair,
        user_id=repair.user_id)
    try:
        db.add(new_repair)
        db.commit()
        db.refresh(new_repair)

    except Exception as e:
        raise HTTPException(status_code=400, detail="Internal server error")
    return new_repair


@app.post("/reports/")
async def create_report(report: ReportCreate, db: Session = Depends(get_db)):

    new_report = Report(
        point_departure=report.point_departure,
        type_point_departure=report.type_point_departure,
        sender=report.sender,
        point_destination=report.point_destination,
        type_point_destination=report.type_point_destination,
        recipient=report.recipient,
        view_wood=report.view_wood,
        length_wood=report.length_wood,
        volume_wood=report.volume_wood,
        report_date_time=report.report_date_time,
        assortment_wood_type_id=report.assortment_wood_type_id,
        variety_wood_type_id=report.variety_wood_type_id,
        user_id=report.user_id
    )

    try:
        db.add(new_report)
        db.commit()
        db.refresh(new_report)

    except Exception as e:
        raise HTTPException(status_code=400, detail="Internal server error")
    return new_report

