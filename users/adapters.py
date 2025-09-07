from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    - Ensures a username is present (generate one if not supplied).
    - Sets is_verified True if provider marks email as verified.
    - Leaves role as default CUSTOMER (your model logic).
    """

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        if not user.username:
            base = (data.get("name") or data.get("email") or "user").split("@")[0]
            base = base.replace(" ", "").lower()
            user.username = base[:30]
        return user

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)


        try:
            email_addresses = sociallogin.account.extra_data
            email_verified = bool(email_addresses.get("email_verified") or email_addresses.get("verified_email"))
            if email_verified and not user.is_verified:
                user.is_verified = True
                user.save(update_fields=["is_verified"])
        except Exception:
            pass

        return user
