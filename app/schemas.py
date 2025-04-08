from pydantic import BaseModel

class PromoInput(BaseModel):
    store_count: int
    shelf_capacity: float
    promo_shelf_capacity: int
    is_promo: bool
    item_number: str
    category_code: str
    group_code: str
    month: str
    weekday: str
    unit_sales_7: float
    unit_sales_14: float
    unit_sales_21: float

# class PromoPrediction(BaseModel):
#     unit_sales:  float 