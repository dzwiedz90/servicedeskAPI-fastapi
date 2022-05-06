import uvicorn
import sqlalchemy

from fastapi import FastAPI, HTTPException, Request, status

from data.postgres_api import PostgresAPI
from data.exceptions import UserNotFoundException
from data import validators

app = FastAPI()
postgres_api = PostgresAPI()


# ADMIN API

# @app.get('/admins')
# async def get_admins():
#     return postgres_api.get_admins()
#
#
# @app.get('/admins/{admin_id}')
# async def get_admin(admin_id: int):
#     try:
#         return postgres_api.get_admin(admin_id)
#     except UserNotFoundException:
#         raise HTTPException(status_code=404, detail='Admin with given id not found in database')
#
#
# @app.post('/admins', status_code=status.HTTP_201_CREATED)
# async def create_admin(r: Request):
#     data = await r.json()
#     try:
#         postgres_api.create_admin(username=data['username'], password=data['password'], email=data['email'])
#         return {'message': 'Admin created'}
#     except sqlalchemy.exc.IntegrityError:
#         raise HTTPException(status_code=400, detail='Username or email in use')
#
#
# @app.put('/admins/{admin_id}')
# async def update_admin_password(admin_id: int, r: Request):
#     data = await r.json()
#     try:
#         postgres_api.update_admin_password(admin_id, data['password'])
#         return {'message': 'Password changed'}
#     except UserNotFoundException:
#         raise HTTPException(status_code=404, detail='Admin with given id not found in database')
#
#
# @app.delete('/admins/{admin_id}')
# async def delete_admin(admin_id: int):
#     try:
#         postgres_api.delete_admin(admin_id)
#         return {'message': 'Admin account deleted'}
#     except UserNotFoundException:
#         raise HTTPException(status_code=404, detail='Admin with given id not found in database')


# USERS API

@app.get('/users')
async def get_users():
    return postgres_api.get_users()


@app.get('/users/users')
async def get_only_users():
    return postgres_api.get_only_users()


@app.get('/users/admins')
async def get_only_admins():
    return postgres_api.get_only_admins()


@app.get('/users/archived')
async def get_only_admins():
    return postgres_api.get_archived_users()


@app.get('/users/{user_id}')
async def get_user(user_id: int):
    try:
        return postgres_api.get_user(user_id)
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail='User with given id not found in database')


@app.post('/users', status_code=status.HTTP_201_CREATED)
async def create_user(r: Request):
    data = await r.json()
    try:
        postgres_api.create_user(username=data['username'], password=data['password'], email=data['email'],
                                 is_admin=data['is_admin'])
        return {'message': 'User created'}
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail='Username or email in use')


@app.put('/users/{user_id}')
async def update_user(user_id: int, r: Request):
    data = await r.json()
    try:
        postgres_api.update_user(user_id, data['password'], data['email'], data['is_admin'])
        return {'message': 'User updated'}
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail='User with given id not found in database')


@app.delete('/users/{user_id}')
async def delete_user(user_id: int):
    try:
        postgres_api.delete_user(user_id)
        return {'message': 'User account deleted'}
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail='User with given id not found in database')


@app.patch('/users/{user_id}')
async def restore_user(user_id: int):
    try:
        postgres_api.restore_user(user_id)
        return {'message': 'User account restored'}
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail='User with given id not found in database')


# CASES API

@app.get('/cases')
async def get_cases():
    return postgres_api.get_cases()
    # return postgres_api.get_users()


@app.get('/cases/{case_id}')
async def get_case(user_id: int):
    pass
    # try:
    #     return postgres_api.get_user(user_id)
    # except UserNotFoundException:
    #     raise HTTPException(status_code=404, detail='User with given id not found in database')


@app.post('/cases', status_code=status.HTTP_201_CREATED)
async def create_case(r: Request):
    data = await r.json()
    if validators.validate_case(data):
        postgres_api.create_case(content=data['content'], severity=data['severity'], user_id=data['user_id'])
        return {'message': 'Case created'}
    else:
        raise HTTPException(status_code=400, detail='Data not valid')


@app.put('/cases/{case_id}')
async def update_case(user_id: int, r: Request):
    pass
    # data = await r.json()
    # try:
    #     postgres_api.update_user_email(user_id, data['email'])
    #     return {'message': 'Email changed'}
    # except UserNotFoundException:
    #     raise HTTPException(status_code=404, detail='User with given id not found in database')


@app.delete('/cases/{case_id}')
async def delete_case(user_id: int):
    pass
    # try:
    #     postgres_api.delete_user(user_id)
    #     return {'message': 'User account deleted'}
    # except UserNotFoundException:
    #     raise HTTPException(status_code=404, detail='User with given id not found in database')


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
