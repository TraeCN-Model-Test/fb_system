from typing import Optional, List
from app.models.tortoise_models import Comment, Feedback
from app.models.pydantic_models import CommentCreate


class CommentService:
    @staticmethod
    async def create_comment(comment_data: CommentCreate) -> Comment:
        feedback = await Feedback.get_or_none(id=comment_data.feedback_id)
        if not feedback:
            return None
        
        comment = await Comment.create(
            content=comment_data.content,
            user_id=comment_data.user_id,
            feedback_id=comment_data.feedback_id
        )
        return comment
    
    @staticmethod
    async def get_comment(comment_id: int) -> Optional[Comment]:
        return await Comment.get_or_none(id=comment_id)
    
    @staticmethod
    async def get_comments(feedback_id: int, skip: int = 0, limit: int = 100) -> List[Comment]:
        return await Comment.filter(feedback_id=feedback_id).offset(skip).limit(limit).order_by("-created_at")
    
    @staticmethod
    async def get_comments_count(feedback_id: int) -> int:
        return await Comment.filter(feedback_id=feedback_id).count()
    
    @staticmethod
    async def update_comment(comment_id: int, content: str) -> Optional[Comment]:
        comment = await Comment.get_or_none(id=comment_id)
        if not comment:
            return None
        
        comment.content = content
        await comment.save()
        return comment
    
    @staticmethod
    async def delete_comment(comment_id: int) -> bool:
        comment = await Comment.get_or_none(id=comment_id)
        if not comment:
            return False
        
        await comment.delete()
        return True
