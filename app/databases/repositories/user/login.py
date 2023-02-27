from app.databases.repositories.base import BaseCrud
from app.databases.models.user.user import User
from app.databases.schemas.users.userschema import ProfileModel


class LoginCrud(BaseCrud):

    def create_profile(self, profile: ProfileModel):

        new_user = User(**profile.dict())