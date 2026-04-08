from django.db import migrations, models
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_doctor_news_serviceprice'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, related_name='appointments', to=settings.AUTH_USER_MODEL, verbose_name='Người dùng'),
        ),
    ]
