from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.models.pydantic_models import (
    User, UserCreate, UserUpdate, UserListResponse,
    Feedback, FeedbackCreate, FeedbackUpdate, FeedbackStatusUpdate, FeedbackListResponse,
    Comment, CommentCreate, CommentUpdate, CommentListResponse,
    Tag, TagCreate, TagListResponse,
    Notification, NotificationCreate, NotificationListResponse,
    UserStats, FeedbackStats, HotTag, FeedbackTrend,
    MessageResponse
)
from app.services import (
    UserService, FeedbackService, CommentService,
    TagService, NotificationService, StatsService
)

router = APIRouter()

# ------------------------
# 用户管理路由
# ------------------------

@router.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    existing_user = await UserService.get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    existing_email = await UserService.get_user_by_email(user.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="邮箱已存在")
    
    db_user = await UserService.create_user(user)
    return db_user

@router.post("/users/login/")
async def login(username: str, password: str):
    user = await UserService.authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    return {"message": "登录成功", "user_id": user.id}

@router.get("/users/{user_id}/", response_model=User)
async def get_user(user_id: int):
    user = await UserService.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@router.get("/users/", response_model=UserListResponse)
async def get_users(skip: int = 0, limit: int = 100):
    users = await UserService.get_users(skip=skip, limit=limit)
    total = await UserService.get_users_count()
    return {"users": users, "total": total}

@router.put("/users/{user_id}/", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate):
    user = await UserService.update_user(user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@router.delete("/users/{user_id}/", response_model=MessageResponse)
async def delete_user(user_id: int):
    success = await UserService.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"message": "用户删除成功"}

# ------------------------
# 反馈管理路由
# ------------------------

