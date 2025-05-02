
from abc import ABC, abstractmethod

from domain.model.member.member import Member


class IMemberRepository(ABC):
    @abstractmethod
    def get_by_id(self, member_id: int) -> Member: ...

    @abstractmethod
    def save_member(self,member : Member) -> None : ...