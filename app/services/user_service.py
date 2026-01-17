from typing import Optional, List, Dict, Any
from passlib.context import CryptContext
from app.models.tortoise_models import User
from app.models.pydantic_models import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    @staticmethod
    async def create_user(user_data: UserCreate) -> User:
        password_hash = pwd_context.hash(user_data.password)
        user = await User.create(
            username=user_data.username,
            email=user_data.email,
            name=user_data.name,
            password_hash=password_hash
        )
        return user
    
    @staticmethod
    async def get_user(user_id: int) -> Optional[User]:
        return await User.get_or_none(id=user_id)
    
    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        return await User.get_or_none(username=username)
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        return await User.get_or_none(email=email)
    
    @staticmethod
    async def get_users(skip: int = 0, limit: int = 100) -> List[User]:
        return await User.all().offset(skip).limit(limit)
    
    @staticmethod
    async def get_users_count() -> int:
        return await User.all().count()
    
    @staticmethod
    async def update_user(user_id: int, update_data: UserUpdate) -> Optional[User]:
        user = await User.get_or_none(id=user_id)
        if not user:
            return None
        
        update_dict = update_data.model_dump(exclude_unset=True)
        if "password" in update_dict:
            update_dict["password_hash"] = pwd_context.hash(update_dict.pop("password"))
        
        for field, value in update_dict.items():
            setattr(user, field, value)
        
        await user.save()
        return user
    
    @staticmethod
    async def delete_user(user_id: int) -> bool:
        user = await User.get_or_none(id=user_id)
        if not user:
            return False
        
        await user.delete()
        return True
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    async def authenticate_user(username: str, password: str) -> Optional[User]:
        user = await UserService.get_user_by_username(username)
        if not user:
            return None
        if not UserService.verify_password(password, user.password_hash):
            return None
        return user