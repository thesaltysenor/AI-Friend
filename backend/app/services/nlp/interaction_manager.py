
# app/services/nlp/interaction_manager.py

import uuid
import bcrypt
import logging
from typing import Optional, List, Union
from datetime import datetime
import pymysql
import sqlite3
from app.core.config import settings
from app.models.interaction import Interaction
from app.services.db.ai_personality_manager import AIPersonalityManager


class InteractionManager:
    def __init__(self, connection=None):
        self.conn = connection
        self.ai_personality_manager = AIPersonalityManager()
        if not self.conn:
            try:
                self.conn = pymysql.connect(
                    host=settings.MYSQL_HOSTNAME,
                    user=settings.MYSQL_USER,
                    password=settings.MYSQL_PASSWORD,
                    database=settings.MYSQL_DB,
                    port=settings.MYSQL_PORT
                )
            except pymysql.Error as e:
                logging.error(f"Error connecting to the database: {str(e)}")
                raise

    def _get_cursor(self):
        if isinstance(self.conn, sqlite3.Connection):
            return self.conn.cursor()
        return self.conn.cursor()

    def create_interaction(self, user_id: str, ai_personality_id: Optional[int], interaction_type: str) -> Optional[Interaction]:
        try:
            with self.conn.cursor() as cursor:
                # If user_id is 'test_user', get or create the test user
                if user_id == 'test_user':
                    user_id = self.get_or_create_test_user()
            
                # Check if the user exists
                check_user_sql = "SELECT user_id FROM users WHERE user_id = %s"
                cursor.execute(check_user_sql, (user_id,))
                if not cursor.fetchone():
                    logging.error(f"User with id {user_id} does not exist")
                    return None

                # If ai_personality_id is not provided, use the default (adaptive) one
                if ai_personality_id is None:
                    ai_personality_id = self.ai_personality_manager.get_or_create_default_ai_personality()

                # Proceed with creating the interaction
                sql = "INSERT INTO interaction (user_id, ai_personality_id, interaction_type, timestamp) VALUES (%s, %s, %s, %s)"
                timestamp = datetime.utcnow()
                cursor.execute(sql, (user_id, ai_personality_id, interaction_type, timestamp))
                self.conn.commit()
                interaction_id = cursor.lastrowid
                return Interaction(id=interaction_id, user_id=user_id, ai_personality_id=ai_personality_id, interaction_type=interaction_type, timestamp=timestamp)
        except pymysql.Error as e:
            logging.error(f"Error creating Interaction: {str(e)}")
            self.conn.rollback()
            return None

    def get_or_create_test_user(self) -> str:
        cursor = self._get_cursor()
    
        # Check if test user exists
        sql = "SELECT user_id FROM users WHERE username = 'test_user'"
        cursor.execute(sql)
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            # Create test user
            user_id = str(uuid.uuid4())
            hashed_password = bcrypt.hashpw('test_password'.encode('utf-8'), bcrypt.gensalt())
            sql = "INSERT INTO users (user_id, username, email, hashed_password, is_active) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (user_id, 'test_user', 'test@example.com', hashed_password, True))
            self.conn.commit()
            return user_id
    
    def get_user_id_by_username(self, username: str) -> int:
        cursor = self._get_cursor()
        sql = "SELECT id FROM users WHERE username = %s"
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            raise ValueError(f"No user found with username: {username}")

    def get_interactions_by_user_id(self, user_id: int) -> List[Interaction]:
        try:
            cursor = self._get_cursor()
            sql = "SELECT * FROM interaction WHERE user_id = %s"
            cursor.execute(sql, (user_id,))
            results = cursor.fetchall()
            interactions = []
            for result in results:
                interaction = Interaction(id=result[0], user_id=result[1], ai_personality_id=result[2], interaction_type=result[3], timestamp=result[4])
                interactions.append(interaction)
            return interactions
        except (pymysql.Error, sqlite3.Error) as e:
            logging.error(f"Error getting Interactions by User ID: {str(e)}")
            return []

    def delete_interaction(self, interaction_id: int) -> bool:
        try:
            cursor = self._get_cursor()
            sql = "DELETE FROM interaction WHERE id = %s"
            cursor.execute(sql, (interaction_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except (pymysql.Error, sqlite3.Error) as e:
            logging.error(f"Error deleting Interaction: {str(e)}")
            self.conn.rollback()
            return False
    