@router.post("/feedback/", response_model=Feedback)
async def create_feedback(feedback: FeedbackCreate):
    user = await UserService.get_user(feedback.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    db_feedback = await FeedbackService.create_feedback(feedback)
    return db_feedback

@router.get("/feedback/", response_model=FeedbackListResponse)
async def get_feedback_list(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = Query(None, description="反馈状态过滤")
):
    feedbacks = await FeedbackService.get_feedback_list(skip=skip, limit=limit, status=status)
    total = await FeedbackService.get_feedback_count(status=status)
    return {"feedbacks": feedbacks, "total": total}

@router.get("/feedback/{feedback_id}/", response_model=Feedback)
async def get_feedback(feedback_id: int):
    feedback = await FeedbackService.get_feedback(feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="反馈不存在")
    return feedback

@router.put("/feedback/{feedback_id}/", response_model=Feedback)
async def update_feedback(feedback_id: int, feedback_update: FeedbackUpdate):
    feedback = await FeedbackService.update_feedback(feedback_id, feedback_update)
    if not feedback:
        raise HTTPException(status_code=404, detail="反馈不存在")
    return feedback

@router.delete("/feedback/{feedback_id}/", response_model=MessageResponse)
async def delete_feedback(feedback_id: int):
    success = await FeedbackService.delete_feedback(feedback_id)
    if not success:
        raise HTTPException(status_code=404, detail="反馈不存在")
    return {"message": "反馈删除成功"}

@router.patch("/feedback/{feedback_id}/status/", response_model=Feedback)
async def update_feedback_status(feedback_id: int, status_update: FeedbackStatusUpdate):
    feedback = await FeedbackService.update_feedback_status(feedback_id, status_update.status)
    if not feedback:
        raise HTTPException(status_code=404, detail="反馈不存在")
    return feedback

@router.get("/feedback/search/", response_model=FeedbackListResponse)
async def search_feedback(
    keyword: str = Query(..., description="搜索关键词"),
    skip: int = 0,
    limit: int = 100
):
    feedbacks = await FeedbackService.search_feedback(keyword=keyword, skip=skip, limit=limit)
    return {"feedbacks": feedbacks, "total": len(feedbacks)}

# ------------------------
# 评论管理路由
# ------------------------

@router.post("/comments/", response_model=Comment)
async def create_comment(comment: CommentCreate):
    user = await UserService.get_user(comment.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    feedback = await FeedbackService.get_feedback(comment.feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="反馈不存在")
    
    db_comment = await CommentService.create_comment(comment)
    if not db_comment:
        raise HTTPException(status_code=400, detail="创建评论失败")
    return db_comment

@router.get("/feedback/{feedback_id}/comments/", response_model=CommentListResponse)
async def get_comments(feedback_id: int, skip: int = 0, limit: int = 100):
    feedback = await FeedbackService.get_feedback(feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="反馈不存在")
    
    comments = await CommentService.get_comments(feedback_id=feedback_id, skip=skip, limit=limit)
    total = await CommentService.get_comments_count(feedback_id=feedback_id)
    return {"comments": comments, "total": total}

@router.put("/comments/{comment_id}/", response_model=Comment)
async def update_comment(comment_id: int, comment_update: CommentUpdate):
    comment = await CommentService.update_comment(comment_id, comment_update.content)
    if not comment:
        raise HTTPException(status_code=404, detail="评论不存在")
    return comment

@router.delete("/comments/{comment_id}/", response_model=MessageResponse)
async def delete_comment(comment_id: int):
    success = await CommentService.delete_comment(comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="评论不存在")
    return {"message": "评论删除成功"}

# ------------------------
# 标签管理路由
# ------------------------

@router.post("/tags/", response_model=Tag)
async def create_tag(tag: TagCreate):
    db_tag = await TagService.create_tag(tag)
    return db_tag

@router.get("/tags/", response_model=TagListResponse)
async def get_tags(skip: int = 0, limit: int = 100):
    tags = await TagService.get_tags(skip=skip, limit=limit)
    total = await TagService.get_tags_count()
    return {"tags": tags, "total": total}

@router.post("/feedback/{feedback_id}/tags/{tag_name}/", response_model=MessageResponse)
async def add_tag_to_feedback(feedback_id: int, tag_name: str):
    success = await FeedbackService.add_tag_to_feedback(feedback_id, tag_name)
    if not success:
        raise HTTPException(status_code=404, detail="反馈或标签不存在")
    return {"message": "标签添加成功"}

@router.delete("/feedback/{feedback_id}/tags/{tag_name}/", response_model=MessageResponse)
async def remove_tag_from_feedback(feedback_id: int, tag_name: str):
    success = await FeedbackService.remove_tag_from_feedback(feedback_id, tag_name)
    if not success:
        raise HTTPException(status_code=404, detail="反馈不存在")
    return {"message": "标签移除成功"}

@router.delete("/tags/{tag_id}/", response_model=MessageResponse)
async def delete_tag(tag_id: int):
    success = await TagService.delete_tag(tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="标签不存在")
    return {"message": "标签删除成功"}

# ------------------------
# 统计功能路由
# ------------------------

@router.get("/stats/users/", response_model=UserStats)
async def get_user_stats():
    stats = await StatsService.get_user_stats()
    return stats

@router.get("/stats/feedback/", response_model=FeedbackStats)
async def get_feedback_stats():
    stats = await StatsService.get_feedback_stats()
    return stats

@router.get("/stats/hot-tags/", response_model=List[HotTag])
async def get_hot_tags(limit: int = 10):
    hot_tags = await StatsService.get_hot_tags(limit=limit)
    return hot_tags

@router.get("/stats/feedback-trend/", response_model=List[FeedbackTrend])
async def get_feedback_trend(days: int = 30):
    trend = await StatsService.get_feedback_trend(days=days)
    return trend

# ------------------------
# 通知功能路由
# ------------------------

@router.get("/users/{user_id}/notifications/", response_model=NotificationListResponse)
async def get_user_notifications(user_id: int, skip: int = 0, limit: int = 100):
    user = await UserService.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    notifications = await NotificationService.get_user_notifications(user_id=user_id, skip=skip, limit=limit)
    unread_count = await NotificationService.get_user_notifications_count(user_id=user_id, unread_only=True)
    return {"notifications": notifications, "total": len(notifications), "unread_count": unread_count}

@router.patch("/notifications/{notification_id}/read/", response_model=MessageResponse)
async def mark_notification_as_read(notification_id: int):
    success = await NotificationService.mark_notification_as_read(notification_id)
    if not success:
        raise HTTPException(status_code=404, detail="通知不存在")
    return {"message": "通知已标记为已读"}

@router.patch("/users/{user_id}/notifications/read-all/", response_model=MessageResponse)
async def mark_all_notifications_as_read(user_id: int):
    user = await UserService.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    await NotificationService.mark_all_notifications_as_read(user_id)
    return {"message": "所有通知已标记为已读"}

@router.delete("/users/{user_id}/notifications/", response_model=MessageResponse)
async def clear_all_notifications(user_id: int):
    user = await UserService.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    await NotificationService.clear_all_notifications(user_id)
    return {"message": "所有通知已清除"}

# ------------------------
# 测试数据生成路由
# ------------------------

@router.post("/test-data/", response_model=MessageResponse)
async def generate_test_data():
    test_users = [
        {"username": "user1", "email": "user1@example.com", "name": "User 1", "password": "password1"},
        {"username": "user2", "email": "user2@example.com", "name": "User 2", "password": "password2"},
        {"username": "user3", "email": "user3@example.com", "name": "User 3", "password": "password3"}
    ]
    
    for user_data in test_users:
        user = UserCreate(**user_data)
        existing = await UserService.get_user_by_username(user.username)
        if not existing:
            await UserService.create_user(user)
    
    test_tags = [
        {"name": "bug", "description": "Bug 报告"},
        {"name": "feature", "description": "功能请求"},
        {"name": "improvement", "description": "改进建议"},
        {"name": "question", "description": "问题咨询"}
    ]
    
    for tag_data in test_tags:
        tag = TagCreate(**tag_data)
        await TagService.create_tag(tag)
    
    test_feedback = [
        {"title": "登录页面有问题", "content": "登录按钮点击无响应", "user_id": 1},
        {"title": "希望添加深色模式", "content": "当前只有浅色模式，希望添加深色模式", "user_id": 2},
        {"title": "页面加载速度慢", "content": "首页加载需要5秒以上", "user_id": 3}
    ]
    
    feedback_tags = [
        ["bug"],
        ["feature"],
        ["bug", "improvement"]
    ]
    
    for i, fb_data in enumerate(test_feedback):
        fb = FeedbackCreate(**fb_data)
        fb_existing = await FeedbackService.search_feedback(fb_data["title"], skip=0, limit=1)
        if not fb_existing:
            created_fb = await FeedbackService.create_feedback(fb)
            for tag_name in feedback_tags[i]:
                await FeedbackService.add_tag_to_feedback(created_fb.id, tag_name)
    
    return {"message": "测试数据生成成功"}
