# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderinfo',
            old_name='odata',
            new_name='odate',
        ),
    ]
