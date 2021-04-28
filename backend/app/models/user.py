import string
from typing import Optional

from pydantic import EmailStr, constr, validator

from app.models.core import DateTimeModelMixin, IDModelMixin, CoreModel

# check for valid username
def validate_username(username: str) -> str:
    allowed = string.ascii_letters + string.digits + '-' + '_'
    assert all(char in allowed for char in username), "Invalid characters in username"
    assert len(username) >= 3, "Username must be 3 characters or more"
    
    return username

class UserBase(CoreModel):
    