# app/services/session_manager.py

import logging
from typing import Optional
from datetime import datetime, timezone
import pymysql
from app.core.config import settings
from app.models.session import Session

class SessionManager:
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

    def create_session(self, user_id: int, status: str) -> Optional[Session]:
        try:
            with self.conn.cursor() as cursor:
                start_time = datetime.now(timezone.utc)
                sql = "INSERT INTO sessions (user_id, start_time, status) VALUES (%s, %s, %s)"
                cursor.execute(sql, (user_id, start_time, status))
                self.conn.commit()
                session_id = cursor.lastrowid
                return Session(id=session_id, user_id=user_id, start_time=start_time, status=status)
        except pymysql.Error as e:
            logging.error(f"Error creating Session: {str(e)}")
            self.conn.rollback()
            return None

    def get_session_by_id(self, session_id: int) -> Optional[Session]:
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM sessions WHERE id = %s"
                cursor.execute(sql, (session_id,))
                result = cursor.fetchone()
                if result:
                    return Session(id=result[0], user_id=result[1], start_time=result[2], end_time=result[3], status=result[4])
                else:
                    return None
        except pymysql.Error as e:
            logging.error(f"Error getting Session by ID: {str(e)}")
            return None

    def update_session(self, session_id: int, end_time: Optional[datetime] = None, status: Optional[str] = None) -> Optional[Session]:
        try:
            with self.conn.cursor() as cursor:
                update_fields = []
                update_values = []
                if end_time is not None:
                    update_fields.append("end_time = %s")
                    update_values.append(end_time)
                if status is not None:
                    update_fields.append("status = %s")
                    update_values.append(status)

                if update_fields:
                    sql = "UPDATE sessions SET " + ", ".join(update_fields) + " WHERE id = %s"
                    update_values.append(session_id)
                    cursor.execute(sql, update_values)
                    self.conn.commit()

                return self.get_session_by_id(session_id)
        except pymysql.Error as e:
            logging.error(f"Error updating Session: {str(e)}")
            self.conn.rollback()
            return None

    def delete_session(self, session_id: int) -> bool:
        try:
            with self.conn.cursor() as cursor:
                sql = "DELETE FROM sessions WHERE id = %s"
                cursor.execute(sql, (session_id,))
                self.conn.commit()
                return True
        except pymysql.Error as e:
            logging.error(f"Error deleting Session: {str(e)}")
            self.conn.rollback()
            return False