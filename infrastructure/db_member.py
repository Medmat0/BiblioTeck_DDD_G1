from typing import List, Optional
from domain.repository.member_repository import IMemberRepository
from domain.model.member.member import Member
from  infrastructure.data.static_member import STATIC_MEMBERS

class DbMember(IMemberRepository):
    def __init__(self):
        self.members = STATIC_MEMBERS.copy()
    
    def get_by_id(self, member_id: int) -> Optional[Member]:
        return next((member for member in self.members if member.id.id == member_id), None)
    
    def save_member(self, member: Member) -> None:
        existing_member = self.get_by_id(member.id.id)
        if existing_member:
            index = self.members.index(existing_member)
            self.members[index] = member
        else:
            self.members.append(member)
    
    def get_all_members(self) -> List[Member]:
        return self.members.copy()