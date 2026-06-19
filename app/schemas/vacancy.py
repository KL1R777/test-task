from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class VacancyBase(BaseModel):
    title: str
    timetable_mode_name: str
    tag_name: str
    city_name: Optional[str] = None
    published_at: datetime
    is_remote_available: bool
    is_hot: bool
    external_id: Optional[int] = None


class VacancyCreate(VacancyBase):
    pass


class VacancyUpdate(BaseModel): 
    title: Optional[str] = None
    timetable_mode_name: Optional[str] = None
    tag_name: Optional[str] = None
    city_name: Optional[str] = None
    published_at: Optional[datetime] = None
    is_remote_available: Optional[bool] = None
    is_hot: Optional[bool] = None
    external_id: Optional[int] = None


class VacancyRead(VacancyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
