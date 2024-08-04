# app/services/entity_manager.py

import logging
from typing import Optional
import pymysql
from app.core.config import settings
from app.models.entity import Entity

class EntityManager:
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

    def create_entity(self, entity_name: str, intent_id: int) -> Optional[Entity]:
        try:
            with self.conn.cursor() as cursor:
                sql = "INSERT INTO entities (entity_name, intent_id) VALUES (%s, %s)"
                cursor.execute(sql, (entity_name, intent_id))
                self.conn.commit()
                entity_id = cursor.lastrowid
                return Entity(id=entity_id, entity_name=entity_name, intent_id=intent_id)
        except pymysql.Error as e:
            logging.error(f"Error creating Entity: {str(e)}")
            self.conn.rollback()
            return None

    def get_entity_by_id(self, entity_id: int) -> Optional[Entity]:
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM entities WHERE id = %s"
                cursor.execute(sql, (entity_id,))
                result = cursor.fetchone()
                if result:
                    return Entity(id=result[0], entity_name=result[1], intent_id=result[2])
                else:
                    return None
        except pymysql.Error as e:
            logging.error(f"Error getting Entity by ID: {str(e)}")
            return None

    def update_entity(self, entity_id: int, entity_name: Optional[str] = None, intent_id: Optional[int] = None) -> Optional[Entity]:
        try:
            with self.conn.cursor() as cursor:
                update_fields = []
                update_values = []
                if entity_name is not None:
                    update_fields.append("entity_name = %s")
                    update_values.append(entity_name)
                if intent_id is not None:
                    update_fields.append("intent_id = %s")
                    update_values.append(intent_id)

                if update_fields:
                    sql = "UPDATE entities SET " + ", ".join(update_fields) + " WHERE id = %s"
                    update_values.append(entity_id)
                    cursor.execute(sql, update_values)
                    self.conn.commit()

                return self.get_entity_by_id(entity_id)
        except pymysql.Error as e:
            logging.error(f"Error updating Entity: {str(e)}")
            self.conn.rollback()
            return None

    def delete_entity(self, entity_id: int) -> bool:
        try:
            with self.conn.cursor() as cursor:
                sql = "DELETE FROM entities WHERE id = %s"
                cursor.execute(sql, (entity_id,))
                self.conn.commit()
                return True
        except pymysql.Error as e:
            logging.error(f"Error deleting Entity: {str(e)}")
            self.conn.rollback()
            return False