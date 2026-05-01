from pydantic import BaseModel


class StockBase(BaseModel):
    name: str
    quantity: int
    purchase_value: float
    present_value: float


class StockCreate(StockBase):
    pass


class StockResponse(StockBase):
    pass