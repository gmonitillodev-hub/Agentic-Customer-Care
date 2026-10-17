from pydantic import BaseModel, Field
from utils.functions import _merge_models

class AddressInfo(BaseModel):
    city: str | None = None
    postal_code: str | None = None
    region: str | None = None

class UserInfo(BaseModel):
    name: str | None = None
    surname: str | None = None
    email: str | None = None
    address_info: AddressInfo | None = None

class SessionEntityData(BaseModel):
    user_info: UserInfo | None = None
    
class SessionEntity(BaseModel):
    sessionId: str
    data: SessionEntityData = Field(default_factory=SessionEntityData)

    def merge_data(self, new_data: SessionEntityData) -> None:
        """Deep-merge new_data into self.data; None values never overwrite existing ones."""
        self.data = _merge_models(self.data, new_data)
