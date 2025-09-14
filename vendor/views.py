from rest_framework import generics, permissions
from .models import VendorApplication
from .serializers import VendorApplicationSerializer
from django.utils.timezone import now

class VendorApplicationCreateView(generics.CreateAPIView):
    serializer_class = VendorApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Admin approves/rejects
class VendorApplicationApproveView(generics.UpdateAPIView):
    queryset = VendorApplication.objects.all()
    serializer_class = VendorApplicationSerializer
    permission_classes = [permissions.IsAdminUser]

    def update(self, request, *args, **kwargs):
        application = self.get_object()
        action = request.data.get("action")

        if action == "approve":
            application.status = "APPROVED"
            application.reviewed_at = now()
            application.save()


            user = application.user
            user.role = user.Role.VENDOR
            user.application_status = user.ApplicationStatus.APPROVED
            user.save()

        elif action == "reject":
            application.status = "REJECTED"
            application.reviewed_at = now()
            application.save()
        else:
            return Response({"error": "Invalid action"}, status=400)

        return Response({"message": f"Application {application.status}"})
