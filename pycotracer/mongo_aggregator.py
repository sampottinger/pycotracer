"""Simple Mongo-DB serialization convienence module for pycotracer.

Convienence / reference implementation for serializing data read from the
pycotracer micro-library to a database. The pycotracer micro-library provides
programatic access to Colorado Transparency in Contribution and Expenditure
Reporting Campaign Finance system data (TRACER). This is an unofficial library /
access layer.

@author: A. Samuel Pottinger (samnsparky, Gleap LLC)
@organization: Gleap LLC (gleap.org)
@copyright: 2013
@license: GNU GPL v3
"""

import bson
import copy

import pymongo

import constants


class UpdateStrategyFactory:
    """A strategy producing factory that serializes different types of reports.

    A strategy producing factory intended to be used as a singleton. This
    factory produces strategies capable of serializing different types of
    reports to a MonogDB or compatabile serialization layer.
    """

    __instance = None

    @classmethod
    def get_instance(cls):
        """Get the shared instance of this singleton.

        Provides access to a shared instance of this singleton. Will create
        the singleton instance if it has not yet been initalized. This singleton
        should be created lazily.

        @return Shared instance of this singleton.
        @rtype UpdateStrategyFactory
        """
        if cls.__instance == None:
            cls.__instance = UpdateStrategyFactory()
        return cls.__instance

    def __init__(self):
        self.__strategies = {
            constants.REPORT_CONTRIB_DATA: update_contribution_entry,
            constants.REPORT_EXPEND_DATA: update_expenditure_entry,
            constants.REPORT_LOAN_DATA: update_loan_entry
        }

    def get_strategy(self, report_type):
        """Get the serialization strategy for the given type of report.

        Get the serialization strategy (function) appropriate to the given type
        of TRACER report.

        @param report_type: The type of report to serialize. Returns None if no
            appropriate strategy could be found.
        @type report_type: String. Should be one of the strings listed in
            constants.REPORT_TYPES.
        """
        return self.__strategies.get(report_type, None)


def update_contribution_entry(database, entry, reassign_id=True,
    force_copy=False):
    """Update a record of a contribution report in the provided database.

    @param database: The MongoDB database to operate on. The contributions
        collection will be used from this database.
    @type db: pymongo.database.Database
    @param entry: The entry to insert into the database, updating the entry with
        the same _id if one exists.
    @type entry: dict
    @keyword reassign_id: Indicates if the entry's _id value should be set to
        RecordID value. Defaults to True.
    @type reassign_id: bool
    @keyword force_copy: Indicates if the entry should be shallow copied before
        being modified. If False, the passed entry and code using it may
        experience side-effects. Setting to True can increase memory usage.
        Defaults to False.
    @type force_copy: bool
    """
    database.contributions.update({'RecordID': entry['RecordID']}, entry, upsert=True)


def update_expenditure_entry(database, entry, reassign_id=True,
    force_copy=False):
    """Update a record of a expenditure report in the provided database.

    @param db: The MongoDB database to operate on. The expenditures collection
        will be used from this database.
    @type db: pymongo.database.Database
    @param entry: The entry to insert into the database, updating the entry with
        the same _id if one exists.
    @type entry: dict
    @keyword reassign_id: Indicates if the entry's _id value should be set to
        RecordID value. Defaults to True.
    @type reassign_id: bool
    @keyword force_copy: Indicates if the entry should be shallow copied before
        being modified. If False, the passed entry and code using it may
        experience side-effects. Setting to True can increase memory usage.
        Defaults to False.
    @type force_copy: bool
    """
    database.expenditures.update({'RecordID': entry['RecordID']}, entry, upsert=True)


def update_loan_entry(database, entry, reassign_id=True, force_copy=False):
    """Update a record of a loan report in the provided database.

    @param db: The MongoDB database to operate on. The loans collection will be
        used from this database.
    @type db: pymongo.database.Database
    @param entry: The entry to insert into the database, updating the entry with
        the same _id if one exists.
    @type entry: dict
    @keyword reassign_id: Indicates if the entry's _id value should be set to
        RecordID value. Defaults to True.
    @type reassign_id: bool
    @keyword force_copy: Indicates if the entry should be shallow copied before
        being modified. If False, the passed entry and code using it may
        experience side-effects. Setting to True can increase memory usage.
        Defaults to False.
    @type force_copy: bool
    """
    database.loans.update({'RecordID': entry['RecordID']}, entry, upsert=True)


def update_entry(database, entry, report_type, reassign_id=True,
    force_copy=False):
    """Update a record of a contribution report in the provided database.

    @param db: The MongoDB database to operate on. The contributions collection
        will be used from this database.
    @type db: pymongo.database.Database
    @param entry: The entry to insert into the database, updating the entry with
        the same _id if one exists.
    @type entry: dict
    @param report_type: The type of report being updated. Should be one of the
        strings in constants.REPORT_TYPES.
    @type report_type: str
    @keyword reassign_id: Indicates if the entry's _id value should be set to
        RecordID value. Defaults to True.
    @type reassign_id: bool
    @keyword force_copy: Indicates if the entry should be shallow copied before
        being modified. If False, the passed entry and code using it may
        experience side-effects. Setting to True can increase memory usage.
        Defaults to False.
    @type force_copy: bool
    @raise ValueError: Raised if the requested report type could not be found.
    """
    factory = UpdateStrategyFactory.get_instance()
    strategy = factory.get_strategy(report_type)
    if not strategy:
        raise ValueError('%s not a recognized report type.' % report_type)

    return strategy(database, entry, reassign_id=reassign_id,
        force_copy=force_copy)
