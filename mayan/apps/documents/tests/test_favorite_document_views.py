from ..models import FavoriteDocument
from ..permissions import permission_document_view

from .base import GenericDocumentViewTestCase
from .mixins.favorite_document_mixins import (
    FavoriteDocumentTestMixin, FavoriteDocumentsViewTestMixin
)


class FavoriteDocumentsTestCase(
    FavoriteDocumentTestMixin, FavoriteDocumentsViewTestMixin,
    GenericDocumentViewTestCase
):
    def test_document_add_to_favorites_view_no_permission(self):
        response = self._request_test_document_favorites_add_view()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(FavoriteDocument.objects.count(), 0)

    def test_document_add_to_favorites_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        response = self._request_test_document_favorites_add_view()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(FavoriteDocument.objects.count(), 1)

    def test_document_list_favorites_view_no_permission(self):
        self._document_add_to_favorites()
        response = self._request_test_document_favorites_list_view()
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )

    def test_document_list_favorites_view_with_access(self):
        self._document_add_to_favorites()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        response = self._request_test_document_favorites_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )

    def test_document_remove_from_favorites_view_no_permission(self):
        self._document_add_to_favorites()
        response = self._request_test_document_favorites_remove_view()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(FavoriteDocument.objects.count(), 1)

    def test_document_remove_from_favorites_view_with_access(self):
        self._document_add_to_favorites()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        response = self._request_test_document_favorites_remove_view()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(FavoriteDocument.objects.count(), 0)
