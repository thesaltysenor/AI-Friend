# app/services/ai_personality_manager.py

import logging
from typing import Optional, List
import pymysql
from app.core.config import settings
from app.models.ai_personality import AIPersonality
from app.services.characters.character_details import CHARACTER_DETAILS


class AIPersonalityManager:
    def __init__(self):
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
            self.conn = None
    
    def _get_cursor(self):
        if self.conn is None:
            raise ConnectionError("Database connection is not established")
        return self.conn.cursor()

    def create_ai_personality(self, name: str, description: str, personality_traits: str, character_type: str = "default", available: bool = True) -> Optional[AIPersonality]:
        try:
            with self.conn.cursor() as cursor:
                sql = "INSERT INTO ai_personality (name, description, personality_traits, character_type, available) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (name, description, personality_traits, character_type, available))
                self.conn.commit()
                ai_personality_id = cursor.lastrowid
                return AIPersonality(id=ai_personality_id, name=name, description=description, personality_traits=personality_traits, character_type=character_type, available=available)
        except pymysql.Error as e:
            logging.error(f"Error creating AI Personality: {str(e)}")
            self.conn.rollback()
            return None

    def get_ai_personality_by_id(self, ai_personality_id: int) -> Optional[AIPersonality]:
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT id, name, description, personality_traits, character_type, available FROM ai_personality WHERE id = %s"
                cursor.execute(sql, (ai_personality_id,))
                result = cursor.fetchone()
                if result:
                    return AIPersonality(id=result[0], name=result[1], description=result[2], personality_traits=result[3], character_type=result[4], available=result[5])
                else:
                    return None
        except pymysql.Error as e:
            logging.error(f"Error getting AI Personality by ID: {str(e)}")
            return None

    def update_ai_personality(self, ai_personality_id: int, name: Optional[str] = None, description: Optional[str] = None,
                         personality_traits: Optional[str] = None, character_type: Optional[str] = None, available: Optional[bool] = None) -> Optional[AIPersonality]:
        try:
            with self.conn.cursor() as cursor:
                update_fields = []
                update_values = []
                if name is not None:
                    update_fields.append("name = %s")
                    update_values.append(name)
                if description is not None:
                    update_fields.append("description = %s")
                    update_values.append(description)
                if personality_traits is not None:
                    update_fields.append("personality_traits = %s")
                    update_values.append(personality_traits)
                if character_type is not None:
                    update_fields.append("character_type = %s")
                    update_values.append(character_type)
                if available is not None:
                    update_fields.append("available = %s")
                    update_values.append(available)

                if update_fields:
                    sql = "UPDATE ai_personality SET " + ", ".join(update_fields) + " WHERE id = %s"
                    update_values.append(ai_personality_id)
                    cursor.execute(sql, update_values)
                    self.conn.commit()

                return self.get_ai_personality_by_id(ai_personality_id)
        except pymysql.Error as e:
            logging.error(f"Error updating AI Personality: {str(e)}")
            self.conn.rollback()
            return None

    def delete_ai_personality(self, ai_personality_id: int) -> bool:
        try:
            with self.conn.cursor() as cursor:
                sql = "DELETE FROM ai_personality WHERE id = %s"
                cursor.execute(sql, (ai_personality_id,))
                self.conn.commit()
                return True
        except pymysql.Error as e:
            logging.error(f"Error deleting AI Personality: {str(e)}")
            self.conn.rollback()
            return False
        
    def get_all_ai_personalities(self) -> List[AIPersonality]:
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT id, name, description, personality_traits, character_type, available FROM ai_personality"
                cursor.execute(sql)
                results = cursor.fetchall()
                return [AIPersonality(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    personality_traits=row[3],
                    character_type=row[4],
                    available=row[5]
                ) for row in results]
        except pymysql.Error as e:
            logging.error(f"Error getting all AI Personalities: {str(e)}")
            return []
        
    def get_default_personality(self):
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT id, name, description, personality_traits, character_type, available FROM ai_personality LIMIT 1"
                cursor.execute(sql)
                result = cursor.fetchone()
                if result:
                    return AIPersonality(id=result[0], name=result[1], description=result[2], personality_traits=result[3], character_type=result[4], available=result[5])
                else:
                    # If no personalities in the database, create a default one
                    return self.create_ai_personality(
                        name="Default AI",
                        description="A friendly AI assistant",
                        personality_traits="Helpful, friendly, knowledgeable",
                        character_type="default",
                        available=True
                    )
        except pymysql.Error as e:
            logging.error(f"Error getting default AI Personality: {str(e)}")
            return None
        
    def insert_or_update_character(self, character_type, details):
        try:
            with self.conn.cursor() as cursor:
                # Check if the character already exists
                sql_check = "SELECT id FROM ai_personality WHERE character_type = %s"
                cursor.execute(sql_check, (character_type,))
                result = cursor.fetchone()

                if result:
                    # Update existing character
                    sql = """
                    UPDATE ai_personality 
                    SET name = %s, description = %s, personality_traits = %s, available = %s
                    WHERE character_type = %s
                    """
                    cursor.execute(sql, (
                        details['name'],
                        details['backstory'],
                        ', '.join(details['personality_traits']),
                        True,
                        character_type
                    ))
                else:
                    # Insert new character
                    sql = """
                    INSERT INTO ai_personality (name, description, personality_traits, character_type, available)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        details['name'],
                        details['backstory'],
                        ', '.join(details['personality_traits']),
                        character_type,
                        True
                    ))

                self.conn.commit()
                logging.info(f"Character {character_type} inserted/updated successfully")
        except Exception as e:
            logging.error(f"Error inserting/updating character {character_type}: {str(e)}")
            self.conn.rollback()

    def populate_characters(self):
        for character_type, details in CHARACTER_DETAILS.items():
            self.insert_or_update_character(character_type, details)

    def get_or_create_default_ai_personality(self) -> int:
        try:
            with self.conn.cursor() as cursor:
                # Check if default Adaptive AI Friend exists
                sql = "SELECT id FROM ai_personality WHERE LOWER(character_type) = 'adaptive' LIMIT 1"
                cursor.execute(sql)
                result = cursor.fetchone()
                
                if result:
                    return result[0]
                else:
                    # Create default Adaptive AI Friend
                    sql = """
                    INSERT INTO ai_personality 
                    (name, description, personality_traits, character_type, available) 
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        "Adaptive AI Friend",
                        "I'm an AI Friend that adapts my personality based on our conversation.",
                        "Adaptive, Observant, Evolving",
                        "adaptive",
                        True
                    ))
                    self.conn.commit()
                    return cursor.lastrowid
        except pymysql.Error as e:
            logging.error(f"Error in get_or_create_default_ai_personality: {str(e)}")
            self.conn.rollback()
            raise