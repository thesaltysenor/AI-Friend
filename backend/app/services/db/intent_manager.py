# app/services/intent_manager.py

import logging
from typing import Optional
import pymysql
from app.core.config import settings
from app.models.intent import Intent

class IntentManager:
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

    def create_intent(self, intent_name: str, description: str) -> Optional[Intent]:
        try:
            with self.conn.cursor() as cursor:
                sql = "INSERT INTO intents (intent_name, description) VALUES (%s, %s)"
                cursor.execute(sql, (intent_name, description))
                self.conn.commit()
                intent_id = cursor.lastrowid
                return Intent(id=intent_id, intent_name=intent_name, description=description)
        except pymysql.Error as e:
            logging.error(f"Error creating Intent: {str(e)}")
            self.conn.rollback()
            return None

    def get_intent_by_id(self, intent_id: int) -> Optional[Intent]:
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM intents WHERE id = %s"
                cursor.execute(sql, (intent_id,))
                result = cursor.fetchone()
                if result:
                    return Intent(id=result[0], intent_name=result[1], description=result[2])
                else:
                    return None
        except pymysql.Error as e:
            logging.error(f"Error getting Intent by ID: {str(e)}")
            return None

    def update_intent(self, intent_id: int, intent_name: Optional[str] = None, description: Optional[str] = None) -> Optional[Intent]:
        try:
            with self.conn.cursor() as cursor:
                update_fields = []
                update_values = []
                if intent_name is not None:
                    update_fields.append("intent_name = %s")
                    update_values.append(intent_name)
                if description is not None:
                    update_fields.append("description = %s")
                    update_values.append(description)

                if update_fields:
                    sql = "UPDATE intents SET " + ", ".join(update_fields) + " WHERE id = %s"
                    update_values.append(intent_id)
                    cursor.execute(sql, update_values)
                    self.conn.commit()

                return self.get_intent_by_id(intent_id)
        except pymysql.Error as e:
            logging.error(f"Error updating Intent: {str(e)}")
            self.conn.rollback()
            return None

    def delete_intent(self, intent_id: int) -> bool:
        try:
            with self.conn.cursor() as cursor:
                sql = "DELETE FROM intents WHERE id = %s"
                cursor.execute(sql, (intent_id,))
                self.conn.commit()
                return True
        except pymysql.Error as e:
            logging.error(f"Error deleting Intent: {str(e)}")
            self.conn.rollback()
            return False