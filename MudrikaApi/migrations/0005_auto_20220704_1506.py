# Generated by Django 3.2.5 on 2022-07-04 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MudrikaApi', '0004_rename_accesslevelkeydummy_accessleveltokendummy'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfileSignUpData',
            fields=[
                ('acc_address', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('username', models.CharField(max_length=24)),
                ('access_level_token', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.RenameModel(
            old_name='AccessLevelTokenDummy',
            new_name='AccessLevelTokenData',
        ),
        migrations.DeleteModel(
            name='UserProfileDummy',
        ),
    ]
