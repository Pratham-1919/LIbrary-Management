import psycopg2
import logging
from abc import ABC, abstractmethod

conn = psycopg2.connect(
    database="Library_management",
    user="postgres",
    password="Pratham@19",
    host="127.0.0.1",
    port="5432"
)

cursor = conn.cursor()

class BaseManager(ABC):
    """
    Abstract base class providing encapsulation for database operations.
    """
    def __init__(self):
        self._conn = conn
        self._cursor = cursor
        self._logger = logging.getLogger(self.__class__.__name__)

    def _execute_query(self, query, params=None, fetchone=False, fetchall=False, commit=False):
        """Protected method encapsulating cursor execution and error handling."""
        try:
            self._cursor.execute(query, params or ())
            if commit:
                self._conn.commit()
            if fetchone:
                return self._cursor.fetchone()
            if fetchall:
                return self._cursor.fetchall()
            return True
        except Exception as e:
            self._conn.rollback()
            self._logger.error(f"Database error in {self.__class__.__name__}: {e}")
            return None

    @abstractmethod
    def get_details(self, entity_id):
        """Polymorphic method to retrieve details of an entity."""
        pass
