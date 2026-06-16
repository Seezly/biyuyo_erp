from django.db.models import Q
from rest_framework.exceptions import PermissionDenied


class BusinessFilterMixin:
    """
    Mixin that provides business-level filtering based on impersonation state.

    - Admin/superadmin NOT impersonating: returns None (show all data)
    - Admin/superadmin impersonating: returns the impersonated business
    - Regular user: returns their own business
    """

    def get_business_filter(self):
        if self.request.impersonated:
            return self.request.business
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='admin').exists():
            return None
        return self.request.business

    def get_required_business(self):
        business = self.request.business
        if not business:
            raise PermissionDenied("Debe seleccionar un negocio primero.")
        return business


class FilteringMixin:
    """
    Reusable mixin that adds filtering, search, and ordering capabilities to ViewSets.

    Usage:
        class ProductViewSet(FilteringMixin, viewsets.ModelViewSet):
            queryset = Product.objects.all()
            serializer_class = ProductSerializer
            search_fields = ['name', 'sku', 'description']
            filter_fields = ['category_id', 'status']
            ordering_fields = ['created_at', 'name', 'stock']
            default_ordering = ['-created_at']

            def get_queryset(self):
                return self.filter_queryset(
                    super().get_queryset().filter(business_id=self.request.user.business_id)
                )
    """

    search_fields = []
    filter_fields = []
    ordering_fields = []
    default_ordering = ['-created_at']

    def filter_queryset_with_params(self, queryset):
        """
        Apply search, filters, and ordering to the given queryset.
        Call this from the ViewSet's get_queryset method.
        """
        user = self.request.user

        # 1. SEARCH - Text search across multiple fields
        search = self.request.query_params.get('search')
        if search and self.search_fields:
            query = Q()
            for field in self.search_fields:
                # Support nested fields with __ (e.g., customer__name)
                query |= Q(**{f'{field}__icontains': search})
            queryset = queryset.filter(query)

        # 2. FILTERS - Specific field filters
        for field in self.filter_fields:
            value = self.request.query_params.get(field)
            if value is not None and value != '':
                queryset = queryset.filter(**{field: value})

        # 3. ORDERING - Sort by specified field
        ordering = self.request.query_params.get('ordering')
        if ordering:
            # Support descending order with prefix (e.g., -created_at)
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by(*self.default_ordering)

        return queryset