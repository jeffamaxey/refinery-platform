# -*- coding: utf-8 -*-


from django.db import models, migrations




class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ce10_WormBase',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ('chrom', models.CharField(max_length=255, db_index=True)),
                ('source', models.CharField(max_length=100)),
                ('feature', models.CharField(max_length=100)),
                ('start', models.IntegerField(db_index=True)),
                ('end', models.IntegerField(db_index=True)),
                ('score', models.CharField(max_length=100)),
                ('strand', models.CharField(max_length=1)),
                ('frame', models.CharField(max_length=100)),
                ('attribute', models.TextField()),
                ('cds', models.CharField(max_length=100)),
                ('clone', models.CharField(max_length=100)),
                ('gene', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['chrom', 'start'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChromInfo',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ('chrom', models.CharField(max_length=255, db_index=True)),
                ('size', models.IntegerField()),
                ('fileName', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['-size'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConservationTrack',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ('chrom', models.CharField(max_length=255, db_index=True)),
                ('position', models.IntegerField(db_index=True)),
                ('value', models.FloatField()),
            ],
            options={
                'ordering': ['chrom', 'position'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CytoBand',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ('chrom', models.CharField(max_length=255)),
                ('chromStart', models.IntegerField(db_index=True)),
                ('chromEnd', models.IntegerField(db_index=True)),
                ('name', models.CharField(max_length=255, db_index=True)),
                ('gieStain', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['chrom', 'chromStart'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='dm3_FlyBase',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ('chrom', models.CharField(max_length=255, db_index=True)),
                ('source', models.CharField(max_length=100)),
                ('feature', models.CharField(max_length=100)),
                ('start', models.IntegerField(db_index=True)),
                ('end', models.IntegerField(db_index=True)),
                ('score', models.CharField(max_length=100)),
                ('strand', models.CharField(max_length=1)),
                ('frame', models.CharField(max_length=100)),
                ('attribute', models.TextField()),
                ('name', models.CharField(max_length=100)),
                ('Alias', models.TextField()),
                ('description', models.CharField(max_length=255)),
                ('fullname', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['chrom', 'start'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmpiricalMappability',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ('chrom', models.CharField(max_length=255, db_index=True)),
                ('chromStart', models.IntegerField(db_index=True)),
                ('chromEnd', models.IntegerField(db_index=True)),
                ('name', models.CharField(max_length=255)),
                ('score', models.CharField(max_length=255)),
                ('strand', models.CharField(max_length=1)),
                ('thickStart', models.IntegerField(null=True)),
                ('thickEnd', models.IntegerField(null=True)),
                ('itemRgb', models.CharField(max_length=255)),
                ('blockCount', models.IntegerField(null=True)),
                (
                    'blockSizes',
                    models.CommaSeparatedIntegerField(max_length=3700),
                ),
                (
                    'blockStarts',
                    models.CommaSeparatedIntegerField(max_length=3700),
                ),
            ],
            options={
                'ordering': ['chrom', 'chromStart'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GapRegionFile',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ('bin', models.IntegerField()),
                ('chrom', models.CharField(max_length=255, db_index=True)),
                ('chromStart', models.IntegerField(db_index=True)),
                ('chromEnd', models.IntegerField(db_index=True)),
                ('ix', models.IntegerField(db_index=True)),
                ('n', models.CharField(max_length=255)),
                ('size', models.IntegerField(db_index=True)),
                ('type', models.CharField(max_length=255)),
                ('bridge', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['chrom', 'chromStart'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GCContent',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ('chrom', models.CharField(max_length=255, db_index=True)),
                ('position', models.IntegerField(db_index=True)),
                ('value', models.FloatField()),
            ],
            options={
                'ordering': ['chrom', 'position'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gene',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ('bin', models.IntegerField()),
                ('name', models.CharField(max_length=255, db_index=True)),
                ('chrom', models.CharField(max_length=255, db_index=True)),
                ('strand', models.CharField(max_length=1)),
                ('txStart', models.IntegerField(db_index=True)),
                ('txEnd', models.IntegerField(db_index=True)),
                ('cdsStart', models.IntegerField(db_index=True)),
                ('cdsEnd', models.IntegerField(db_index=True)),
                ('exonCount', models.IntegerField()),
                (
                    'exonStarts',
                    models.CommaSeparatedIntegerField(
                        max_length=3700, db_index=True
                    ),
                ),
                (
                    'exonEnds',
                    models.CommaSeparatedIntegerField(
                        max_length=3700, db_index=True
                    ),
                ),
                ('score', models.IntegerField()),
                ('name2', models.CharField(max_length=255, db_index=True)),
                (
                    'cdsStartStat',
                    models.CharField(max_length=10, db_index=True),
                ),
                ('cdsEndStat', models.CharField(max_length=10, db_index=True)),
                (
                    'exonFrames',
                    models.CommaSeparatedIntegerField(max_length=3700),
                ),
            ],
            options={
                'ordering': ['chrom', 'txStart'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GenomeBuild',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ('name', models.CharField(unique=True, max_length=255)),
                (
                    'affiliation',
                    models.CharField(default=b'UCSC', max_length=255),
                ),
                ('description', models.CharField(max_length=255)),
                (
                    'html_path',
                    models.CharField(max_length=1024, null=True, blank=True),
                ),
                (
                    'source_name',
                    models.CharField(max_length=1024, null=True, blank=True),
                ),
                ('available', models.BooleanField(default=True)),
                ('default_build', models.BooleanField(default=False)),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='hg19_GenCode',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ('chrom', models.CharField(max_length=255, db_index=True)),
                ('source', models.CharField(max_length=100)),
                ('feature', models.CharField(max_length=100)),
                ('start', models.IntegerField(db_index=True)),
                ('end', models.IntegerField(db_index=True)),
                ('score', models.CharField(max_length=100)),
                ('strand', models.CharField(max_length=1)),
                ('frame', models.CharField(max_length=100)),
                ('attribute', models.TextField()),
                ('gene_id', models.CharField(max_length=255, db_index=True)),
                (
                    'transcript_id',
                    models.CharField(max_length=255, db_index=True),
                ),
                ('gene_type', models.CharField(max_length=100, db_index=True)),
                (
                    'gene_status',
                    models.CharField(max_length=100, db_index=True),
                ),
                ('gene_name', models.CharField(max_length=100, db_index=True)),
                (
                    'transcript_type',
                    models.CharField(max_length=100, db_index=True),
                ),
                (
                    'transcript_status',
                    models.CharField(max_length=100, db_index=True),
                ),
                (
                    'transcript_name',
                    models.CharField(max_length=100, db_index=True),
                ),
                (
                    'genomebuild',
                    models.ForeignKey(
                        default=None,
                        to='annotation_server.GenomeBuild',
                        null=True,
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Taxon',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ('taxon_id', models.IntegerField(db_index=True)),
                ('name', models.CharField(max_length=1024)),
                (
                    'unique_name',
                    models.CharField(max_length=1024, null=True, blank=True),
                ),
                ('type', models.CharField(max_length=255, db_index=True)),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TheoreticalMappability',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ('chrom', models.CharField(max_length=255, db_index=True)),
                ('chromStart', models.IntegerField(db_index=True)),
                ('chromEnd', models.IntegerField(db_index=True)),
                ('name', models.CharField(max_length=255)),
                ('score', models.CharField(max_length=255)),
                ('strand', models.CharField(max_length=1)),
                ('thickStart', models.IntegerField(null=True)),
                ('thickEnd', models.IntegerField(null=True)),
                ('itemRgb', models.CharField(max_length=255)),
                ('blockCount', models.IntegerField(null=True)),
                (
                    'blockSizes',
                    models.CommaSeparatedIntegerField(max_length=3700),
                ),
                (
                    'blockStarts',
                    models.CommaSeparatedIntegerField(max_length=3700),
                ),
                (
                    'genomebuild',
                    models.ForeignKey(
                        default=None,
                        to='annotation_server.GenomeBuild',
                        null=True,
                    ),
                ),
            ],
            options={
                'ordering': ['chrom', 'chromStart'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WigDescription',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ('annotation_type', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=1024)),
                ('altColor', models.CharField(max_length=255)),
                ('color', models.CharField(max_length=255)),
                ('visibility', models.CharField(max_length=255)),
                ('priority', models.IntegerField()),
                ('type', models.CharField(max_length=255)),
                ('description', models.TextField()),
                (
                    'genomebuild',
                    models.ForeignKey(
                        default=None,
                        to='annotation_server.GenomeBuild',
                        null=True,
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='taxon', unique_together={('taxon_id', 'name')}
        ),
        migrations.AddField(
            model_name='genomebuild',
            name='species',
            field=models.ForeignKey(to='annotation_server.Taxon'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gene',
            name='genomebuild',
            field=models.ForeignKey(
                default=None, to='annotation_server.GenomeBuild', null=True
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gccontent',
            name='annot',
            field=models.ForeignKey(to='annotation_server.WigDescription'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gccontent',
            name='genomebuild',
            field=models.ForeignKey(
                default=None, to='annotation_server.GenomeBuild', null=True
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gapregionfile',
            name='genomebuild',
            field=models.ForeignKey(
                default=None, to='annotation_server.GenomeBuild', null=True
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='empiricalmappability',
            name='genomebuild',
            field=models.ForeignKey(
                default=None, to='annotation_server.GenomeBuild', null=True
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dm3_flybase',
            name='genomebuild',
            field=models.ForeignKey(
                default=None, to='annotation_server.GenomeBuild', null=True
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cytoband',
            name='genomebuild',
            field=models.ForeignKey(
                default=None, to='annotation_server.GenomeBuild', null=True
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conservationtrack',
            name='annot',
            field=models.ForeignKey(to='annotation_server.WigDescription'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conservationtrack',
            name='genomebuild',
            field=models.ForeignKey(
                default=None, to='annotation_server.GenomeBuild', null=True
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chrominfo',
            name='genomebuild',
            field=models.ForeignKey(
                default=None, to='annotation_server.GenomeBuild', null=True
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ce10_wormbase',
            name='genomebuild',
            field=models.ForeignKey(
                default=None, to='annotation_server.GenomeBuild', null=True
            ),
            preserve_default=True,
        ),
    ]
