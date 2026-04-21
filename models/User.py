from database.database import BaseManager
from datetime import datetime,timedelta


class Managemember(BaseManager):
    def add_member(self, name, email, phone, duration_time = 365):
        """Add a new user in the system"""
        valid_date = datetime.now() + timedelta(days=duration_time)
        query = """
            INSERT INTO member (name, email, phone, valid_date,status)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING member_id;

        """
        result = self._execute_query(query, (name, email, phone, valid_date, True), fetchone=True, commit=True)
        if result:
            self._logger.info(f"Member added successfully with ID: {result[0]}")
            return result[0]
        return None

    def member_details(self, member_id):
        """Retrives the details of the member"""
        return self.get_details(member_id)
        
    def get_details(self, member_id):
        """Polymorphic method implementation for member."""
        query = "SELECT * FROM member WHERE member_id = %s"
        return self._execute_query(query, (member_id,), fetchone=True)

    def deactivate_member(self, member_id):
        """To deactivate a account of the user"""
        query = "UPDATE member SET status = False WHERE member_id = %s"
        return self._execute_query(query, (member_id,), commit=True) is not None
        
    def get_user_due_date(self,user_id):
        """Get the user due date"""
        query = "SELECT valid_date FROM member WHERE member_id = %s"
        result = self._execute_query(query, (user_id,), fetchone=True)
        return result[0] if result else None