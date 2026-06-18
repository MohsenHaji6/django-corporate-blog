from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def create_user(self, phone_number, password=None, **extra_fields):  # pyright: ignore[reportIncompatibleMethodOverride]
        if not phone_number:
            raise ValueError("The given phone number must be set")

        if not isinstance(phone_number, str):
            raise ValueError("Phone number must be a string.")
        phone_number = phone_number.strip()

        user = self.model(phone_number=phone_number, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, password, **extra_fields):  # pyright: ignore[reportIncompatibleMethodOverride]
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        if not password:
            raise ValueError("Superusers must have a password.")

        return self.create_user(phone_number, password, **extra_fields)
