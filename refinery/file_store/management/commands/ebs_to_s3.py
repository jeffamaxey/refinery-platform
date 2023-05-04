import os
import logging

import boto3
import botocore

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from ...models import FileStoreItem
from ...utils import S3MediaStorage, S3_WRITE_ARGS

logging.disable(logging.INFO)  # boto3 logging is verbose at DEBUG level


class Command(BaseCommand):
    help = """Move data files from EBS volume to S3 MEDIA_BUCKET and update
    corresponding FileStoreItem instances"""

    def handle(self, *args, **options):
        storage = S3MediaStorage()
        s3 = boto3.client('s3')
        for item in FileStoreItem.objects.all():
            try:
                file_name = os.path.basename(item.datafile.path)
            except NotImplementedError:
                # make sure SymlinkedFileSystemStorage is the default backend
                raise CommandError(
                    f"No path available for FileStoreItem with UUID '{item.uuid}'.Is default storage backend file based?"
                )
            except ValueError:  # no datafile available
                continue

            # skip files that have already been transferred to S3
            if '/' not in item.datafile.name[:7]:
                self.stdout.write(f"Skipping {item.datafile.name}: already transferred")
                continue

            # transfer the file
            key = storage.get_name(file_name)
            self.stdout.write(
                f"Moving '{item.datafile.path}' to 's3://{settings.MEDIA_BUCKET}/{key}'"
            )
            try:
                s3.upload_file(item.datafile.path, settings.MEDIA_BUCKET, key,
                               ExtraArgs=S3_WRITE_ARGS)
            except (EnvironmentError, botocore.exceptions.BotoCoreError,
                    botocore.exceptions.ClientError) as exc:
                raise CommandError(
                    f"Error uploading from '{item.datafile.path}' to 's3://{settings.MEDIA_BUCKET}/{key}': {exc}"
                )
            try:
                os.unlink(item.datafile.path)
            except EnvironmentError as exc:
                raise CommandError(f"Error deleting '{item.datafile.path}': {exc}")

            item.datafile.name = key
            item.save()
