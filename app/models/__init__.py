from app.models.pydantic_models import (
    User, UserCreate, UserUpdate, UserListResponse,
    Feedback, FeedbackCreate, FeedbackUpdate, FeedbackStatusUpdate, FeedbackListResponse,
    Comment, CommentCreate, CommentUpdate, CommentListResponse,
    Tag, TagCreate, TagListResponse,
    Notification, NotificationCreate, NotificationListResponse,
    UserStats, FeedbackStats, HotTag, FeedbackTrend,
    MessageResponse
)

from app.models.tortoise_models import (
    User as UserModel,
    Feedback as FeedbackModel,
    Comment as CommentModel,
    Tag as TagModel,
    FeedbackTag as FeedbackTagModel,
    Notification as NotificationModel,
    init_db,
    close_db
)

__all__ = [
    "User", "UserCreate", "UserUpdate", "UserListResponse",
    "Feedback", "FeedbackCreate", "FeedbackUpdate", "FeedbackStatusUpdate", "FeedbackListResponse",
    "Comment", "CommentCreate", "CommentUpdate", "CommentListResponse",
    "Tag", "TagCreate", "TagListResponse",
    "Notification", "NotificationCreate", "NotificationListResponse",
    "UserStats", "FeedbackStats", "HotTag", "FeedbackTrend",
    "MessageResponse",
    "UserModel", "FeedbackModel", "CommentModel", "TagModel", "FeedbackTagModel", "NotificationModel",
    "init_db", "close_db"
]