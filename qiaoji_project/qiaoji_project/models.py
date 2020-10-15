# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models







class CompanyLevel(models.Model):
    company = models.CharField(max_length=50, blank=True, null=True)
    company_level = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_level'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TestInformation(models.Model):
    order_name = models.CharField(unique=True, max_length=50)
    test_name = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    number = models.IntegerField()
    code = models.CharField(max_length=200)
    customer_name = models.CharField(max_length=50)
    tester_name = models.CharField(max_length=50)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    state = models.CharField(max_length=20)
    note = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test_information'


class UserTable(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=36, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    company = models.CharField(max_length=50, blank=True, null=True)
    account_level = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_table'

