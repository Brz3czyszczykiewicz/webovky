def is_member_of_group(user, group_name):
    #user instance + str [name1, 2 ...]
    if isinstance(group_name, str):
        rights_exist = user.groups.filter(name=group_name).exists()
    else:
        rights_exist = user.groups.filter(name__in=group_name).exists()
    return rights_exist

class UserRightsMixin:
    access_rights = [] #group names, requirements set in view

    def user_has_rights(self, user):
        return is_member_of_group(user, self.access_rights)

    def get_context_rights(self):
        """
        create dict user_has_rights -> context
        """
        context = {
            'user_has_rights': self.user_has_rights(self.request.user),
        }
        return context