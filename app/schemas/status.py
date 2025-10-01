from pydantic import BaseModel


class AppStatus(BaseModel):
    """
    Pydantic model for the application status response.
    """

    status: str
    name: str
    version: str
