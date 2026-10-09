from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, List

class ParticipantIn(BaseModel):
    name: str
    email: Optional[str] = None

class TranscriptIn(BaseModel):
    speaker: str
    start_time: float = Field(ge=0)
    end_time: float = Field(ge=0)
    text: str

class ActionItemIn(BaseModel):
    title: str
    description: str = ""
    assignee: str = ""
    completed: bool = False

class SummaryIn(BaseModel):
    overview: str
    key_topics: List[str] = []
    outline: List[str] = []

class MeetingCreate(BaseModel):
    title: str
    date: Optional[datetime] = None
    duration: int = 0
    participants: List[ParticipantIn] = []
    transcript: List[TranscriptIn] = []
    summary: Optional[SummaryIn] = None
    action_items: List[ActionItemIn] = []

class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    date: Optional[datetime] = None
    duration: Optional[int] = None
    participants: Optional[List[ParticipantIn]] = None

class ParticipantOut(ParticipantIn):
    model_config = ConfigDict(from_attributes=True)
    id: int

class TranscriptOut(TranscriptIn):
    model_config = ConfigDict(from_attributes=True)
    id: int

class SummaryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    overview: str
    key_topics: List[str] = []
    outline: List[str] = []

    @field_validator("key_topics", "outline", mode="before")
    @classmethod
    def split_lines(cls, value):
        if isinstance(value, str):
            return [x.strip() for x in value.split("\n") if x.strip()]
        return value

class ActionItemOut(ActionItemIn):
    model_config = ConfigDict(from_attributes=True)
    id: int

class MeetingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    date: datetime
    duration: int
    created_at: datetime
    updated_at: datetime
    participants: List[ParticipantOut] = []
    transcript: List[TranscriptOut] = []
    summary: Optional[SummaryOut] = None
    action_items: List[ActionItemOut] = []
