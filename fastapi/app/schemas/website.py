from pydantic import BaseModel

class Create_Brochure_Request(BaseModel):
    url:str
    company_name:str