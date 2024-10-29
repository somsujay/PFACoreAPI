from fastapi import APIRouter

#from app.db.database import get_db_pool

router = APIRouter()


# @router.post("/users/")
# async def create_user(user: User):
#     # Validate the user using the service rule
#     if not UserRules.validate_user_age(user):
#         raise HTTPException(status_code=400, detail="User must be 18 years or older")
#
#     query = "INSERT INTO users (name, age, city) VALUES (%s, %s, %s)"
#
#     pool = await get_db_pool()
#     async with pool.acquire() as conn:
#         async with conn.cursor() as cursor:
#             await cursor.execute(query, (user.name, user.age, user.city))
#             await conn.commit()
#
#     # Use the service rule to generate a profile
#     user_profile = UserRules.generate_user_profile(user)
#
#     return {"message": "User created successfully", "profile": user_profile}
