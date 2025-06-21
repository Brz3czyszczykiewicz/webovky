from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0013_customer_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tripimage',
            name='relation',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='trip_images',
                to='webapp.trip',
            ),
        ),
        migrations.DeleteModel(
            name='CustomerAdmin',
        ),
        migrations.DeleteModel(
            name='TripDetail',
        ),
    ]
