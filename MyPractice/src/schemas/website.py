from pydantic import BaseModel

class WebsiteSummarizeRequest(BaseModel):
    url: str
    tone: str = "concise and professional"

# New: Request body for the full brochure generator
class BrochureRequest(BaseModel):
    company_name: str
    url: str
