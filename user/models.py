from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('이메일은 필수 입력사항입니다.')
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # python manage.py createsuperuser 사용 시 해당 함수 사용
    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField("이메일", max_length=50, unique=True)
    nickname = models.CharField("닉네임", max_length=10, unique=True)
    password = models.CharField("비밀번호", max_length=256)
    profile_image = models.ImageField("프로필 이미지", default="../static/default_profile.jpg", upload_to='profile/')
    join_date = models.DateTimeField("가입일", auto_now_add=True)
    
    # 활성화 여부
    is_active = models.BooleanField("계정 활성화 여부", default=True)
    
    # 작가 여부
    is_author = models.BooleanField("작가 여부", default=False)

    # 관리자 권한 여부
    is_admin = models.BooleanField("관리자 권한", default=False)

    class Meta:
        db_table = "users"

    # 실제 로그인에 사용되는 아이디
    USERNAME_FIELD = 'email'

    # admin 계정을 만들 때 입력받을 정보 ex) email
    REQUIRED_FIELDS = []

    # custom user 생성 시 필요
    objects = UserManager()

    # 어드민 페이지에서 데이터를 제목을 어떻게 붙여줄 것인지 지정
    def __str__(self):
        return f"[유저] pk: {self.id} / 이메일: {self.email} / 닉네임: {self.nickname}"

    # 로그인 사용자의 특정 테이블의 crud 권한을 설정, perm table의 crud 권한이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
