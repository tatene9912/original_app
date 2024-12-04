from django.db import models
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser,
                                        PermissionsMixin)
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email=email,
            password=password,
            **extra_fields,
        )

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_active'] = True
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(
            email=email,
            password=password,
            **extra_fields,
        )


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
            swappable = 'AUTH_USER_MODEL'
            
    id = models.AutoField(primary_key=True) 
    email = models.EmailField(
        verbose_name=_("メールアドレス"),
        unique=True
    )
    nic_name = models.CharField(
        verbose_name=_("ニックネーム"),
        max_length=150,
        null=True,
        blank=False
    )
    image = CloudinaryField(
        verbose_name='アイコン',
        null=True,
        blank=True,
        default='noImage_hr5mpd'
    )
    name = models.CharField(
        verbose_name=_("氏名"),
        max_length=150,
        null=True,
        blank=False
    )
    profile = models.TextField(
        verbose_name=_("プロフィール"),
        null=True,
        blank=False
    )
    postal_code = models.CharField(
        max_length=7, 
        verbose_name='郵便番号', 
        null=True
    )
    address = models.CharField(
        max_length=50, 
        verbose_name='住所', 
        null=True
    )
    phone_number = models.CharField(
        max_length=11,
        verbose_name='電話番号', 
        null=True
    )
    is_superuser = models.BooleanField(
        verbose_name=_("is_superuser"),
        default=False
    )
    is_staff = models.BooleanField(
        verbose_name=_('staff status'),
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_("作成日時"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("更新日時"),
        auto_now=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email' # ログイン時、ユーザー名の代わりにemailを使用
    REQUIRED_FIELDS = []  # スーパーユーザー作成時に必要なフィールド

    def __str__(self):
        return self.email