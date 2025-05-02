from abc import ABC

class Entity(ABC):
    """Base class for DDD Entities (must have an ID)."""
    pass

class ValueObject(ABC):
    """Base class for DDD Value Objects (immutable)."""
    pass