from unittest import TestCase
from contentful.sync_page import SyncPage


class SyncPageTest(TestCase):
    def test_sync_page_deleted_items(self):
        sync_page = SyncPage({
            "sys": {
                "type": "Array"
            },
            "items": [
                {
                    "sys": {
                        "space": {
                            "sys": {
                                "type": "Link",
                                "linkType": "Space",
                                "id": "cfexampleapi"
                            }
                        },
                        "id": "4rPdazIwWkuuKEAQgemSmO",
                        "type": "DeletedEntry",
                        "createdAt": "2014-08-11T08:30:42.546Z",
                        "updatedAt": "2014-08-11T08:30:42.546Z",
                        "deletedAt": "2014-08-11T08:30:42.546Z",
                        "revision": 1
                    }
                },
                {
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
                },
                {
                    "sys": {
                        "space": {
                            "sys": {
                                "type": "Link",
                                "linkType": "Space",
                                "id": "cfexampleapi"
                            }
                        },
                        "id": "finn",
                        "type": "DeletedAsset",
                        "createdAt": "2013-09-02T15:10:33.749Z",
                        "updatedAt": "2013-09-02T15:10:33.749Z",
                        "deletedAt": "2013-09-02T15:10:33.749Z",
                        "revision": 1
                    }
                },
                {
                    "sys": {
                        "space": {
                            "sys": {
                                "type": "Link",
                                "linkType": "Space",
                                "id": "cfexampleapi"
                            }
                        },
                        "id": "3MZPnjZTIskAIIkuuosCss",
                        "type": "DeletedAsset",
                        "createdAt": "2013-09-02T14:55:34.645Z",
                        "updatedAt": "2013-09-02T14:55:34.645Z",
                        "deletedAt": "2013-09-02T14:55:34.645Z",
                        "revision": 1
                    }
                },
                {
                    "sys": {
                        "space": {
                            "sys": {
                                "type": "Link",
                                "linkType": "Space",
                                "id": "cfexampleapi"
                            }
                        },
                        "id": "4gp6taAwW4CmSgumq2ekUm",
                        "type": "DeletedAsset",
                        "createdAt": "2013-09-02T14:55:34.623Z",
                        "updatedAt": "2013-09-02T14:55:34.623Z",
                        "deletedAt": "2013-09-02T14:55:34.623Z",
                        "revision": 2
                    }
                },
                {
                    "sys": {
                        "space": {
                            "sys": {
                                "type": "Link",
                                "linkType": "Space",
                                "id": "cfexampleapi"
                            }
                        },
                        "id": "1uf1qqyZuEuiwmigoUYkeu",
                        "type": "DeletedAsset",
                        "createdAt": "2013-09-02T14:55:34.323Z",
                        "updatedAt": "2013-09-02T14:55:34.323Z",
                        "deletedAt": "2013-09-02T14:55:34.323Z",
                        "revision": 1
                    }
                },
                {
                    "sys": {
                        "space": {
                            "sys": {
                                "type": "Link",
                                "linkType": "Space",
                                "id": "cfexampleapi"
                            }
                        },
                        "id": "4hlteQAXS8iS0YCMU6QMWg",
                        "type": "DeletedAsset",
                        "createdAt": "2013-09-02T14:55:34.282Z",
                        "updatedAt": "2013-09-02T14:55:34.282Z",
                        "deletedAt": "2013-09-02T14:55:34.282Z",
                        "revision": 1
                    }
                },
                {
                    "sys": {
                        "space": {
                            "sys": {
                                "type": "Link",
                                "linkType": "Space",
                                "id": "cfexampleapi"
                            }
                        },
                        "id": "CVebBDcQsSsu6yKKIayy",
                        "type": "DeletedEntry",
                        "createdAt": "2013-06-23T19:06:46.224Z",
                        "updatedAt": "2013-06-23T19:06:46.224Z",
                        "deletedAt": "2016-03-07T15:10:41.286Z",
                        "revision": 1
                    }
                }
            ],
            "nextPageUrl": (
                "https://cdn.contentful.com/spaces/cfexampleapi/environments/master/sync?"
                "sync_token=w5ZGw6JFwqZmVcKsE8Kow4grw45QdybCnV_Cg8OASMKpwo1UY8K8bsKFwqJrw7DDhcKnM2RDOVbDt1E-"
                "wo7CnDjChMKKGsK1w5zCrA3CnU7CgEvDtsK6w7B2wrRZwrwPIgDCjVo8PMOoUcK2wqTCl8O1wpY8wpjCkGM"
            )
        })

        self.assertEqual(
            sync_page.next_page_url,
            "https://cdn.contentful.com/spaces/cfexampleapi/environments/master/sync?"
            "sync_token=w5ZGw6JFwqZmVcKsE8Kow4grw45QdybCnV_Cg8OASMKpwo1UY8K8bsKFwqJrw7DDhcKnM2RDOVbDt1E-"
            "wo7CnDjChMKKGsK1w5zCrA3CnU7CgEvDtsK6w7B2wrRZwrwPIgDCjVo8PMOoUcK2wqTCl8O1wpY8wpjCkGM"
        )
        self.assertEqual(
            sync_page.next_sync_token,
            "w5ZGw6JFwqZmVcKsE8Kow4grw45QdybCnV_Cg8OASMKpwo1UY8K8bsKFwqJrw7DDhcKnM2RDOVbDt1E-"
            "wo7CnDjChMKKGsK1w5zCrA3CnU7CgEvDtsK6w7B2wrRZwrwPIgDCjVo8PMOoUcK2wqTCl8O1wpY8wpjCkGM"
        )
        self.assertEqual(len(sync_page.items), 8)
        self.assertEqual(str(sync_page.items[-1]), "<DeletedEntry id='CVebBDcQsSsu6yKKIayy'>")
        self.assertEqual(str(sync_page.items[-2]), "<DeletedAsset id='4hlteQAXS8iS0YCMU6QMWg'>")

    def test_sync_page_initial(self):
        sync_page = SyncPage({
            "sys": {
                "type": "Array"
            },
            "items": [
                {
                    "sys": {
                        "space": {
                            "sys": {
                                "type": "Link",
                                "linkType": "Space",
                                "id": "cfexampleapi"
                            }
                        },
                        "id": "5ETMRzkl9KM4omyMwKAOki",
                        "type": "Entry",
                        "createdAt": "2014-02-21T13:42:57.752Z",
                        "updatedAt": "2014-08-23T14:42:35.207Z",
                        "revision": 3,
                        "contentType": {
                            "sys": {
                                "type": "Link",
                                "linkType": "ContentType",
                                "id": "1t9IbcfdCk6m04uISSsaIK"
                            }
                        }
                    },
                    "fields": {
                        "name": {
                            "en-US": "London"
                        },
                        "center": {
                            "en-US": {
                                "lon": -0.12548719999995228,
                                "lat": 51.508515
                            }
                        }
                    }
                },
                {
                    "sys": {
                        "space": {
                            "sys": {
                                "type": "Link",
                                "linkType": "Space",
                                "id": "cfexampleapi"
                            }
                        },
                        "id": "7qVBlCjpWE86Oseo40gAEY",
                        "type": "Entry",
                        "createdAt": "2014-02-21T13:43:38.258Z",
                        "updatedAt": "2014-04-15T08:22:22.010Z",
                        "revision": 2,
                        "contentType": {
                            "sys": {
                                "type": "Link",
                                "linkType": "ContentType",
                                "id": "1t9IbcfdCk6m04uISSsaIK"
                            }
                        }
                    },
                    "fields": {
                        "name": {
                            "en-US": "San Francisco"
                        },
                        "center": {
                            "en-US": {
                                "lon": -122.41941550000001,
                                "lat": 37.7749295
                            }
                        }
                    }
                },
                {
                    "sys": {
                        "space": {
                            "sys": {
                                "type": "Link",
                                "linkType": "Space",
                                "id": "cfexampleapi"
                            }
                        },
                        "id": "ge1xHyH3QOWucKWCCAgIG",
                        "type": "Entry",
                        "createdAt": "2014-02-21T13:43:23.210Z",
                        "updatedAt": "2014-02-21T13:43:23.210Z",
                        "revision": 1,
                        "contentType": {
                            "sys": {
                                "type": "Link",
                                "linkType": "ContentType",
                                "id": "1t9IbcfdCk6m04uISSsaIK"
                            }
                        }
                    },
                    "fields": {
                        "name": {
                            "en-US": "Paris"
                        },
                        "center": {
                            "en-US": {
                                "lon": 2.3522219000000177,
                                "lat": 48.856614
                            }
                        }
                    }
                },
                {
                    "sys": {
                        "space": {
                            "sys": {
                                "type": "Link",
                                "linkType": "Space",
                                "id": "cfexampleapi"
                            }
                        },
                        "id": "4MU1s3potiUEM2G4okYOqw",
                        "type": "Entry",
                        "createdAt": "2014-02-21T13:42:45.926Z",
                        "updatedAt": "2014-02-21T13:42:45.926Z",
                        "revision": 1,
                        "contentType": {
                            "sys": {
                                "type": "Link",
                                "linkType": "ContentType",
                                "id": "1t9IbcfdCk6m04uISSsaIK"
                            }
                        }
                    },
                    "fields": {
                        "name": {
                            "en-US": "Berlin"
                        },
                        "center": {
                            "en-US": {
                                "lon": 13.404953999999975,
                                "lat": 52.52000659999999
                            }
                        }
                    }
                },
                {
                    "sys": {
                        "space": {
                            "sys": {
                                "type": "Link",
                                "linkType": "Space",
                                "id": "cfexampleapi"
                            }
                        },
                        "id": "1x0xpXu4pSGS4OukSyWGUK",
                        "type": "Asset",
                        "createdAt": "2013-11-06T09:45:10.000Z",
                        "updatedAt": "2013-12-18T13:27:14.917Z",
                        "revision": 6
                    },
                    "fields": {
                        "title": {
                            "en-US": "Doge"
                        },
                        "description": {
                            "en-US": "nice picture"
                        },
                        "file": {
                            "en-US": {
                                "url": "//images.contentful.com/cfexampleapi/1x0xpXu4pSGS4OukSyWGUK/cc1239c6385428ef26f4180190532818/doge.jpg",
                                "details": {
                                    "size": 522943,
                                    "image": {
                                        "width": 5800,
                                        "height": 4350
                                    }
                                },
                                "fileName": "doge.jpg",
                                "contentType": "image/jpeg"
                            }
                        }
                    }
                },
                {
                    "sys": {
                        "space": {
                            "sys": {
                                "type": "Link",
                                "linkType": "Space",
                                "id": "cfexampleapi"
                            }
                        },
                        "id": "jake",
                        "type": "Entry",
                        "createdAt": "2013-06-27T22:46:22.096Z",
                        "updatedAt": "2013-12-18T13:10:26.212Z",
                        "revision": 5,
                        "contentType": {
                            "sys": {
                                "type": "Link",
                                "linkType": "ContentType",
                                "id": "dog"
                            }
                        }
                    },
                    "fields": {
                        "name": {
                            "en-US": "Jake"
                        },
                        "description": {
                            "en-US": "Bacon pancakes, makin' bacon pancakes!"
                        },
                        "image": {
                            "en-US": {
                                "sys": {
                                    "type": "Link",
                                    "linkType": "Asset",
                                    "id": "jake"
                                }
                            }
                        }
                    }
                },
                {
                    "sys": {
                        "space": {
                            "sys": {
                                "type": "Link",
                                "linkType": "Space",
                                "id": "cfexampleapi"
                            }
                        },
                        "id": "happycat",
                        "type": "Entry",
                        "createdAt": "2013-06-27T22:46:20.171Z",
                        "updatedAt": "2013-11-18T15:58:02.018Z",
                        "revision": 8,
                        "contentType": {
                            "sys": {
                                "type": "Link",
                                "linkType": "ContentType",
                                "id": "cat"
                            }
                        }
                    },
                    "fields": {
                        "name": {
                            "en-US": "Happy Cat",
                            "tlh": "Quch vIghro'"
                        },
                        "likes": {
                            "en-US": [
                                "cheezburger"
                            ]
                        },
                        "color": {
                            "en-US": "gray"
                        },
                        "bestFriend": {
                            "en-US": {
                                "sys": {
                                    "type": "Link",
                                    "linkType": "Entry",
                                    "id": "nyancat"
                                }
                            }
                        },
                        "birthday": {
                            "en-US": "2003-10-28T23:00:00+00:00"
                        },
                        "lives": {
                            "en-US": 1
                        },
                        "image": {
                            "en-US": {
                                "sys": {
                                    "type": "Link",
                                    "linkType": "Asset",
                                    "id": "happycat"
                                }
                            }
                        }
                    }
                },
                {
                    "sys": {
                        "space": {
                            "sys": {
                                "type": "Link",
                                "linkType": "Space",
                                "id": "cfexampleapi"
                            }
                        },
                        "id": "6KntaYXaHSyIw8M6eo26OK",
                        "type": "Entry",
                        "createdAt": "2013-11-06T09:45:27.475Z",
                        "updatedAt": "2013-11-18T09:13:37.808Z",
                        "revision": 2,
                        "contentType": {
                            "sys": {
                                "type": "Link",
                                "linkType": "ContentType",
                                "id": "dog"
                            }
                        }
                    },
                    "fields": {
                        "name": {
                            "en-US": "Doge"
                        },
                        "description": {
                            "en-US": "such json\nwow"
                        },
                        "image": {
                            "en-US": {
                                "sys": {
                                    "type": "Link",
                                    "linkType": "Asset",
                                    "id": "1x0xpXu4pSGS4OukSyWGUK"
                                }
                            }
                        }
                    }
                },
                {
                    "sys": {
                        "space": {
                            "sys": {
                                "type": "Link",
                                "linkType": "Space",
                                "id": "cfexampleapi"
                            }
                        },
                        "id": "finn",
                        "type": "Entry",
                        "createdAt": "2013-06-27T22:46:21.450Z",
                        "updatedAt": "2013-09-09T16:15:01.297Z",
                        "revision": 6,
                        "contentType": {
                            "sys": {
                                "type": "Link",
                                "linkType": "ContentType",
                                "id": "human"
                            }
                        }
                    },
                    "fields": {
                        "name": {
                            "en-US": "Finn"
                        },
                        "description": {
                            "en-US": "Fearless adventurer! Defender of pancakes."
                        },
                        "likes": {
                            "en-US": [
                                "adventure"
                            ]
                        }
                    }
                },
                {
                    "sys": {
                        "space": {
                            "sys": {
                                "type": "Link",
                                "linkType": "Space",
                                "id": "cfexampleapi"
                            }
                        },
                        "id": "nyancat",
                        "type": "Entry",
                        "createdAt": "2013-06-27T22:46:19.513Z",
                        "updatedAt": "2013-09-04T09:19:39.027Z",
                        "revision": 5,
                        "contentType": {
                            "sys": {
                                "type": "Link",
                                "linkType": "ContentType",
                                "id": "cat"
                            }
                        }
                    },
                    "fields": {
                        "name": {
                            "en-US": "Nyan Cat",
                            "tlh": "Nyan vIghro'"
                        },
                        "likes": {
                            "en-US": [
                                "rainbows",
                                "fish"
                            ]
                        },
                        "color": {
                            "en-US": "rainbow"
                        },
                        "bestFriend": {
                            "en-US": {
                                "sys": {
                                    "type": "Link",
                                    "linkType": "Entry",
                                    "id": "happycat"
                                }
                            }
                        },
                        "birthday": {
                            "en-US": "2011-04-04T22:00:00+00:00"
                        },
                        "lives": {
                            "en-US": 1337
                        },
                        "image": {
                            "en-US": {
                                "sys": {
                                    "type": "Link",
                                    "linkType": "Asset",
                                    "id": "nyancat"
                                }
                            }
                        }
                    }
                },
                {
                    "sys": {
                        "space": {
                            "sys": {
                                "type": "Link",
                                "linkType": "Space",
                                "id": "cfexampleapi"
                            }
                        },
                        "id": "jake",
                        "type": "Asset",
                        "createdAt": "2013-09-02T14:56:34.260Z",
                        "updatedAt": "2013-09-02T15:22:39.466Z",
                        "revision": 2
                    },
                    "fields": {
                        "title": {
                            "en-US": "Jake"
                        },
                        "file": {
                            "en-US": {
                                "url": "//images.contentful.com/cfexampleapi/4hlteQAXS8iS0YCMU6QMWg/2a4d826144f014109364ccf5c891d2dd/jake.png",
                                "details": {
                                    "size": 20480,
                                    "image": {
                                        "width": 100,
                                        "height": 161
                                    }
                                },
                                "fileName": "jake.png",
                                "contentType": "image/png"
                            }
                        }
                    }
                },
                {
                    "sys": {
                        "space": {
                            "sys": {
                                "type": "Link",
                                "linkType": "Space",
                                "id": "cfexampleapi"
                            }
                        },
                        "id": "happycat",
                        "type": "Asset",
                        "createdAt": "2013-09-02T14:56:34.267Z",
                        "updatedAt": "2013-09-02T15:11:24.361Z",
                        "revision": 2
                    },
                    "fields": {
                        "title": {
                            "en-US": "Happy Cat"
                        },
                        "file": {
                            "en-US": {
                                "url": "//images.contentful.com/cfexampleapi/3MZPnjZTIskAIIkuuosCss/382a48dfa2cb16c47aa2c72f7b23bf09/happycatw.jpg",
                                "details": {
                                    "size": 59939,
                                    "image": {
                                        "width": 273,
                                        "height": 397
                                    }
                                },
                                "fileName": "happycatw.jpg",
                                "contentType": "image/jpeg"
                            }
                        }
                    }
                },
                {
                    "sys": {
                        "space": {
                            "sys": {
                                "type": "Link",
                                "linkType": "Space",
                                "id": "cfexampleapi"
                            }
                        },
                        "id": "nyancat",
                        "type": "Asset",
                        "createdAt": "2013-09-02T14:56:34.240Z",
                        "updatedAt": "2013-09-02T14:56:34.240Z",
                        "revision": 1
                    },
                    "fields": {
                        "title": {
                            "en-US": "Nyan Cat"
                        },
                        "file": {
                            "en-US": {
                                "url": "//images.contentful.com/cfexampleapi/4gp6taAwW4CmSgumq2ekUm/9da0cd1936871b8d72343e895a00d611/Nyan_cat_250px_frame.png",
                                "details": {
                                    "size": 12273,
                                    "image": {
                                        "width": 250,
                                        "height": 250
                                    }
                                },
                                "fileName": "Nyan_cat_250px_frame.png",
                                "contentType": "image/png"
                            }
                        }
                    }
                },
                {
                    "sys": {
                        "space": {
                            "sys": {
                                "type": "Link",
                                "linkType": "Space",
                                "id": "cfexampleapi"
                            }
                        },
                        "id": "garfield",
                        "type": "Entry",
                        "createdAt": "2013-06-27T22:46:20.821Z",
                        "updatedAt": "2013-08-27T10:09:07.929Z",
                        "revision": 2,
                        "contentType": {
                            "sys": {
                                "type": "Link",
                                "linkType": "ContentType",
                                "id": "cat"
                            }
                        }
                    },
                    "fields": {
                        "name": {
                            "en-US": "Garfield",
                            "tlh": "Garfield"
                        },
                        "likes": {
                            "en-US": [
                                "lasagna"
                            ]
                        },
                        "color": {
                            "en-US": "orange"
                        },
                        "birthday": {
                            "en-US": "1979-06-18T23:00:00+00:00"
                        },
                        "lifes": {
                            "en-US": 1
                        },
                        "lives": {
                            "en-US": 9
                        }
                    }
                }
            ],
            "nextPageUrl": (
                "https://cdn.contentful.com/spaces/cfexampleapi/environments/master/sync?"
                "sync_token=w5ZGw6JFwqZmVcKsE8Kow4grw45QdybCnV_Cg8OASMKpwo1UY8K8bsKFwqJrw7DDhcKnM2RDOVbDt1E-"
                "wo7CnDjChMKKGsK1wrzCrBzCqMOpZAwOOcOvCcOAwqHDv0XCiMKaOcOxZA8BJUzDr8K-wo1lNx7DnHE"
            )
        })

        self.assertEqual(
            sync_page.next_page_url,
            "https://cdn.contentful.com/spaces/cfexampleapi/environments/master/sync?"
            "sync_token=w5ZGw6JFwqZmVcKsE8Kow4grw45QdybCnV_Cg8OASMKpwo1UY8K8bsKFwqJrw7DDhcKnM2RDOVbDt1E-"
            "wo7CnDjChMKKGsK1wrzCrBzCqMOpZAwOOcOvCcOAwqHDv0XCiMKaOcOxZA8BJUzDr8K-wo1lNx7DnHE"
        )
        self.assertEqual(
            sync_page.next_sync_token,
            "w5ZGw6JFwqZmVcKsE8Kow4grw45QdybCnV_Cg8OASMKpwo1UY8K8bsKFwqJrw7DDhcKnM2RDOVbDt1E-"
            "wo7CnDjChMKKGsK1wrzCrBzCqMOpZAwOOcOvCcOAwqHDv0XCiMKaOcOxZA8BJUzDr8K-wo1lNx7DnHE"
        )
        self.assertEqual(len(sync_page.items), 14)
        self.assertEqual(str(sync_page.items[-1]), "<Entry[cat] id='garfield'>")
        self.assertEqual(
            str(sync_page.items[-2]),
            "<Asset id='nyancat' url='//images.contentful.com/cfexampleapi/4gp6taAwW4CmSgumq2ekUm/9da0cd1936871b8d72343e895a00d611/Nyan_cat_250px_frame.png'>"
        )

    def test__when_sync_has_multiple_pages__extracts_sync_token_from_next_page_url(self):
        sync_page = SyncPage({
            "sys": {
                "type": "Array"
            },
            "items": [
                {
                    "sys": {
                        "space": {
                            "sys": {
                                "type": "Link",
                                "linkType": "Space",
                                "id": "cfexampleapi"
                            }
                        },
                        "id": "4rPdazIwWkuuKEAQgemSmO",
                        "type": "DeletedEntry",
                        "createdAt": "2014-08-11T08:30:42.546Z",
                        "updatedAt": "2014-08-11T08:30:42.546Z",
                        "deletedAt": "2014-08-11T08:30:42.546Z",
                        "revision": 1
                    }
                }
            ],
            "nextPageUrl": (
                "https://cdn.contentful.com/spaces/cfexampleapi/environments/master/sync?"
                "sync_token=w5ZGw6JFwqZmVcKsE8Kow4grw45QdybCnV_Cg8OASMKpwo1UY8K8bsKFwqJrw7DDhcKnM2RDOVbDt1E-"
                "wo7CnDjChMKKGsK1w5zCrA3CnU7CgEvDtsK6w7B2wrRZwrwPIgDCjVo8PMOoUcK2wqTCl8O1wpY8wpjCkGM"
            )
        })

        self.assertEqual(
            sync_page.next_page_url,
            "https://cdn.contentful.com/spaces/cfexampleapi/environments/master/sync?"
            "sync_token=w5ZGw6JFwqZmVcKsE8Kow4grw45QdybCnV_Cg8OASMKpwo1UY8K8bsKFwqJrw7DDhcKnM2RDOVbDt1E-"
            "wo7CnDjChMKKGsK1w5zCrA3CnU7CgEvDtsK6w7B2wrRZwrwPIgDCjVo8PMOoUcK2wqTCl8O1wpY8wpjCkGM"
        )

    def test__when_SyncPage_has_property_next_page_url__get_sync_token_extracts_token_from_it(self):
        sync_page = SyncPage({
            "sys": {
                "type": "Array"
            },
            "items": [
                {
                    "sys": {
                        "space": {
                            "sys": {
                                "type": "Link",
                                "linkType": "Space",
                                "id": "cfexampleapi"
                            }
                        },
                        "id": "4rPdazIwWkuuKEAQgemSmO",
                        "type": "DeletedEntry",
                        "createdAt": "2014-08-11T08:30:42.546Z",
                        "updatedAt": "2014-08-11T08:30:42.546Z",
                        "deletedAt": "2014-08-11T08:30:42.546Z",
                        "revision": 1
                    }
                }
            ],
            "nextPageUrl": (
                "https://cdn.contentful.com/spaces/cfexampleapi/environments/master/sync?"
                "sync_token=w5ZGw6JFwqZmVcKsE8Kow4grw45QdybCnV_Cg8OASMKpwo1UY8K8bsKFwqJrw7DDhcKnM2RDOVbDt1E-"
                "wo7CnDjChMKKGsK1w5zCrA3CnU7CgEvDtsK6w7B2wrRZwrwPIgDCjVo8PMOoUcK2wqTCl8O1wpY8wpjCkGM"
            )
        })

        self.assertEqual(
            sync_page._get_sync_token(),
            "w5ZGw6JFwqZmVcKsE8Kow4grw45QdybCnV_Cg8OASMKpwo1UY8K8bsKFwqJrw7DDhcKnM2RDOVbDt1E-"
            "wo7CnDjChMKKGsK1w5zCrA3CnU7CgEvDtsK6w7B2wrRZwrwPIgDCjVo8PMOoUcK2wqTCl8O1wpY8wpjCkGM"
        )
