"""Logic for retrieving and orchestrating parsing of CO-TRACER reports.

Main data retrival and interpretation orchestration logic for a micro-library
enabling programatic access to Colorado Transparency in Contribution and
Expenditure Reporting Campaign Finance system data (TRACER). This provides the
functions necessary for downloading and parsing TRACER data and should be used
by client code if the logic imported into pycotracers's __init__.py file is
insufficient. This micro-library is an unofficial library / access layer.

@author: A. Samuel Pottinger (samnsparky, Gleap LLC)
@organization: Gleap LLC (gleap.org)
@copyright: 2013
@license: GNU GPL v3
"""


import cStringIO
import urllib2
import csv
import zipfile

import constants
import report_interpreters

CONTRIB_STR = constants.REPORT_CONTRIB_DATA
EXPEND_STR = constants.REPORT_EXPEND_DATA
LOAN_STR = constants.REPORT_LOAN_DATA
REPORT_TYPE_INTERPRETERS = {
    CONTRIB_STR: report_interpreters.interpret_contributions_data,
    EXPEND_STR: report_interpreters.interpret_expenditure_data,
    LOAN_STR: report_interpreters.interpret_loan_data
}


def get_url(year, report_type):
    """Get the URL for a ZIP archive containing a CSV file for a TRACER report.

    Get the URL / web address where a GET request will yield a ZIP archive
    containing a CSV report that fits the provided parameters.

    @param year: The year about which a report is being requested.
    @type year: int
    @param report_type: The type of report to generate a URL for. Should be one
        of the strings listed in constants.REPORT_TYPES.
    @type report_type: str
    @return: URL on the official TRACER site where an un-interpreted / cleaned
        CSV report archive can be downloaded
    @rtype: str
    """
    return constants.BASE_URL % (year, report_type)


def is_valid_report_type(report_type):
    """Determines if the the given report type descriptor is valid.

    Indiciates if the given report type is one of the recognized report types
    supported by this library. Should be one of the report types provided by
    the official TRACER site. Value types are available in
    constants.REPORT_TYPES.

    @param report_type: String describing the report type.
    @type report_type: str
    @return: True if recognized and valid and False otherwise.
    @rtype: bool
    """
    return report_type in constants.REPORT_TYPES


def get_zipped_file(url, encoding_error_opt='ignore'):
    """Download and unzip the report file at the given URL.

    Downloads and unzips the CO-TRACER archive at the given URL. This is not
    intended for data outside of the CO-TRACER official site and it will
    automatically extract the first file found in the downloaded zip archive
    as the CO-TRACER website produces single file archives. Note that the
    contents of that file are loaded directly into memory.

    @param url: The URL to download the archive from.
    @type url: str
    @return: The contents of the first file found in the provided archive.
    @rtype: str
    """
    remotezip = urllib2.urlopen(url)
    raw_contents = cStringIO.StringIO(remotezip.read())
    target_zip = zipfile.ZipFile(raw_contents)
    first_filename = target_zip.namelist()[0]
    return unicode(target_zip.read(first_filename), errors=encoding_error_opt)


def get_report_raw(year, report_type):
    """Download and extract a CO-TRACER report.

    Generate a URL for the given report, download the corresponding archive,
    extract the CSV report, and interpret it using the standard CSV library.

    @param year: The year for which data should be downloaded.
    @type year: int
    @param report_type: The type of report that should be downloaded. Should be
        one of the strings in constants.REPORT_TYPES.
    @type report_type: str
    @return: A DictReader with the loaded data. Note that this data has not
        been interpreted so data fields like floating point values, dates, and
        boolean values are still strings.
    @rtype: csv.DictReader
    """
    if not is_valid_report_type(report_type):
        msg = '%s is not a valid report type.' % report_type
        raise ValueError(msg)

    url = get_url(year, report_type)
    raw_contents = get_zipped_file(url)
    return csv.DictReader(cStringIO.StringIO(raw_contents))


def get_report_interpreted(year, report_type):
    """Download, exract, and interpret a CO-TRACER report.

    Generate a URL for the given report, download the corresponding archive,
    extract the CSV report, and interpret it using TRACER-specific logic.

    @param year: The year for which data should be downloaded.
    @type year: int
    @param report_type: The type of report that should be downloaded. Should be
        one of the strings in constants.REPORT_TYPES.
    @type report_type: str
    @return: A collection of dict with the loaded data. Note that this data has
        been interpreted so data fields like floating point values, dates, and
        boolean values are no longer strings.
    @rtype: Iterable over dict
    """
    if not is_valid_report_type(report_type):
        msg = '%s is not a valid report type.' % report_type
        raise ValueError(msg)

    raw_report = get_report_raw(year, report_type)
    interpreter = REPORT_TYPE_INTERPRETERS[report_type]
    return interpreter(raw_report)


def get_report(year, report_type=None):
    """Download, extract, and interpret a CO-TRACER report or reports.

    Generate a URL for the given report, download the corresponding archive,
    extract the CSV report, and interpret it using TRACER-specific logic. If
    no report type is provided, this process is repeated for all available
    report types for the given year.

    @param year: The year to retrieve a report or reports for.
    @type year: int
    @keyword report_type: The type of report that should be downloaded. Should
        be one of the strings in constants.REPORT_TYPES. If None, all reports
        for the given year will be downloaded. Defaults to None.
    @type report_type: str or None
    @return: A collection of dict with the loaded data. Note that this data has
        been interpreted so data fields like floating point values, dates, and
        boolean values are no longer strings. If report_type was None, this
        will be a dictionary where the keys are the report types as listed in
        constants.REPORT_TYPES and the values are Iterable over dict. Each dict
        rendered by that iterable will have one report entry.
    @rtype: dict or Iterable over dict
    """
    if report_type == None:
        report_types = constants.REPORT_TYPES
        report_sections = [
            get_report_interpreted(year, report) for report in report_types
        ]

        return dict(zip(constants.REPORT_TYPES, report_sections))
    
    else:
        return get_report_interpreted(year, report_type)
