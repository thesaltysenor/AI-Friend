# app/services/db/image_service.py

from sqlalchemy.orm import Session
from app.models.image import GeneratedImage
from typing import List, Optional

class ImageService:
    def __init__(self, db: Session):
        self.db = db

    def create_generated_image(self, prompt: str, prompt_id: str, image_url: str, user_id: int, character_id: int) -> GeneratedImage:
        db_image = GeneratedImage(
            prompt=prompt,
            prompt_id=prompt_id,
            image_url=image_url,
            user_id=user_id,
            character_id=character_id
        )
        self.db.add(db_image)
        self.db.commit()
        self.db.refresh(db_image)
        return db_image

    def get_generated_image_by_id(self, image_id: int) -> Optional[GeneratedImage]:
        return self.db.query(GeneratedImage).filter(GeneratedImage.id == image_id).first()

    def get_generated_image_by_prompt_id(self, prompt_id: str) -> Optional[GeneratedImage]:
        return self.db.query(GeneratedImage).filter(GeneratedImage.prompt_id == prompt_id).first()

    def get_user_generated_images(self, user_id: int) -> List[GeneratedImage]:
        return self.db.query(GeneratedImage).filter(GeneratedImage.user_id == user_id).all()

    def get_character_generated_images(self, character_id: int) -> List[GeneratedImage]:
        return self.db.query(GeneratedImage).filter(GeneratedImage.character_id == character_id).all()

    def update_image_url(self, prompt_id: str, image_url: str) -> Optional[GeneratedImage]:
        db_image = self.get_generated_image_by_prompt_id(prompt_id)
        if db_image:
            db_image.image_url = image_url
            self.db.commit()
            self.db.refresh(db_image)
        return db_image

    def delete_generated_image(self, image_id: int) -> bool:
        db_image = self.get_generated_image_by_id(image_id)
        if db_image:
            self.db.delete(db_image)
            self.db.commit()
            return True
        return False