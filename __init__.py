"""Micro-library for downloading, parsing, and storing Colorado TRACER data.

Micro-library for downloading, extracting, parsing / interpreting, and storing
Colorado Transparency in Contribution and Expenditure Reporting Campaign Finance
system data (TRACER) using public CSV archive URLs. See Readme.textile for usage
guidelines. While testing requires installation of the pymox library, this
micro-library should not require any external dependencies.

While this top level module provides basic interfaces for usage, advanced use
cases may require interaction with the retrieval submodule.

@author: A. Samuel Pottinger (samnsparky, Gleap LLC)
@organization: Gleap LLC (gleap.org)
@copyright: 2013
@license: GNU GPL v3
"""

from pycotracer.retrieval import get_report
from pycotracer.mongo_aggregator import update_entry
from pycotracer.constants import REPORT_TYPES
from pycotracer.constants import REPORT_CONTRIB_DATA
from pycotracer.constants import REPORT_EXPEND_DATA
from pycotracer.constants import REPORT_LOAN_DATA
