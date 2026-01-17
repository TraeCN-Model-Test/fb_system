from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# 用户模型
class UserBase(BaseModel):
    username: str = Field(..., example="testuser")
    email: str = Field(..., example="test@example.com")
    name: str = Field(..., example="Test User")

class UserCreate(UserBase):
    password: str = Field(..., example="password123")

class UserUpdate(BaseModel):
    email: Optional[str] = Field(None, example="newemail@example.com")
    name: Optional[str] = Field(None, example="New Name")
    password: Optional[str] = Field(None, example="newpassword123")

class User(UserBase):
    id: int = Field(..., example=1)
    created_at: datetime = Field(..., example="2023-01-01T00:00:00")
    updated_at: datetime = Field(..., example="2023-01-01T00:00:00")

    class Config:
        from_attributes = True

# 反馈模型
class FeedbackBase(BaseModel):
    title: str = Field(..., example="反馈标题")
    content: str = Field(..., example="反馈内容")
    user_id: int = Field(..., example=1)

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackUpdate(BaseModel):
    title: Optional[str] = Field(None, example="新反馈标题")
    content: Optional[str] = Field(None, example="新反馈内容")
    status: Optional[str] = Field(None, example="resolved")

class FeedbackStatusUpdate(BaseModel):
    status: str = Field(..., example="resolved")

class Feedback(FeedbackBase):
    id: int = Field(..., example=1)
    status: str = Field(..., example="pending")
    created_at: datetime = Field(..., example="2023-01-01T00:00:00")
    updated_at: datetime = Field(..., example="2023-01-01T00:00:00")
    tags: List[str] = Field(default_factory=list, example=["bug", "feature"])

    class Config:
        from_attributes = True

# 评论模型
class CommentBase(BaseModel):
    content: str = Field(..., example="评论内容")
    user_id: int = Field(..., example=1)
    feedback_id: int = Field(..., example=1)

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    content: str = Field(..., example="新评论内容")

class Comment(CommentBase):
    id: int = Field(..., example=1)
    created_at: datetime = Field(..., example="2023-01-01T00:00:00")
    updated_at: datetime = Field(..., example="2023-01-01T00:00:00")

    class Config:
        from_attributes = True

# 标签模型
class TagBase(BaseModel):
    name: str = Field(..., example="bug")
    description: Optional[str] = Field(None, example="Bug 报告")

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    description: Optional[str] = Field(None, example="新标签描述")

class Tag(TagBase):
    id: int = Field(..., example=1)
    created_at: datetime = Field(..., example="2023-01-01T00:00:00")
    usage_count: int = Field(default=0, example=5)

    class Config:
        from_attributes = True

# 通知模型
class NotificationBase(BaseModel):
    user_id: int = Field(..., example=1)
    title: str = Field(..., example="通知标题")
    content: str = Field(..., example="通知内容")

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    id: int = Field(..., example=1)
    is_read: bool = Field(default=False, example=False)
    created_at: datetime = Field(..., example="2023-01-01T00:00:00")

    class Config:
        from_attributes = True

# 统计模型
class UserStats(BaseModel):
    total_users: int = Field(..., example=100)
    active_users: int = Field(..., example=80)

class FeedbackStats(BaseModel):
    total_feedback: int = Field(..., example=200)
    pending: int = Field(..., example=50)
    in_progress: int = Field(..., example=100)
    resolved: int = Field(..., example=30)
    closed: int = Field(..., example=20)

class HotTag(BaseModel):
    name: str = Field(..., example="bug")
    count: int = Field(..., example=50)

class FeedbackTrend(BaseModel):
    date: str = Field(..., example="2023-01-01")
    count: int = Field(..., example=10)

# 响应模型
class MessageResponse(BaseModel):
    message: str = Field(..., example="操作成功")

class UserListResponse(BaseModel):
    users: List[User] = Field(...)
    total: int = Field(..., example=10)

class FeedbackListResponse(BaseModel):
    feedbacks: List[Feedback] = Field(...)
    total: int = Field(..., example=20)

class CommentListResponse(BaseModel):
    comments: List[Comment] = Field(...)
    total: int = Field(..., example=5)

class TagListResponse(BaseModel):
    tags: List[Tag] = Field(...)
    total: int = Field(..., example=15)

class NotificationListResponse(BaseModel):
    notifications: List[Notification] = Field(...)
    total: int = Field(..., example=5)
    unread_count: int = Field(..., example=3)
