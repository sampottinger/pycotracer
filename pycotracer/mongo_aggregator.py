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

FIELD_TRANSFORM_INDEX = {
    'CO_ID': 'commiteeID',
    'MI': 'middleInitial',
    'ContributionAmount': 'amount',
    'ExpenditureAmount': 'amount',
    'LoanDate': 'loanStartDate',
    'PaymentDate': 'date'
}


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


def clean_entry(entry):
    """Consolidate some entry attributes and rename a few others.

    Consolidate address attributes into a single field and replace some field
    names with others as described in FIELD_TRANSFORM_INDEX.

    @param entry: The entry attributes to update.
    @type entry: dict
    @return: Entry copy after running clean operations
    @rtype: dict
    """
    newEntry = {}

    if 'Address1' in entry:
        address = str(entry['Address1'])
        if entry['Address2'] != '':
            address = address + ' ' + str(entry['Address2'])
        newEntry['address'] = address
        del entry['Address1']
        del entry['Address2']

    for key in entry.keys():

        if key != None:
        
            if key in FIELD_TRANSFORM_INDEX:
                newKey = FIELD_TRANSFORM_INDEX[key]
            else:
                newKey = key
            
            newKey = newKey[:1].lower() + newKey[1:]
            newEntry[newKey] = entry[key]

    return newEntry


def update_contribution_entry(database, entry):
    """Update a record of a contribution report in the provided database.

    @param database: The MongoDB database to operate on. The contributions
        collection will be used from this database.
    @type db: pymongo.database.Database
    @param entry: The entry to insert into the database, updating the entry with
        the same recordID if one exists.
    @type entry: dict
    """
    entry = clean_entry(entry)
    database.contributions.update(
        {'recordID': entry['recordID']},
        {'$set': entry},
        upsert=True
    )


def update_expenditure_entry(database, entry):
    """Update a record of a expenditure report in the provided database.

    @param db: The MongoDB database to operate on. The expenditures collection
        will be used from this database.
    @type db: pymongo.database.Database
    @param entry: The entry to insert into the database, updating the entry with
        the same recordID if one exists.
    @type entry: dict
    """
    entry = clean_entry(entry)
    database.expenditures.update(
        {'recordID': entry['recordID']},
        {'$set': entry},
        upsert=True
    )


def update_loan_entry(database, entry):
    """Update a record of a loan report in the provided database.

    @param db: The MongoDB database to operate on. The loans collection will be
        used from this database.
    @type db: pymongo.database.Database
    @param entry: The entry to insert into the database, updating the entry with
        the same recordID if one exists.
    @type entry: dict
    """
    entry = clean_entry(entry)
    database.loans.update(
        {'recordID': entry['recordID']},
        {'$set': entry},
        upsert=True
    )


def insert_contribution_entries(database, entries):
    """Insert a set of records of a contribution report in the provided database.

    Insert a set of new records into the provided database without checking
    for conflicting entries.

    @param database: The MongoDB database to operate on. The contributions
        collection will be used from this database.
    @type db: pymongo.database.Database
    @param entries: The entries to insert into the database.
    @type entries: dict
    """
    entries = map(clean_entry, entries)
    database.contributions.insert(entries, continue_on_error=True)


def insert_expenditure_entries(database, entries):
    """Insert a set of records of a expenditure report in the provided database.

    Insert a set of new records into the provided database without checking
    for conflicting entries.

    @param db: The MongoDB database to operate on. The expenditures collection
        will be used from this database.
    @type db: pymongo.database.Database
    @param entries: The entries to insert into the database.
    @type entries: dict
    """
    entries = map(clean_entry, entries)
    database.expenditures.insert(entries, continue_on_error=True)


def insert_loan_entries(database, entries):
    """Insert a set of records of a loan report in the provided database.

    Insert a set of new records into the provided database without checking
    for conflicting entries.

    @param db: The MongoDB database to operate on. The loans collection will be
        used from this database.
    @type db: pymongo.database.Database
    @param entries: The entries to insert into the database.
    @type entries: dict
    """
    entries = map(clean_entry, entries)
    database.loans.insert(entries, continue_on_error=True)


def update_entry(database, entry, report_type):
    """Update a record of a contribution report in the provided database.

    @param db: The MongoDB database to operate on. The contributions collection
        will be used from this database.
    @type db: pymongo.database.Database
    @param entry: The entry to insert into the database, updating the entry with
        the same recordID if one exists.
    @type entry: dict
    @param report_type: The type of report being updated. Should be one of the
        strings in constants.REPORT_TYPES.
    @type report_type: str
    @raise ValueError: Raised if the requested report type could not be found.
    """
    factory = UpdateStrategyFactory.get_instance()
    strategy = factory.get_strategy(report_type)
    if not strategy:
        raise ValueError('%s not a recognized report type.' % report_type)

    return strategy(database, entry, reassign_id=reassign_id,
        force_copy=force_copy)


def update_contribution_entries(database, entries):
    """Update a collection contribution reports in the provided database.

    @param database: The MongoDB database to operate on. The contributions
        collection will be used from this database.
    @type db: pymongo.database.Database
    @param entry: The entries to insert into the database, updating the entry
        with the same recordID if one exists.
    @type entry: dict
    """
    map(lambda x: update_contribution_entry(database, x), entries)


def update_expenditure_entries(database, entries):
    """Update a collection expenditure reports in the provided database.

    @param db: The MongoDB database to operate on. The expenditures collection
        will be used from this database.
    @type db: pymongo.database.Database
    @param entries: The entry to insert into the database, updating the entry with
        the same recordID if one exists.
    @type entries: dict
    """
    map(lambda x: update_expenditure_entry(database, x), entries)


def update_loan_entries(database, entries):
    """Update a collection loan reports in the provided database.

    @param db: The MongoDB database to operate on. The loans collection will be
        used from this database.
    @type db: pymongo.database.Database
    @param entry: The entry to insert into the database, updating the entry with
        the same recordID if one exists.
    @type entry: dict
    """
    map(lambda x: update_loan_entry(database, x), entries)
