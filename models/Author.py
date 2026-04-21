from database.database import BaseManager


class Authormanager(BaseManager):
    def add_author(self,name):
        """To add the author name in a new book set"""

        query = """
                    INSERT INTO author (name) VALUES (%s) RETURNING author_id;
                """
        
        result = self._execute_query(query, (name,), fetchone=True, commit=True)
        if result:
            self._logger.info(f"Author '{name}' added successfully with ID: {result[0]}")
            return result[0]
        return None
        
    def search_author(self, name):
        """
        Checks if the author exists. 
        Returns the (author_id,) tuple if found, otherwise None.
        """
        query = "SELECT author_id FROM author WHERE name = %s;"
        return self._execute_query(query, (name,), fetchone=True)
        
    def get_all_authors(self):
        """Returns a list of all authors for the librarian to see."""
        query = "SELECT * FROM author ORDER BY name ASC;"
        return self._execute_query(query, fetchall=True)

    def get_details(self, author_id):
        """Polymorphic method implementation for author."""
        query = "SELECT * FROM author WHERE author_id = %s;"
        return self._execute_query(query, (author_id,), fetchone=True)
