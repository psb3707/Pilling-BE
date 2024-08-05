from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class PillingUserManager(BaseUserManager):
    def create_user(self, kakao_sub, nickname, picture, password=None):
        if not kakao_sub:
            raise ValueError('User must have a kakao_sub')
        
        user = self.model(
            kakao_sub=kakao_sub,
        )
        user.nickname = nickname
        user.set_password(password)
        user.picture = picture
        user.save()
        return user
    
    def create_superuser(self, kakao_sub, nickname, picture, password=None):
        if not kakao_sub:
            raise ValueError('User must have a kakao_sub')
        
        user = self.model(
            kakao_sub=kakao_sub,
        )
        user.is_admin = True
        user.nickname = nickname
        user.set_password(password)
        user.picture = picture
        user.save()
        return user

class PillingUser(AbstractBaseUser):
    kakao_sub = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    nickname = models.CharField(max_length=10)
    picture = models.CharField(max_length=200, default='')

    objects = PillingUserManager()

    USERNAME_FIELD = 'kakao_sub'
    REQUIRED_FIELDS = ['nickname']

    @property
    def is_staff(self):
        return self.is_admin