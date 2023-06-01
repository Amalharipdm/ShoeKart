from django.contrib.auth.backends import ModelBackend
from .models import Account

class AccountBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Account.objects.get(email=email)
            if user.check_password(password):
                return user
        except Account.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None
        

# from django.contrib.auth.backends import ModelBackend
# from django.contrib import messages
# from django.http import request

# class BlockedUserModelBackend(ModelBackend):
#     def user_can_authenticate(self, user):
#         if user.is_blocked:
#             # User is blocked, display a message
#             messages.error(request, 'Your account has been blocked by the admin.')
#             return False
#         return super().user_can_authenticate(user)
