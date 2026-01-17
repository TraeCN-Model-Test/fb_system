from typing import Optional, List, Dict
from app.models.tortoise_models import Tag, FeedbackTag
from app.models.pydantic_models import TagCreate, HotTag


class TagService:
    @staticmethod
    async def create_tag(tag_data: TagCreate) -> Tag:
        tag, created = await Tag.get_or_create(
            name=tag_data.name,
            defaults={"description": tag_data.description}
        )
        if not created and tag_data.description:
            tag.description = tag_data.description
            await tag.save()
        return tag
    
    @staticmethod
    async def get_tag(tag_id: int) -> Optional[Tag]:
        return await Tag.get_or_none(id=tag_id)
    
    @staticmethod
    async def get_tag_by_name(name: str) -> Optional[Tag]:
        return await Tag.get_or_none(name=name)
    
    @staticmethod
    async def get_tags(skip: int = 0, limit: int = 100) -> List[Tag]:
        return await Tag.all().offset(skip).limit(limit).order_by("-usage_count")
    
    @staticmethod
    async def get_tags_count() -> int:
        return await Tag.all().count()
    
    @staticmethod
    async def delete_tag(tag_id: int) -> bool:
        tag = await Tag.get_or_none(id=tag_id)
        if not tag:
            return False
        
        await FeedbackTag.filter(tag_id=tag_id).delete()
        await tag.delete()
        return True
    
    @staticmethod
    async def get_hot_tags(limit: int = 10) -> List[HotTag]:
        tags = await Tag.all().order_by("-usage_count").limit(limit)
        
        return [HotTag(name=tag.name, count=tag.usage_count) for tag in tags]
    
    @staticmethod
    async def refresh_tag_usage_counts() -> None:
        tags = await Tag.all()
        for tag in tags:
            count = await FeedbackTag.filter(tag_id=tag.id).count()
            tag.usage_count = count
            await tag.save()
