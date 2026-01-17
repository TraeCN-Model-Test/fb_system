from typing import List, Dict
from datetime import datetime, timedelta, date
from app.models.tortoise_models import Feedback
from app.models.pydantic_models import UserStats, FeedbackStats, HotTag, FeedbackTrend
from app.services.user_service import UserService
from app.services.tag_service import TagService


class StatsService:
    @staticmethod
    async def get_user_stats() -> UserStats:
        total_users = await UserService.get_users_count()
        return UserStats(
            total_users=total_users,
            active_users=total_users
        )
    
    @staticmethod
    async def get_feedback_stats() -> FeedbackStats:
        total = await Feedback.all().count()
        pending = await Feedback.filter(status="pending").count()
        in_progress = await Feedback.filter(status="in_progress").count()
        resolved = await Feedback.filter(status="resolved").count()
        closed = await Feedback.filter(status="closed").count()
        
        return FeedbackStats(
            total_feedback=total,
            pending=pending,
            in_progress=in_progress,
            resolved=resolved,
            closed=closed
        )
    
    @staticmethod
    async def get_hot_tags(limit: int = 10) -> List[HotTag]:
        return await TagService.get_hot_tags(limit)
    
    @staticmethod
    async def get_feedback_trend(days: int = 30) -> List[FeedbackTrend]:
        trend = []
        today = date.today()
        
        for i in range(days):
            trend_date = today - timedelta(days=i)
            date_str = trend_date.strftime("%Y-%m-%d")
            
            start_datetime = datetime.combine(trend_date, datetime.min.time())
            end_datetime = datetime.combine(trend_date, datetime.max.time())
            
            count = await Feedback.filter(
                created_at__gte=start_datetime,
                created_at__lte=end_datetime
            ).count()
            
            trend.append(FeedbackTrend(date=date_str, count=count))
        
        trend.reverse()
        return trend
