# app/services/db/interaction_manager.py

import logging
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.interaction import Interaction
from app.models.user import User
from app.services.db.character_database import AIPersonalityManager

class InteractionManager:
    def __init__(self, db: Session):
        self.db = db
        self.ai_personality_manager = AIPersonalityManager(db)

    def create_interaction(self, user_id: str, ai_personality_id: Optional[int], interaction_type: str) -> Optional[Interaction]:
        try:
            # Check if the user exists
            user = self.db.query(User).filter(User.user_id == user_id).first()
            if not user:
                logging.error(f"User with id {user_id} does not exist")
                return None

            # If ai_personality_id is not provided, use the default (adaptive) one
            if ai_personality_id is None:
                ai_personality_id = self.ai_personality_manager.get_or_create_default_ai_personality()

            # Create the interaction
            new_interaction = Interaction(
                user_id=user_id,
                ai_personality_id=ai_personality_id,
                interaction_type=interaction_type
            )
            self.db.add(new_interaction)
            self.db.commit()
            self.db.refresh(new_interaction)
            return new_interaction
        except SQLAlchemyError as e:
            logging.error(f"Error creating Interaction: {str(e)}")
            self.db.rollback()
            return None

    def get_interaction_by_id(self, interaction_id: int) -> Optional[Interaction]:
        return self.db.query(Interaction).filter(Interaction.id == interaction_id).first()

    def get_interactions_by_user_id(self, user_id: str) -> List[Interaction]:
        return self.db.query(Interaction).filter(Interaction.user_id == user_id).all()

    def update_interaction(self, interaction_id: int, **kwargs) -> Optional[Interaction]:
        interaction = self.get_interaction_by_id(interaction_id)
        if interaction:
            for key, value in kwargs.items():
                if hasattr(interaction, key):
                    setattr(interaction, key, value)
            try:
                self.db.commit()
                self.db.refresh(interaction)
                return interaction
            except SQLAlchemyError as e:
                logging.error(f"Error updating Interaction: {str(e)}")
                self.db.rollback()
                return None
        return None

    def delete_interaction(self, interaction_id: int) -> bool:
        interaction = self.get_interaction_by_id(interaction_id)
        if interaction:
            try:
                self.db.delete(interaction)
                self.db.commit()
                return True
            except SQLAlchemyError as e:
                logging.error(f"Error deleting Interaction: {str(e)}")
                self.db.rollback()
                return False
        return False

    def get_or_create_test_user(self) -> str:
        test_user = self.db.query(User).filter(User.username == 'test_user').first()
        if test_user:
            return test_user.user_id
        else:
            # Create test user
            new_user = User(
                username='test_user',
                email='test@example.com',
                hashed_password='hashed_test_password',
                is_active=True
            )
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user.user_id

    def get_user_id_by_username(self, username: str) -> Optional[str]:
        user = self.db.query(User).filter(User.username == username).first()
        if user:
            return user.user_id
        else:
            return None