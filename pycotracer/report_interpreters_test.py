"""Unit tests for download data interpretation logic.

Unit tests to exercise logic to interpret certain fields downloaded from the
Colorado Transparency in Contribution and Expenditure Reporting Campaign
Finance website (TRACER). This is an unofficial library.

These tests utalize a testing dataset in the testing_corpus subdirectory that
should be in the directory holding this script. This directory should include
one JSON file per report type, each file containing an object with a single
attribute with the same name as the report type. The value of that attribute
should be an Array of Arrays, each sub-array having two elements. The first of
that pair is a sample of data like that coming from the TRACER website and the
second is the expected dictionary after interpretation.

@author: A. Samuel Pottinger (samnsparky, Gleap LLC)
@organization: Gleap LLC (gleap.org)
@copyright: 2013
@license: GNU GPL v3
"""

import datetime
import json
import os
import unittest

import mox

import constants
import report_interpreters

CORPUS_FOLDER_NAME = 'testing_corpus'
TEST_INJECT_VALUES = {
    'date0': datetime.datetime(2013, 1, 1, 0, 0, 0),
    'date1': datetime.datetime(2013, 1, 17, 0, 0, 0),
    'date2': datetime.datetime(2012, 9, 28, 0, 0, 0)
}


class TestDataInterpretation(unittest.TestCase):
    """Unit tests for interpreting downloaded report data."""

    def load_testing_corpus(self, report_type):
        """Convienence function to load testing corpus data.

        @param report_type: The string identifier for the type of report that
            testing data should be loaded for.
        @type report_type: str
        @return: The loaded and de-serialized testing data.
        @rtype: dict
        """
        filename = '%s.json' % report_type
        parent_directory = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(parent_directory, CORPUS_FOLDER_NAME, filename)
        raw_data = json.load(open(path, 'rb'))[report_type]
        return self.load_dates(raw_data)

    def load_dates(self, raw_data):
        """Inject pre-created datetimes.

        Looks through loading test corpus data for the values in
        TEST_INJECT_VALUES, replacing those strings with the corresponding
        value in TEST_INJECT_VALUES.

        @param raw_data: The data to inject datetimes into.
        @type raw_data: dict
        """
        for (input_dict, expected_output) in raw_data:
            for field in expected_output.keys():
                value = expected_output[field]
                if value in TEST_INJECT_VALUES:
                    expected_output[field] = TEST_INJECT_VALUES[value]
        return raw_data

    def check_dict_equal(self, dict_1, dict_2):
        """Check if two dictionaries are equal.

        Convienence function for testing equality in two very large
        dictionaries, one item at a time. Asserts are executed within the body
        of this function.

        @param dict_1: The dictionary to test equality against.
        @type dict_1: dict
        @param dict_2: The dictionary to test equality for.
        @type dict_2: dict
        """
        self.assertEqual(dict_1.keys(), dict_2.keys())
        for key in dict_1.keys():
            self.assertEqual(dict_1[key], dict_2[key])


    def setUp(self):
        """Load testing corpus data. Called before each test."""
        self.contributions_data = self.load_testing_corpus(
            constants.REPORT_CONTRIB_DATA)
        self.expenditures_data = self.load_testing_corpus(
            constants.REPORT_EXPEND_DATA)
        self.loan_data = self.load_testing_corpus(
            constants.REPORT_LOAN_DATA)

    def test_interpret_contributions(self):
        """Test loading contribution reports."""
        for i in range(0, len(self.contributions_data)):
            (raw, expected_output) = self.contributions_data[i]
            output = report_interpreters.interpret_contribution_entry(raw)
            self.check_dict_equal(output, expected_output)

    def test_interpret_expenditures(self):
        """Test loading expenditure reports."""
        for i in range(0, len(self.expenditures_data)):
            (raw, expected_output) = self.expenditures_data[i]
            output = report_interpreters.interpret_expenditure_entry(raw)
            self.check_dict_equal(output, expected_output)

    def test_interpret_loans(self):
        """Test loading loan reports."""
        for i in range(0, len(self.loan_data)):
            (raw, expected_output) = self.loan_data[i]
            output = report_interpreters.interpret_loan_entry(raw)
            self.check_dict_equal(output, expected_output)


if __name__ == '__main__':
    unittest.main()
