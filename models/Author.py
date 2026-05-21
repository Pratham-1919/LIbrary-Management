from database.database import BaseManager
from database.deconnection import session
from database.author import Author
from logger import  logger



class Authormanager(BaseManager):
    def add_author(self,author_name):
        with session as Session:    
            try: 
                """To add the author name in a new book set"""

                author = Author(name = author_name)
                Session.add(author)
                Session.commit()
                logger.info("Author added successfully: ")
                return author.author_id
            except Exception as e:
                Session.rollback()
                logger.error("Failed to add author: ")
                return
            
        
    def search_author(self, author_name):
        """
        Checks if the author exists. 
        Returns the author object if found, otherwise None.
        """
        with session as Session:
            return Session.query(Author).filter(Author.name.ilike(author_name)).first()
        
    def get_all_authors(self):
        """Returns a list of all authors for the librarian to see."""
        author = session.query(Author).all()
        for row in author:
            return row.name

    def get_details(self, author_id):
        """Polymorphic method implementation for author."""
        author = session.query(Author).get(author_id)
        return author
