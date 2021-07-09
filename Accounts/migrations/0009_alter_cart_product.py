# Generated by Django 3.2 on 2021-05-05 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0005_alter_product_category'),
        ('Accounts', '0008_remove_cart_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.product', unique=True),
        ),
    ]