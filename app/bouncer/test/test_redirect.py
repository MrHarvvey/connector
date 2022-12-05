from google.cloud import ndb

from django.urls import reverse

from bouncer.test.base import DatastoreTestCase

from bouncer.models import Redirect


class RedirectTests(DatastoreTestCase):
    def test_not_found(self):
        url = reverse('bouncer:redirect', kwargs={'slug': 'notfound'})
        res = self.client.get(url, fallow=False)

        self.assertEqual(res.status_code, 404)

    def test_success(self):
        with self.ds_client.context():
            redirect = Redirect(
                key=ndb.Key(Redirect, 'example'),
                destination_url='https://example.com',
            )
            redirect.put()

        url = reverse('bouncer:redirect', kwargs={'slug': redirect.key.id()})
        res = self.client.get(url, fallow=False)

        self.assertRedirects(
            res,
            redirect.destination_url,
            fetch_redirect_response=False,
            status_code=301,
        )
