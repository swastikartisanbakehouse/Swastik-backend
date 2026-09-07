from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to='products/'),
        ),
    ]
