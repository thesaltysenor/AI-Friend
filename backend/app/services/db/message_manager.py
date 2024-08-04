# app/services/message_manager.py

import logging
from typing import Optional
import pymysql
from app.core.config import settings
from app.models.messages import Message

class MessageManager:
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

    def create_message(self, role: str, content: str, user_id: str, relevance: float = 1.0) -> Optional[Message]:
        try:
            with self.conn.cursor() as cursor:
                sql = "INSERT INTO messages (role, content, user_id, relevance) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (role, content, user_id, relevance))
                self.conn.commit()
                message_id = cursor.lastrowid
                return Message(id=message_id, role=role, content=content, user_id=user_id, relevance=relevance)
        except pymysql.Error as e:
            logging.error(f"Error creating Message: {str(e)}")
            self.conn.rollback()
            return None

    def get_message_by_id(self, message_id: int) -> Optional[Message]:
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM messages WHERE id = %s"
                cursor.execute(sql, (message_id,))
                result = cursor.fetchone()
                if result:
                    return Message(id=result[0], role=result[1], content=result[2], timestamp=result[3], user_id=result[4], relevance=result[5])
                else:
                    return None
        except pymysql.Error as e:
            logging.error(f"Error getting Message by ID: {str(e)}")
            return None

    def update_message(self, message_id: int, role: Optional[str] = None, content: Optional[str] = None, relevance: Optional[float] = None) -> Optional[Message]:
        try:
            with self.conn.cursor() as cursor:
                update_fields = []
                update_values = []
                if role is not None:
                    update_fields.append("role = %s")
                    update_values.append(role)
                if content is not None:
                    update_fields.append("content = %s")
                    update_values.append(content)
                if relevance is not None:
                    update_fields.append("relevance = %s")
                    update_values.append(relevance)

                if update_fields:
                    sql = "UPDATE messages SET " + ", ".join(update_fields) + " WHERE id = %s"
                    update_values.append(message_id)
                    cursor.execute(sql, update_values)
                    self.conn.commit()

                return self.get_message_by_id(message_id)
        except pymysql.Error as e:
            logging.error(f"Error updating Message: {str(e)}")
            self.conn.rollback()
            return None

    def delete_message(self, message_id: int) -> bool:
        try:
            with self.conn.cursor() as cursor:
                sql = "DELETE FROM messages WHERE id = %s"
                cursor.execute(sql, (message_id,))
                self.conn.commit()
                return True
        except pymysql.Error as e:
            logging.error(f"Error deleting Message: {str(e)}")
            self.conn.rollback()
            return False