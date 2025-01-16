from unittest import TestCase
from contentful.resource_builder import ResourceBuilder
from contentful.sync_page import SyncPage


class ResourceBuilderTest(TestCase):
    def test__when_build_recieves_a_sync_page__returns_a_SyncPage(self):
        sync_api_responses = [
            {
                "sys": {
                    "type": "Array"
                },
                "items": [],
                "nextSyncUrl": (
                    "https://cdn.contentful.com/spaces/cfexampleapi/environments/master/sync?"
                    "sync_token=w5ZGw6JFwqZmVcKsE8Kow4grw45QdybCnV_Cg8OASMKpwo1UY8K8bsKFwqJrw7DDhcKnM2RDOVbDt1E-"
                    "wo7CnDjChMKKGsK1w5zCrA3CnU7CgEvDtsK6w7B2wrRZwrwPIgDCjVo8PMOoUcK2wqTCl8O1wpY8wpjCkGM"
                )
            },
            {
                "sys": {
                    "type": "Array"
                },
                "items": [],
                "nextPageUrl": (
                    "https://cdn.contentful.com/spaces/cfexampleapi/environments/master/sync?"
                    "sync_token=w5ZGw6JFwqZmVcKsE8Kow4grw45QdybCnV_Cg8OASMKpwo1UY8K8bsKFwqJrw7DDhcKnM2RDOVbDt1E-"
                    "wo7CnDjChMKKGsK1w5zCrA3CnU7CgEvDtsK6w7B2wrRZwrwPIgDCjVo8PMOoUcK2wqTCl8O1wpY8wpjCkGM"
                )
            }
        ]

        for response in sync_api_responses:
            resource_builder = ResourceBuilder(
                'en-GB',
                True,
                response
            )

            result = resource_builder.build()
            self.assertTrue(isinstance(result, SyncPage))
