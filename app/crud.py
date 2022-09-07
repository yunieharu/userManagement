from sqlalchemy.orm import Session

from app import models
from app import schemas


def get_users(db: Session):
    return db.query(models.User).all()


def get_accounts(db: Session):
    return db.query(models.Account).all()


def get_user_by_id(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).all()


def create_account(db:Session, account: schemas.AccountCreate):
    db_account = models.Account(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def update_account(db: Session, email: str, password: str):
    db_account = db.query(models.Account).filter(models.Account.email == email).one()
    db_account.password = password
    db.commit()
    db.refresh(db_account)
    return db_account


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: schemas.UserUpdate, id: int):
    db_user = db.query(models.User).get(id)

    db_user.name = user.name
    db_user.age = user.age
    db_user.gender = user.gender

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, id: int):
    db_user = db.query(models.User).get(id)
    db.delete(db_user)
    db.commit()
