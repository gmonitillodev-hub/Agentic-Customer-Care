from pydantic import BaseModel, Field
from utils.functions import _merge_models

class AddressInfo(BaseModel):
    city: str | None = None
    postal_code: str | None = None
    region: str | None = None
    street: str | None = None

class UserInfo(BaseModel):
    name: str | None = None
    surname: str | None = None
    email: str | None = None
    address_info: AddressInfo | None = None

class OrderData(BaseModel):
    additional_info: str
    issues_to_be_solved:list[str]
    issues_resolved:list[str]
    request_status: str    

class SessionEntityData(BaseModel):
    user_info: UserInfo | None = None
    order_data: dict[str, OrderData] | None = Field(description="Dict with orderId -> OrderData that keep track of already known info", default=None)
    
class SessionEntity(BaseModel):
    sessionId: str
    data: SessionEntityData = Field(default_factory=SessionEntityData)

    def merge_data(self, new_data: SessionEntityData) -> None:
        """Deep-merge new_data into self.data; None values never overwrite existing ones."""
        self.data = _merge_models(self.data, new_data)
