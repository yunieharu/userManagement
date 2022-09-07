from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.auth import AuthHandler
from app.schemas import AuthDetails, AccountForget, TokenCheck, AccountReset
from app import models, crud, schemas

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/", response_model=List[schemas.User])
def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db=db)


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.put("/users/{id}/", response_model=schemas.User)
def update_user(user: schemas.UserUpdate, id: int = id, db: Session = Depends(get_db)):
    return crud.update_user(db=db, user=user, id=id)


@app.delete("/users/{id}/")
def delete_user(id: int = id, db: Session = Depends(get_db)):
    crud.delete_user(db=db, id=id)
    return {}


auth_handler = AuthHandler()
users = []


@app.post('/register', status_code=201)
def register(auth_details: AuthDetails, db: Session = Depends(get_db)):
    account = crud.get_accounts(db=db)
    for x in account:
        if (x.username == auth_details.username):
            raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    acc = {
        'username': auth_details.username,
        'email': auth_details.email,
        'password': hashed_password
    }
    new_user = {
        'username': auth_details.username,
        'name': '',
        'age': 0,
        'gender': '',
    }
    account_schema = schemas.AccountCreate(**acc)
    new_user = schemas.UserCreate(**new_user)
    crud.create_account(db=db, account=account_schema)
    crud.create_user(db=db, user=new_user)
    return


@app.post('/login')
def login(auth_details: AuthDetails, db: Session = Depends(get_db)):
    user = None
    account = crud.get_accounts(db=db)
    for x in account:
        if x.username == auth_details.username:
            user = x
            break

    if (user is None) or (not auth_handler.verify_password(auth_details.password, user.password)):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user.username)
    return { 'token': token }


@app.post('/forget-password')
def forget(auth_details: AccountForget, db: Session = Depends(get_db)):
    user = None
    account = crud.get_accounts(db=db)
    for x in account:
        if x.email == auth_details.email:
            user = x
            break

    if (user is None):
        raise HTTPException(status_code=401, detail='Invalid email')
    token = auth_handler.encode_token(user.email)
    return { 'token': token }


@app.put('/reset-password')
def reset(reset_password: AccountReset, db: Session = Depends(get_db)):
    email = auth_handler.decode_token(reset_password.token)
    print(email)
    user = None
    account = crud.get_accounts(db=db)
    if reset_password.new_password != reset_password.confirm_password:
        raise HTTPException(status_code=401, detail='Your password and confirmation password do not match')
    for x in account:
        if x.email == email:
            user = x
            break
    if (user is None):
        raise HTTPException(status_code=401, detail='Invalid token')
    print(auth_handler.get_password_hash(reset_password.new_password))
    crud.update_account(db=db, email= email, password=auth_handler.get_password_hash(reset_password.new_password))
    return { 'message': "Reset password successfully" }

@app.get("/accounts/")
def list_accounts(db: Session = Depends(get_db)):
    return crud.get_accounts(db=db)

@app.get('/unprotected')
def unprotected():
    return { 'hello': 'world' }


@app.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    return crud.get_user_by_id(db=db, username= username)


