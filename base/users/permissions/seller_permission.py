from .is_authenticated_permission import IsAuthenticatedPermission


class SellerPermission(IsAuthenticatedPermission):
    def has_permission(self, request, view):
        permitted = super().has_permission(request=request, view=view)
        if not permitted:
            return False

        if not request.user.is_seller:
            return False

        return True
