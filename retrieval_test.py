"""Unit tests for retrieving and orchestrating parsing of CO-TRACER reports.

@author: A. Samuel Pottinger (samnsparky, Gleap LLC)
@organization: Gleap LLC (gleap.org)
@copyright: 2013
@license: GNU GPL v3
"""

# pylint: disable=E1101
# pylint: disable=E1103
# pylint: disable=R0904

import cStringIO
import datetime
import unittest
import urllib2
import zipfile

import mox

import constants
import retrieval


class RetrievalTest(mox.MoxTestBase):
    """Unit tests for retrieval and parsing orchestration."""

    def test_get_url(self):
        """Test generating a URL for a report archive."""
        test_url = retrieval.get_url(2013, 'ContributionData')
        self.assertIn('2013', test_url)
        self.assertIn('ContributionData', test_url)
    
    def test_get_zipped_file(self):
        """Test downloading and extracting a CSV file / report archive."""
        self.mox.StubOutWithMock(urllib2, 'urlopen')
        self.mox.StubOutClassWithMocks(zipfile, 'ZipFile')

        test_url = 'test_url'
        test_data = cStringIO.StringIO('test_data')
        
        urllib2.urlopen(test_url).AndReturn(test_data)
        zip_file = zipfile.ZipFile(mox.IgnoreArg())
        zip_file.namelist().AndReturn(['test_filename_1'])
        zip_file.read('test_filename_1').AndReturn('test_file_contents')
        
        self.mox.ReplayAll()
        ret_val = retrieval.get_zipped_file(test_url)

        self.assertEqual(ret_val, 'test_file_contents')

    def test_get_report_raw_invalid(self):
        """Test requesting an invalid type of report."""
        with self.assertRaises(ValueError):
            retrieval.get_report_raw(2013, '_invalid_type')

    def test_get_report_raw(self):
        """Test getting the raw but extracted archive of a TRACER CSV report."""
        self.mox.StubOutWithMock(retrieval, 'get_url')
        self.mox.StubOutWithMock(retrieval, 'get_zipped_file')

        test_dict_data = 'test1,test2,test3\n1,2,3'

        test_url = 'test_url'
        test_year = 2013
        test_report_type = constants.REPORT_CONTRIB_DATA

        retrieval.get_url(test_year, test_report_type).AndReturn(test_url)
        retrieval.get_zipped_file(test_url).AndReturn(test_dict_data)

        self.mox.ReplayAll()
        ret_val = retrieval.get_report_raw(test_year, test_report_type)
        first_row = ret_val.next()
        self.assertEqual(first_row['test1'], '1')
        self.assertEqual(first_row['test2'], '2')
        self.assertEqual(first_row['test3'], '3')

    def test_get_report_interpreted_invalid(self):
        """Test getting an invalid type of raw TRACER report."""
        with self.assertRaises(ValueError):
            retrieval.get_report_interpreted(2013, '_invalid_type')

    def test_get_report_interpreted(self):
        """Test getting an interpreted TRACER report."""
        self.mox.StubOutWithMock(retrieval, 'get_report_raw')

        test_year = 2013
        test_report_type = constants.REPORT_CONTRIB_DATA

        ret_val = [{
            'ContributionAmount': '100',
            'ContributionDate': '2013-01-01 00:00:00',
            'FiledDate': '2013-01-02 00:00:00',
            'Amended': 'Y',
            'Amendment': 'N'
        }]
        retrieval.get_report_raw(test_year, test_report_type).AndReturn(ret_val)

        self.mox.ReplayAll()
        ret_val = retrieval.get_report_interpreted(test_year, test_report_type)
        ret_entry = ret_val[0]
        test_date_1 = datetime.datetime(2013, 1, 1, 0, 0, 0)
        test_date_2 = datetime.datetime(2013, 1, 2, 0, 0, 0)
        self.assertEqual(ret_entry['ContributionAmount'], 100)
        self.assertEqual(ret_entry['ContributionDate'], test_date_1)
        self.assertEqual(ret_entry['FiledDate'], test_date_2)
        self.assertEqual(ret_entry['Amended'], True)
        self.assertEqual(ret_entry['Amendment'], False)


if __name__ == '__main__':
    unittest.main()
