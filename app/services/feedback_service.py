from typing import Optional, List
from tortoise.functions import Count
from tortoise.queryset import Q
from app.models.tortoise_models import Feedback, FeedbackTag, Tag
from app.models.pydantic_models import FeedbackCreate, FeedbackUpdate


class FeedbackService:
    @staticmethod
    async def create_feedback(feedback_data: FeedbackCreate) -> Feedback:
        feedback = await Feedback.create(
            title=feedback_data.title,
            content=feedback_data.content,
            user_id=feedback_data.user_id,
            status="pending"
        )
        return feedback
    
    @staticmethod
    async def get_feedback(feedback_id: int) -> Optional[Feedback]:
        feedback = await Feedback.get_or_none(id=feedback_id)
        if feedback:
            feedback.tags = await FeedbackService._get_feedback_tags(feedback.id)
        return feedback
    
    @staticmethod
    async def get_feedback_list(
        skip: int = 0, 
        limit: int = 100, 
        status: Optional[str] = None
    ) -> List[Feedback]:
        query = Feedback.all()
        if status:
            query = query.filter(status=status)
        
        feedbacks = await query.offset(skip).limit(limit).order_by("-created_at")
        
        for feedback in feedbacks:
            feedback.tags = await FeedbackService._get_feedback_tags(feedback.id)
        
        return feedbacks
    
    @staticmethod
    async def get_feedback_count(status: Optional[str] = None) -> int:
        query = Feedback.all()
        if status:
            query = query.filter(status=status)
        return await query.count()
    
    @staticmethod
    async def search_feedback(keyword: str, skip: int = 0, limit: int = 100) -> List[Feedback]:
        query = Feedback.filter(
            Q(title__icontains=keyword) | Q(content__icontains=keyword)
        )
        
        feedbacks = await query.offset(skip).limit(limit).order_by("-created_at")
        
        for feedback in feedbacks:
            feedback.tags = await FeedbackService._get_feedback_tags(feedback.id)
        
        return feedbacks
    
    @staticmethod
    async def update_feedback(feedback_id: int, update_data: FeedbackUpdate) -> Optional[Feedback]:
        feedback = await Feedback.get_or_none(id=feedback_id)
        if not feedback:
            return None
        
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(feedback, field, value)
        
        await feedback.save()
        feedback.tags = await FeedbackService._get_feedback_tags(feedback.id)
        return feedback
    
    @staticmethod
    async def update_feedback_status(feedback_id: int, status: str) -> Optional[Feedback]:
        feedback = await Feedback.get_or_none(id=feedback_id)
        if not feedback:
            return None
        
        feedback.status = status
        await feedback.save()
        feedback.tags = await FeedbackService._get_feedback_tags(feedback.id)
        return feedback
    
    @staticmethod
    async def delete_feedback(feedback_id: int) -> bool:
        feedback = await Feedback.get_or_none(id=feedback_id)
        if not feedback:
            return False
        
        await feedback.delete()
        return True
    
    @staticmethod
    async def add_tag_to_feedback(feedback_id: int, tag_name: str) -> bool:
        feedback = await Feedback.get_or_none(id=feedback_id)
        if not feedback:
            return False
        
        tag = await Tag.get_or_none(name=tag_name)
        if not tag:
            return False
        
        await FeedbackTag.get_or_create(feedback_id=feedback_id, tag_id=tag.id)
        
        tag.usage_count += 1
        await tag.save()
        
        return True
    
    @staticmethod
    async def remove_tag_from_feedback(feedback_id: int, tag_name: str) -> bool:
        feedback = await Feedback.get_or_none(id=feedback_id)
        if not feedback:
            return False
        
        tag = await Tag.get_or_none(name=tag_name)
        if not tag:
            return False
        
        feedback_tag = await FeedbackTag.get_or_none(feedback_id=feedback_id, tag_id=tag.id)
        if feedback_tag:
            await feedback_tag.delete()
            if tag.usage_count > 0:
                tag.usage_count -= 1
                await tag.save()
        
        return True
    
    @staticmethod
    async def _get_feedback_tags(feedback_id: int) -> List[str]:
        feedback_tags = await FeedbackTag.filter(feedback_id=feedback_id).prefetch_related("tag")
        return [ft.tag.name for ft in feedback_tags]
