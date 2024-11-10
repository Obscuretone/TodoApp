from tortoise import fields, models


class User(models.Model):
    uuid = fields.UUIDField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    display_name = fields.CharField(max_length=255, null=True)
    password = fields.CharField(max_length=255)  # Add the password field

    class Meta:
        table = "users"

    def to_dict(self):
        """
        Convert the User model instance to a dictionary.
        """
        return {
            "uuid": str(self.uuid),  # UUID needs to be converted to string
            "email": self.email,
            "display_name": self.display_name,
        }
