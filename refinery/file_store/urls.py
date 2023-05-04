from django.conf.urls import url

from constants import UUID_RE
from file_store.views import FileStoreItemAPIView

file_store_api_urls = [
    url(
        f'^file_store_items/(?P<uuid>{UUID_RE})/$',
        FileStoreItemAPIView.as_view(),
    )
]
