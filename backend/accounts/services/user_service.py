from django.contrib.auth.models import Group
from accounts.models import CustomUser

def create_user_with_role(validated_data, business, role_name):
    user = CustomUser.objects.create_user(
        **validated_data,
        business_id=business
    )

    group = Group.objects.get(name=role_name)
    user.groups.add(group)

    return user