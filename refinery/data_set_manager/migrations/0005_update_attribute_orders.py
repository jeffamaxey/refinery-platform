# -*- coding: utf-8 -*-

from django.db import models, migrations

from data_set_manager.search_indexes import NodeIndex


def create_missing_attribute_orders(apps, schema_editor):
    investigation_model = apps.get_model("data_set_manager", "Investigation")
    attribute_order_model = apps.get_model("data_set_manager",
                                           "AttributeOrder")
    attribute_orders_to_create = []
    for investigation in investigation_model.objects.all():
        for study in investigation.study_set.all():
            attribute_orders_to_create.extend(
                attribute_order_model(
                    study=study,
                    assay=assay,
                    solr_field=NodeIndex.DOWNLOAD_URL,
                    rank=0,
                    is_facet=False,
                    is_exposed=True,
                    is_internal=False,
                    is_active=True,
                )
                for assay in study.assay_set.all()
                if attribute_order_model.objects.filter(
                    study=study, assay=assay, solr_field=NodeIndex.DOWNLOAD_URL
                ).count()
                == 0
            )
    attribute_order_model.objects.bulk_create(attribute_orders_to_create)


class Migration(migrations.Migration):
    dependencies = [
        ('data_set_manager', '0004_auto_20171211_1145'),
    ]

    operations = [
        migrations.RunPython(create_missing_attribute_orders, migrations.RunPython.noop),
    ]
