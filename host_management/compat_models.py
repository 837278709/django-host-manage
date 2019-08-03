from django.db import models


class User(models.Model):
    id = models.CharField(max_length=36, primary_key=True, db_column="userID")
    name = models.CharField(max_length=45, db_column="userName")

    class Meta:
        db_table = "system_user"
