from core.models import User


def show_user_info(username, message):
    user = User.objects.get(username=username)
    print("Showing user info", message, user.username, user.is_superuser)


def show_test_info(message):
    print("***", message)
