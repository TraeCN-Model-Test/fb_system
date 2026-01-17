from fastapi import FastAPI
from contextlib import asynccontextmanager
from tortoise import Tortoise

from app.core.config import settings
from app.api.api_v1 import router as api_v1_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理：初始化和关闭数据库连接"""
    # 初始化Tortoise ORM
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["app.models.tortoise_models"]}
    )
    # 创建数据库表
    await Tortoise.generate_schemas()
    
    yield
    
    # 关闭数据库连接
    await Tortoise.close_connections()

# 创建FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A hasty developed feedback system API",
    version="1.0.0",
    lifespan=lifespan
)



# 根路径
@app.get("/")
async def root():
    return {"message": "Welcome to Hasty Feedback System"}

# 注册API路由
app.include_router(api_v1_router, prefix=settings.API_V1_STR)

print("Application initialized successfully!")
print(f"Database URL: {settings.DATABASE_URL}")
print(f"API prefix: {settings.API_V1_STR}")
print("Visit http://localhost:8000/docs to see API documentation")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)