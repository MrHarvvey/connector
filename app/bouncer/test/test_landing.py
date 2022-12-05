from google.cloud import ndb

from django.urls import reverse

from bouncer.test.base import DatastoreTestCase
from bouncer.models import Redirect

URL_LANDING = reverse('bouncer:landing')


class LandingPageTests(DatastoreTestCase):

    def test_list_redirect_links(self):
        with self.ds_client.context():
            r1 = Redirect(
                name='Example 1',
                key=ndb.Key(Redirect, 'example-one'),
                destination_url='https://example1.com/r1'
            )
            r1.put()
            r2 = Redirect(
                name='Example 2',
                key=ndb.Key(Redirect, 'example-two'),
                destination_url='https://example1.com/r2'
            )
            r2.put()

        res = self.client.get(URL_LANDING)

        self.assertEqual(res.status_code, 200)

        for r in [r1, r2]:
            url = reverse('bouncer:redirect', kwargs={'slug': r.key.id()})
            self.assertContains(res, url)
            self.assertContains(res, r.name)
