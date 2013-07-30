"""Unit tests for the convienence MongoDB aggegator for pycotracer.

@author: A. Samuel Pottinger (samnsparky, Gleap LLC)
@organization: Gleap LLC (gleap.org)
@copyright: 2013
@license: GNU GPL v3
"""

import unittest

import mox

import constants
import mongo_aggregator


class TestMongoAggregator(mox.MoxTestBase):
    """Test suite for the MongoDB aggregator logic."""

    def test_update_strategy_factory(self):
        """Test using the UpdateStrategyFactory to get update strategies."""
        factory = mongo_aggregator.UpdateStrategyFactory.get_instance()

        expend_strategy = factory.get_strategy(constants.REPORT_EXPEND_DATA)
        expected_strategy = mongo_aggregator.update_expenditure_entry
        self.assertEqual(expend_strategy, expected_strategy)

    def test_manage_id_reassignment_no_copy(self):
        """Test loading an _id for a new entry without a shallow copy."""
        start_entry = {'RecordID': 1}
        new_entry = mongo_aggregator.manage_id_reassignment(start_entry, True,
            False)
        self.assertEqual(start_entry, new_entry)
        self.assertEqual(new_entry, {'RecordID': 1, '_id': 1})

    def test_manage_id_reassignment_copy(self):
        """Test loading an _id for a new entry with a shallow copy."""
        start_entry = {'RecordID': 1}
        new_entry = mongo_aggregator.manage_id_reassignment(start_entry, True,
            True)
        self.assertEqual(start_entry, {'RecordID': 1})
        self.assertEqual(new_entry, {'RecordID': 1, '_id': 1})

    def test_manage_id_reassignment_noop(self):
        """Test logic to avoid adding _id for a new entry."""
        start_entry = {'RecordID': 1}
        new_entry = mongo_aggregator.manage_id_reassignment(start_entry, False,
            False)
        self.assertEqual(new_entry, {'RecordID': 1})

    def test_update_entry_invalid(self):
        """Test serializing an entry of an unknown report type."""
        test_dict = {}
        with self.assertRaises(ValueError):
            mongo_aggregator.update_entry(None, test_dict, '_invalid_type')

    def test_update_entry(self):
        """Test updating an entry by specifying its report type via a string."""
        self.mox.StubOutWithMock(mongo_aggregator, 'update_contribution_entry')

        entry = {'RecordID': 1}
        mongo_aggregator.update_contribution_entry(
            None,
            entry,
            reassign_id=True,
            force_copy=False
        ).AndReturn(None)

        self.mox.ReplayAll()
        mongo_aggregator.update_entry(
            None,
            entry,
            'ContributionData',
            reassign_id=True,
            force_copy=False
        )


if __name__ == '__main__':
    unittest.main()
