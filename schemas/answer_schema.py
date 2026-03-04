from pydantic import BaseModel, Field

class AnswerSchema(BaseModel):
    answer: str = Field(description="Final answer to the user")
    source: str = Field(description="Document source used")
    confidence: float = Field(description="Confidence score between 0 and 1")