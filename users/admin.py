from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.mail import send_mail

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        "username", "email", "role", "application_role", "application_status",
        "is_staff", "is_active", "is_verified"
    )
    list_filter = ("role", "application_status", "is_staff", "is_active", "is_verified")
    fieldsets = (
        (None, {
            "fields": (
                "email", "username", "password", "phone", "country",
                "role", "application_role", "application_status", "is_verified"
            )
        }),
        ("Permissions", {
            "fields": (
                "is_staff", "is_active", "is_superuser", "groups", "user_permissions"
            )
        }),
    )
    add_fieldsets = (
        (None, {
            "fields": (
                "email", "username", "password1", "password2", "phone",
                "role", "is_verified", "is_staff", "is_active"
            )
        }),
    )
    search_fields = ("email", "username", "phone")
    ordering = ("email",)


    actions = ["approve_upgrade", "reject_upgrade"]


    def approve_upgrade(self, request, queryset):
        for user in queryset:
            if user.application_status == User.ApplicationStatus.PENDING:
                user.role = user.application_role
                user.application_status = User.ApplicationStatus.APPROVED
                user.save()

                dashboard_url = f"{settings.FRONTEND_URL}/dashboard?access={access}&refresh={refresh}"
                send_mail(
                    subject="Untied nations of hair Your Upgrade Request is Approved ",
                    message=f"""
                Hello {user.username},

                Congratulations! Your request to upgrade to {user.role} has been approved.  
                You can now log in to your upgraded dashboard here: {dashboard_url}

                Thank you,
                United Nations of Haire Team
                """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=True,
                )
        self.message_user(request, "Selected users have been approved for upgrade.")

    approve_upgrade.short_description = "Approve selected upgrade requests"

    def reject_upgrade(self, request, queryset):
        queryset.filter(application_status=User.ApplicationStatus.PENDING)\
                .update(application_status=User.ApplicationStatus.REJECTED)
        self.message_user(request, "Selected users have been rejected.")

    reject_upgrade.short_description = "Reject selected upgrade requests"
