
def is_admin(user):
    if user:
        return bool(hasattr(user, "lengths_user") and user.lengths_user.is_admin)


def is_crud_user(user):
    # nested under admin
    if user:
        return is_admin(user) or bool(hasattr(user, "lengths_user") and user.lengths_user.is_crud_user)

