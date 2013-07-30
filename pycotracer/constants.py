"""Settings and constants for the pycotracer Python micro-library.

Settings and contants for a micro-library enabling programatic access to
Colorado Transparency in Contribution and Expenditure Reporting Campaign
Finance system data (TRACER). This is an unofficial library / access layer.

@author: A. Samuel Pottinger (samnsparky)
@organization: Gleap LLC (gleap.org)
@copyright: 2013
@license: GNU GPL v3
"""

START_YEAR = 2000
TRACER_DOMAIN = 'http://tracer.sos.colorado.gov/'
DOWNLOADS_URL = 'PublicSite/Docs/BulkDataDownloads/%d_%s.csv.zip'
BASE_URL = TRACER_DOMAIN + DOWNLOADS_URL
REPORT_CONTRIB_DATA = 'ContributionData'
REPORT_EXPEND_DATA = 'ExpenditureData'
REPORT_LOAN_DATA = 'LoanData'

REPORT_TYPES = [
    REPORT_CONTRIB_DATA,
    REPORT_EXPEND_DATA,
    REPORT_LOAN_DATA
]
