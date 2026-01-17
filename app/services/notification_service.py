from typing import Optional, List
from app.models.tortoise_models import Notification, User
from app.models.pydantic_models import NotificationCreate


class NotificationService:
    @staticmethod
    async def create_notification(notification_data: NotificationCreate) -> Notification:
        user = await User.get_or_none(id=notification_data.user_id)
        if not user:
            return None
        
        notification = await Notification.create(
            user_id=notification_data.user_id,
            title=notification_data.title,
            content=notification_data.content
        )
        return notification
    
    @staticmethod
    async def get_notification(notification_id: int) -> Optional[Notification]:
        return await Notification.get_or_none(id=notification_id)
    
    @staticmethod
    async def get_user_notifications(user_id: int, skip: int = 0, limit: int = 100) -> List[Notification]:
        return await Notification.filter(user_id=user_id).offset(skip).limit(limit).order_by("-created_at")
    
    @staticmethod
    async def get_user_notifications_count(user_id: int, unread_only: bool = False) -> int:
        query = Notification.filter(user_id=user_id)
        if unread_only:
            query = query.filter(is_read=False)
        return await query.count()
    
    @staticmethod
    async def mark_notification_as_read(notification_id: int) -> bool:
        notification = await Notification.get_or_none(id=notification_id)
        if not notification:
            return False
        
        notification.is_read = True
        await notification.save()
        return True
    
    @staticmethod
    async def mark_all_notifications_as_read(user_id: int) -> bool:
        updated_count = await Notification.filter(user_id=user_id, is_read=False).update(is_read=True)
        return updated_count > 0
    
    @staticmethod
    async def clear_all_notifications(user_id: int) -> bool:
        deleted_count = await Notification.filter(user_id=user_id).delete()
        return deleted_count > 0
