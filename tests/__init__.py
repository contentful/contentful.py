import sys
import os
from .asset_test import *
from .client_test import *
from .content_type_cache_test import *
from .content_type_field_types_test import *
from .content_type_field_test import *
from .content_type_test import *
from .deleted_asset_test import *
from .deleted_entry_test import *
from .entry_test import *
from .errors_test import *
from .locale_test import *
from .resource_builder_test import *
from .resource_test import *
from .space_test import *
from .sync_page_test import *
from .utils_test import *


sys.path.insert(0, os.path.abspath('..'))
