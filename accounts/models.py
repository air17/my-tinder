import os.path
from PIL import Image
from django.contrib.auth.hashers import make_password, identify_hasher
from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from model_utils.models import UUIDModel
from myTinder import settings


class CustomUserManager(UserManager):
    """Custom model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, UUIDModel):
    username = None
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    sex = models.CharField(max_length=1, choices=(('F', 'Female'),
                                                  ('M', 'Male'),
                                                  ))
    picture = models.ImageField(blank=True, upload_to="photos/")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.get_full_name()

    def get_avatar_url(self) -> str:
        if self.picture:
            url = self.picture.url
        else:
            url = settings.MEDIA_URL + "user.png"
        return url

    def save(self, *args, **kwargs):
        # hashing password when it is not hashed
        try:
            identify_hasher(self.password)
        except ValueError:
            self.password = make_password(self.password)

        super(User, self).save(*args, **kwargs)

        # editing picture
        try:
            picture_path = self.picture.path
            self.add_watermark(picture_path)
        except Exception as e:
            print(f"Error adding watermark: {e}")

    @staticmethod
    def add_watermark(path):
        img = Image.open(path)
        watermark = Image.open(os.path.join("accounts", "watermark.webp"))
        img.paste(watermark, (img.width-260, img.height-260), mask=watermark)
        img.save(path)
