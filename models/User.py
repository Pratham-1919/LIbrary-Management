from database.database import BaseManager
from database.member import Member
from datetime import datetime,timedelta
from logger import logger


class Managemember(BaseManager):
    def add_member(self, name, email, phone, duration_time = 365):
        """Add a new user in the system"""
        valid_date = datetime.now() + timedelta(days=duration_time)
        try:
            new_member = Member(
                name=name,
                email=email,
                phone=phone,
                valid_date=valid_date,
                status=True
            )
            self.db.add(new_member)
            self.db.commit()
            logger.info(f"Member added successfully with ID: {new_member.member_id}")
            return new_member.member_id
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to add member: {e}")
            return None

    def member_details(self, member_id):
        """Retrives the details of the member"""
        return self.get_details(member_id)
        
    def get_details(self, member_id):
        """Polymorphic method implementation for member."""
        return self.db.query(Member).get(member_id)

    def deactivate_member(self, member_id):
        """To deactivate a account of the user"""
        try:
            member = self.db.query(Member).get(member_id)
            if member:
                member.status = False
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to deactivate member: {e}")
            return False
        
    def get_user_due_date(self,user_id):
        """Get the user due date"""
        member = self.db.query(Member).get(user_id)
        return member.valid_date if member else None
    
    def get_all_members(self):
        """Get the details of all members"""
        return self.db.query(Member).all()