# import uuid
# import base64
from oscar.core.compat import get_user_model
# from django.utils.crypto import random
#
#
# def generate_unique_invite_code(regex=None):
#     User = get_user_model()
#     try:
#         letters = string.ascii_letters
#     except AttributeError:
#         letters = string.letters
#     code = ''.join([random.choice(letters + string.digits + '_')
#                     for i in range(15)])
#     try:
#         User.objects.get(invite_code=code)
#         return generate_unique_invite_code()
#     except User.DoesNotExist:
#         return code
