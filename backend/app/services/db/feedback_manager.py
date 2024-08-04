# app/services/feedback_manager.py

import logging
from typing import Optional
import pymysql
from app.core.config import settings
from app.models.feedback import Feedback

class FeedbackManager:
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

    def create_feedback(self, user_id: str, session_id: int, message_id: str, rating: int) -> Optional[Feedback]:
        try:
            with self.conn.cursor() as cursor:
                sql = "INSERT INTO feedbacks (user_id, session_id, message_id, rating) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (user_id, session_id, message_id, rating))
                self.conn.commit()
                feedback_id = cursor.lastrowid
                return Feedback(id=feedback_id, user_id=user_id, session_id=session_id, message_id=message_id, rating=rating)
        except pymysql.Error as e:
            logging.error(f"Error creating Feedback: {str(e)}")
            self.conn.rollback()
            return None

    def get_feedback_by_id(self, feedback_id: int) -> Optional[Feedback]:
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM feedbacks WHERE id = %s"
                cursor.execute(sql, (feedback_id,))
                result = cursor.fetchone()
                if result:
                    return Feedback(id=result[0], user_id=result[1], session_id=result[2], message_id=result[3], rating=result[4])
                else:
                    return None
        except pymysql.Error as e:
            logging.error(f"Error getting Feedback by ID: {str(e)}")
            return None

    def update_feedback(self, feedback_id: int, rating: Optional[int] = None) -> Optional[Feedback]:
        try:
            with self.conn.cursor() as cursor:
                update_fields = []
                update_values = []
                if rating is not None:
                    update_fields.append("rating = %s")
                    update_values.append(rating)

                if update_fields:
                    sql = "UPDATE feedbacks SET " + ", ".join(update_fields) + " WHERE id = %s"
                    update_values.append(feedback_id)
                    cursor.execute(sql, update_values)
                    self.conn.commit()

                return self.get_feedback_by_id(feedback_id)
        except pymysql.Error as e:
            logging.error(f"Error updating Feedback: {str(e)}")
            self.conn.rollback()
            return None

    def delete_feedback(self, feedback_id: int) -> bool:
        try:
            with self.conn.cursor() as cursor:
                sql = "DELETE FROM feedbacks WHERE id = %s"
                cursor.execute(sql, (feedback_id,))
                self.conn.commit()
                return True
        except pymysql.Error as e:
            logging.error(f"Error deleting Feedback: {str(e)}")
            self.conn.rollback()
            return False