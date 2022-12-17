from fastapi import APIRouter, HTTPException, status
from models.users import User, UserSignIn

user_routers = APIRouter(
    tags=["User"]
)

users = {}


@user_routers.post("/signup")
async def sign_new_user(data: User) -> dict:
    if data.email in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied username exist"
        )
    users[data.email] = data
    return {
        "message": "User successfully registered"
    }


@user_routers.post("/signin")
async def sign_in_user(user: UserSignIn) -> dict:
    if user.email not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    if users[user.email].password != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong credential passed"
        )
    return {
        "message": "User signed in successfully"
    }


@user_routers.get("/users")
async def get_users() -> dict:
    return users