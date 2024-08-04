# app/services/user_preference_manager.py

import logging
from typing import Optional
import pymysql
from app.core.config import settings
from app.models.user_preference import UserPreference

class UserPreferenceManager:
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

    def create_user_preference(self, user_id: int, preference_type: str, preference_value: str) -> Optional[UserPreference]:
        try:
            with self.conn.cursor() as cursor:
                sql = "INSERT INTO user_preferences (user_id, preference_type, preference_value) VALUES (%s, %s, %s)"
                cursor.execute(sql, (user_id, preference_type, preference_value))
                self.conn.commit()
                user_preference_id = cursor.lastrowid
                return UserPreference(id=user_preference_id, user_id=user_id, preference_type=preference_type, preference_value=preference_value)
        except pymysql.Error as e:
            logging.error(f"Error creating User Preference: {str(e)}")
            self.conn.rollback()
            return None

    def get_user_preference_by_id(self, user_preference_id: int) -> Optional[UserPreference]:
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM user_preferences WHERE id = %s"
                cursor.execute(sql, (user_preference_id,))
                result = cursor.fetchone()
                if result:
                    return UserPreference(id=result[0], user_id=result[1], preference_type=result[2], preference_value=result[3])
                else:
                    return None
        except pymysql.Error as e:
            logging.error(f"Error getting User Preference by ID: {str(e)}")
            return None

    def update_user_preference(self, user_preference_id: int, preference_value: Optional[str] = None) -> Optional[UserPreference]:
        try:
            with self.conn.cursor() as cursor:
                update_fields = []
                update_values = []
                if preference_value is not None:
                    update_fields.append("preference_value = %s")
                    update_values.append(preference_value)

                if update_fields:
                    sql = "UPDATE user_preferences SET " + ", ".join(update_fields) + " WHERE id = %s"
                    update_values.append(user_preference_id)
                    cursor.execute(sql, update_values)
                    self.conn.commit()

                return self.get_user_preference_by_id(user_preference_id)
        except pymysql.Error as e:
            logging.error(f"Error updating User Preference: {str(e)}")
            self.conn.rollback()
            return None

    def delete_user_preference(self, user_preference_id: int) -> bool:
        try:
            with self.conn.cursor() as cursor:
                sql = "DELETE FROM user_preferences WHERE id = %s"
                cursor.execute(sql, (user_preference_id,))
                self.conn.commit()
                return True
        except pymysql.Error as e:
            logging.error(f"Error deleting User Preference: {str(e)}")
            self.conn.rollback()
            return False