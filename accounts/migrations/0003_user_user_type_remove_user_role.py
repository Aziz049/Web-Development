# Generated manually to fix user_type migration
from django.db import migrations, models


def migrate_role_to_user_type(apps, schema_editor):
    """Migrate data from role field to user_type field"""
    User = apps.get_model('accounts', 'User')
    for user in User.objects.all():
        # Map old role values to new user_type values
        if hasattr(user, 'role'):
            if user.role == 'PATIENT':
                user.user_type = 'PATIENT'
            elif user.role in ['DOCTOR', 'ADMIN']:
                user.user_type = 'STAFF'
            else:
                user.user_type = 'PATIENT'  # Default
            user.save(update_fields=['user_type'])


def reverse_migrate_user_type_to_role(apps, schema_editor):
    """Reverse migration - map user_type back to role"""
    User = apps.get_model('accounts', 'User')
    for user in User.objects.all():
        if hasattr(user, 'user_type'):
            if user.user_type == 'PATIENT':
                user.role = 'PATIENT'
            elif user.user_type == 'STAFF':
                user.role = 'DOCTOR'  # Default staff to DOCTOR
            user.save(update_fields=['role'])


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_branch_doctorprofile_branch_doctorschedule'),
    ]

    operations = [
        # Add user_type field first (nullable temporarily for data migration)
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(
                choices=[('PATIENT', 'Patient'), ('STAFF', 'Staff')],
                default='PATIENT',
                max_length=10,
                null=True,  # Allow null temporarily
                blank=True
            ),
        ),
        # Migrate data from role to user_type
        migrations.RunPython(migrate_role_to_user_type, reverse_migrate_user_type_to_role),
        # Make user_type non-nullable
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(
                choices=[('PATIENT', 'Patient'), ('STAFF', 'Staff')],
                default='PATIENT',
                max_length=10
            ),
        ),
        # Remove old role field
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
    ]

