import json
from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin
from audit.models import AuditLog

User = get_user_model()


class AuditMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Store the original request data for comparison in process_response
        if request.method in ["POST", "PUT", "PATCH"]:
            request._audit_data = {
                "method": request.method,
                "path": request.path,
                "data": request.POST.dict() if hasattr(request, "POST") else {},
                "user": (
                    getattr(request, "user", None)
                    if request.user.is_authenticated
                    else None
                ),
            }
        return None

    def process_response(self, request, response):
        # Skip logging for non-API requests or certain paths
        if not request.path.startswith("/api/"):
            return response

        # Skip logging for auth endpoints to avoid too much noise
        if "/api/auth/" in request.path or "/api/token/" in request.path:
            return response

        # Only log successful requests (2xx status codes)
        if not (200 <= response.status_code < 300):
            return response

        # Get audit data from request
        audit_data = getattr(request, "_audit_data", None)
        if not audit_data:
            return response

        user = audit_data["user"]
        method = audit_data["method"]
        path = audit_data["path"]

        # Determine action based on HTTP method
        action_map = {
            "POST": "create",
            "PUT": "update",
            "PATCH": "update",
            "DELETE": "delete",
        }
        action = action_map.get(method, "other")

        # Skip if no user or action not in our map
        if not user or action not in ["create", "update", "delete"]:
            return response

        # Extract model and object info from path
        # Path format: /api/{app}/{model}/{id}/ or /api/{app}/{model}/
        path_parts = path.strip("/").split("/")
        if len(path_parts) >= 3 and path_parts[0] == "api":
            app_name = path_parts[1]
            model_name = path_parts[2] if len(path_parts) > 2 else None
            object_id = (
                path_parts[3]
                if len(path_parts) > 3 and path_parts[3].isdigit()
                else None
            )

            # Create audit log entry
            try:
                AuditLog.objects.create(
                    user=user,
                    action=action,
                    model_name=f"{app_name}.{model_name}" if model_name else app_name,
                    object_id=str(object_id) if object_id else None,
                    description=f"{action.capitalize()} operation on {model_name}",
                    ip_address=self.get_client_ip(request),
                    user_agent=request.META.get("HTTP_USER_AGENT", "")[
                        :255
                    ],  # Limit length
                )
            except Exception:
                # Don't let audit logging errors break the application
                pass

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
