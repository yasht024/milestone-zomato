from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class RecommendationRequest(BaseModel):
    location: str = Field(..., description="The city or location to search for restaurants.")
    budget: str = Field(..., description="The budget tier: Low, Mid, or High.")
    cuisine: Optional[str] = Field(None, description="Preferred cuisine (e.g., North Indian, Chinese).")
    min_rating: Optional[float] = Field(None, description="Minimum acceptable rating (e.g., 4.0).")
    soft_preferences: Optional[str] = Field(None, description="Textual description of user's soft preferences.")

class RestaurantResponse(BaseModel):
    id: int
    name: str
    location: str
    budget_tier: str
    rating: Optional[float]
    cost_for_two: Optional[int]
    cuisines: str
    features: str

    model_config = ConfigDict(from_attributes=True)

class AIRecommendationResponse(RestaurantResponse):
    explanation: str = Field(..., description="AI generated explanation for why this restaurant is a good fit.")
