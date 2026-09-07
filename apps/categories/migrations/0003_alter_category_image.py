from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_category_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to='categories/'),
        ),
    ]
