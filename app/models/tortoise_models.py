from tortoise import fields
from tortoise.models import Model
from tortoise import Tortoise
from datetime import datetime
from typing import Optional, List


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True, index=True)
    email = fields.CharField(max_length=100, unique=True, index=True)
    name = fields.CharField(max_length=100)
    password_hash = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    feedbacks: fields.ReverseRelation["Feedback"]
    comments: fields.ReverseRelation["Comment"]
    notifications: fields.ReverseRelation["Notification"]
    
    class Meta:
        table = "users"


class Feedback(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=200, index=True)
    content = fields.TextField()
    status = fields.CharField(max_length=20, default="pending", index=True)
    created_at = fields.DatetimeField(auto_now_add=True, index=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="feedbacks", on_delete=fields.CASCADE
    )
    comments: fields.ReverseRelation["Comment"]
    feedback_tags: fields.ReverseRelation["FeedbackTag"]
    
    class Meta:
        table = "feedbacks"


class Comment(Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="comments", on_delete=fields.CASCADE
    )
    feedback: fields.ForeignKeyRelation[Feedback] = fields.ForeignKeyField(
        "models.Feedback", related_name="comments", on_delete=fields.CASCADE
    )
    
    class Meta:
        table = "comments"


class Tag(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True, index=True)
    description = fields.CharField(max_length=200, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    usage_count = fields.IntField(default=0)
    
    feedback_tags: fields.ReverseRelation["FeedbackTag"]
    
    class Meta:
        table = "tags"


class FeedbackTag(Model):
    id = fields.IntField(pk=True)
    
    feedback: fields.ForeignKeyRelation[Feedback] = fields.ForeignKeyField(
        "models.Feedback", related_name="feedback_tags", on_delete=fields.CASCADE
    )
    tag: fields.ForeignKeyRelation[Tag] = fields.ForeignKeyField(
        "models.Tag", related_name="feedback_tags", on_delete=fields.CASCADE
    )
    
    class Meta:
        table = "feedback_tags"
        unique_together = ("feedback", "tag")


class Notification(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=200)
    content = fields.TextField()
    is_read = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True, index=True)
    
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="notifications", on_delete=fields.CASCADE
    )
    
    class Meta:
        table = "notifications"


async def init_db(db_url: str = "sqlite://./feedback.db"):
    await Tortoise.init(
        db_url=db_url,
        modules={
            "models": ["app.models.tortoise_models"]
        }
    )
    await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()