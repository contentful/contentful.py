import datetime
from dateutil.tz import tzutc
from unittest import TestCase
from contentful.deleted_asset import DeletedAsset


class DeletedAssetTest(TestCase):
    def test_deleted_asset(self):
        deleted_asset = DeletedAsset({
            "sys": {
                "space": {
                    "sys": {
                        "type": "Link",
                        "linkType": "Space",
                        "id": "cfexampleapi"
                        }
                    },
                "id": "5c6VY0gWg0gwaIeYkUUiqG",
                "type": "DeletedAsset",
                "createdAt": "2013-09-09T16:17:12.600Z",
                "updatedAt": "2013-09-09T16:17:12.600Z",
                "deletedAt": "2013-09-09T16:17:12.600Z",
                "revision": 1
            }
        })

        self.assertEqual(deleted_asset.id, '5c6VY0gWg0gwaIeYkUUiqG')
        self.assertEqual(deleted_asset.deleted_at, datetime.datetime(2013, 9, 9, 16, 17, 12, 600000, tzinfo=tzutc()))
        self.assertEqual(str(deleted_asset), "<DeletedAsset id='5c6VY0gWg0gwaIeYkUUiqG'>")
