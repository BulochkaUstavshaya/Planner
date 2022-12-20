from fastapi import APIRouter, HTTPException, status
from models.users import User, UserSignIn
from database.connection import Database


user_routers = APIRouter(
    tags=["User"]
)

user_database = Database(User)


@user_routers.post("/signup")
async def sign_new_user(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied username exist"
        )
    await user_database.save(user)
    return {
        "message": "User successfully registered"
    }


@user_routers.post("/signin")
async def sign_in_user(user: UserSignIn) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    if user_exist.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong credential passed"
        )

    return {
        "message": "User signed in successfully"
    }


# @user_routers.get("/users")
# async def get_users() -> dict:
#     return users