import datetime
from dateutil.tz import tzutc
from unittest import TestCase
from contentful.deleted_entry import DeletedEntry


class DeletedEntryTest(TestCase):
    def test_deleted_entry(self):
        deleted_entry = DeletedEntry({
            "sys": {
                "space": {
                    "sys": {
                        "type": "Link",
                        "linkType": "Space",
                        "id": "cfexampleapi"
                        }
                    },
                "id": "5c6VY0gWg0gwaIeYkUUiqG",
                "type": "DeletedEntry",
                "createdAt": "2013-09-09T16:17:12.600Z",
                "updatedAt": "2013-09-09T16:17:12.600Z",
                "deletedAt": "2013-09-09T16:17:12.600Z",
                "revision": 1
            }
        })

        self.assertEqual(deleted_entry.id, '5c6VY0gWg0gwaIeYkUUiqG')
        self.assertEqual(deleted_entry.deleted_at, datetime.datetime(2013, 9, 9, 16, 17, 12, 600000, tzinfo=tzutc()))
        self.assertEqual(str(deleted_entry), "<DeletedEntry id='5c6VY0gWg0gwaIeYkUUiqG'>")
