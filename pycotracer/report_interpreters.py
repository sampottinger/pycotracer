"""Downloaded data interpretation strategies for pycotracer.

Interpretation stategies that parse certain data fields like those with boolean
data, dates, and numerical values. Strategies are specific to report types from
Colorado Transparency in Contribution and Expenditure Reporting Campaign Finance
system data (TRACER)

@author: A. Samuel Pottinger (samnsparky, Gleap LLC)
@organization: Gleap LLC (gleap.org)
@copyright: 2013
@license: GNU GPL v3
"""

import datetime


def parse_iso_str(date_str):
    """Convienence function to parse an ISO 8601 datetime without timezone info.

    Convienece function to parse an ISO 8601 datetime string wihtout any
    timezone information. This is not a complete ISO 8601 parser, supporting a
    very limited subset of the standard.

    @param date_str: The ISO 8601 string to parse.
    @type date_str: str
    @return: The parsed datetime.
    @rtype: datetime.datetime
    """
    return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')


def parse_yes_no_str(bool_str):
    """Parse a string serialization of boolean data as yes (Y) or no (N).

    Prase a string serialization of boolean data where True is "Y" and False is
    "N" case-insensitive.

    @param bool_str: The string to parse.
    @type bool_str: str
    @return: The interpreted string.
    @rtype: bool
    @raise ValueError: Raised if the passed string is not equal to 'N' or 'Y'
        case insensitive.
    """
    lower_bool_str = bool_str.lower()
    if lower_bool_str == 'n':
        return False
    elif lower_bool_str == 'y':
        return True
    else:
        raise ValueError('%s not a valid boolean string.' % bool_str)


def interpret_contribution_entry(entry):
    """Interpret data fields within a CO-TRACER contributions report.

    Interpret the contribution amount, contribution date, filed date, amended,
    and amendment fields of the provided entry. All dates (contribution and
    filed) are interpreted together and, if any fails, all will retain their
    original value. Likewise, amended and amendment are interpreted together and
    if one is malformed, both will retain their original value. Entry may be
    edited in place and side-effects are possible in coupled code. However,
    client code should use the return value to guard against future changes.

    A value with the key 'AmountsInterpreted' will be set to True or False in
    the returned entry if floating point values are successfully interpreted
    (ContributionAmount) or not respectively.

    A value with the key 'DatesInterpreted' will be set to True or False in
    the returned entry if ISO 8601 strings are successfully interpreted
    (ContributionDate and FiledDate) or not respectively.

    A value with the key 'BooleanFieldsInterpreted' will be set to True or
    False in the returned entry if boolean strings are successfully interpreted
    (Amended and Amendment) or not respectively.

    @param entry: The contribution report data to manipulate / interpret.
    @type entry: dict
    @return: The entry passed 
    @raise ValueError: Raised if any expected field cannot be found in entry.
    """
    try:
        new_contribution_amount = float(entry['ContributionAmount'])
        entry['AmountsInterpreted'] = True
        entry['ContributionAmount'] = new_contribution_amount
    except ValueError:
        entry['AmountsInterpreted'] = False
    except TypeError:
        entry['AmountsInterpreted'] = False
    except AttributeError:
        entry['AmountsInterpreted'] = False

    try:
        contribution_date = parse_iso_str(entry['ContributionDate'])
        filed_date = parse_iso_str(entry['FiledDate'])
        entry['DatesInterpreted'] = True
        entry['ContributionDate'] = contribution_date
        entry['FiledDate'] = filed_date
    except ValueError:
        entry['DatesInterpreted'] = False
    except TypeError:
        entry['DatesInterpreted'] = False
    except AttributeError:
        entry['DatesInterpreted'] = False

    try: 
        amended = parse_yes_no_str(entry['Amended'])
        amendment = parse_yes_no_str(entry['Amendment'])
        entry['BooleanFieldsInterpreted'] = True
        entry['Amended'] = amended
        entry['Amendment'] = amendment
    except ValueError:
        entry['BooleanFieldsInterpreted'] = False
    except TypeError:
        entry['BooleanFieldsInterpreted'] = False
    except AttributeError:
        entry['BooleanFieldsInterpreted'] = False

    return entry


def interpret_contributions_data(entries):
    """Interpret data fields within CO-TRACER contributions reports.

    Interpret the contribution amount, contribution date, filed date, amended,
    and amendment fields of the provided entries. All dates (contribution and
    filed) are interpreted together and, if any fails, all within an entry will
    retain their original value. However, other entries in the same collection
    will be interpreted and edited independently. Likewise, amended and
    amendment are interpreted together and if one is malformed, both will retain
    its original value in that entry. Entries may be edited in place and
    side-effects are possible in coupled code. However,
    client code should use the return value to guard against future changes.

    A value with the key 'AmountsInterpreted' will be set to True or False in
    the returned entries if floating point values were successfully interpreted
    (ContributionAmount) or not respectively for that entry.

    A value with the key 'DatesInterpreted' will be set to True or False in
    the returned entries if ISO 8601 strings were successfully interpreted
    (ContributionDate and FiledDate) or not respectively for that entry.

    A value with the key 'BooleanFieldsInterpreted' will be set to True or
    False in the returned entries if boolean strings were successfully
    interpreted (Amended and Amendment) or not respectively for that entry.

    @param entries: The contribution report data to manipulate / interpret.
    @type entries: collection of dict
    @return: The entry passed 
    @raise ValueError: Raised if any expected field cannot be found in atleast
        one of the provided entries.
    """
    return map(interpret_contribution_entry, entries)


def interpret_expenditure_entry(entry):
    """Interpret data fields within a CO-TRACER expediture report.

    Interpret the expenditure amount, expenditure date, filed date, amended,
    and amendment fields of the provided entry. All dates (expenditure and
    filed) are interpreted together and, if any fails, all will retain their
    original value. Likewise, amended and amendment are interpreted together and
    if one is malformed, both will retain their original value. Entry may be
    edited in place and side-effects are possible in coupled code. However,
    client code should use the return value to guard against future changes.

    A value with the key 'AmountsInterpreted' will be set to True or False in
    the returned entry if floating point values are successfully interpreted
    (ExpenditureAmount) or not respectively.

    A value with the key 'DatesInterpreted' will be set to True or False in
    the returned entry if ISO 8601 strings are successfully interpreted
    (ExpenditureDate and FiledDate) or not respectively.

    A value with the key 'BooleanFieldsInterpreted' will be set to True or
    False in the returned entry if boolean strings are successfully interpreted
    (Amended and Amendment) or not respectively.

    @param entry: The expenditure report data to manipulate / interpret.
    @type entry: dict
    @return: The entry passed 
    @raise ValueError: Raised if any expected field cannot be found in entry.
    """
    try:
        expenditure_amount = float(entry['ExpenditureAmount'])
        entry['AmountsInterpreted'] = True
        entry['ExpenditureAmount'] = expenditure_amount
    except ValueError:
        entry['AmountsInterpreted'] = False

    try:
        expenditure_date = parse_iso_str(entry['ExpenditureDate'])
        filed_date = parse_iso_str(entry['FiledDate'])
        entry['DatesInterpreted'] = True
        entry['ExpenditureDate'] = expenditure_date
        entry['FiledDate'] = filed_date
    except ValueError:
        entry['DatesInterpreted'] = False

    try:
        amended = parse_yes_no_str(entry['Amended'])
        amendment = parse_yes_no_str(entry['Amendment'])
        entry['BooleanFieldsInterpreted'] = True
        entry['Amended'] = amended
        entry['Amendment'] = amendment
    except ValueError:
        entry['BooleanFieldsInterpreted'] = False

    return entry


def interpret_expenditure_data(entries):
    """Interpret data fields within CO-TRACER expenditure reports.

    Interpret the expenditure amount, expenditure date, filed date, amended,
    and amendment fields of the provided entries. All dates (expenditure and
    filed) are interpreted together and, if any fails, all within an entry will
    retain their original value. However, other entries in the same collection
    will be interpreted and edited independently. Likewise, amended and
    amendment are interpreted together and if one is malformed, both will retain
    their original value in that entry. Entries may be edited in place and
    side-effects are possible in coupled code. However, client code should use
    the return value to guard against future changes.

    A value with the key 'AmountsInterpreted' will be set to True or False in
    the returned entries if floating point values were successfully interpreted
    (ExpenditureAmount) or not respectively for that entry.

    A value with the key 'DatesInterpreted' will be set to True or False in
    the returned entries if ISO 8601 strings were successfully interpreted
    (ExpenditureDate and FiledDate) or not respectively for that entry.

    A value with the key 'BooleanFieldsInterpreted' will be set to True or
    False in the returned entries if boolean strings were successfully
    interpreted (Amended and Amendment) or not respectively for that entry.

    @param entries: The expediture report data to manipulate / interpret.
    @type entries: collection of dict
    @return: The entry passed 
    @raise ValueError: Raised if any expected field cannot be found in atleast
        one of the provided entries.
    """
    return map(interpret_expenditure_entry, entries)


def interpret_loan_entry(entry):
    """Interpret data fields within a CO-TRACER loan report.

    Interpret the payment amount, loan amount, interest rate, interest payment,
    loan balance, payment date, filed date, loan date, amended, and amendment
    fields of the provided entry. All dates (payment, filed, and loan) are
    interpreted together and, if any fails, all will retain their original
    value. Likewise, amended and amendment are interpreted together and
    if one is malformed, both will retain their original value. Finally,
    the payment amount, loan amount, interest rate, interest payment, and
    loan balance will be interpreted transactionally and, if any fail, all
    will retain their original value.

    Entry may be edited in place and side-effects are possible in coupled code.
    However, client code should use the return value to guard against future
    changes.

    A value with the key 'AmountsInterpreted' will be set to True or False in
    the returned entry if floating point values are successfully interpreted
    or not respectively.

    A value with the key 'DatesInterpreted' will be set to True or False in
    the returned entry if ISO 8601 strings are successfully interpreted
    or not respectively.

    A value with the key 'BooleanFieldsInterpreted' will be set to True or
    False in the returned entry if boolean strings are successfully interpreted
    or not respectively.

    @param entry: The loan report data to manipulate / interpret.
    @type entry: dict
    @return: The entry passed 
    @raise ValueError: Raised if any expected field cannot be found in entry.
    """
    try:
        payment_amount = float(entry['PaymentAmount'])
        loan_amount = float(entry['LoanAmount'])
        interest_rate = float(entry['InterestRate'])
        interest_payment = float(entry['InterestPayment'])
        loan_balance = float(entry['LoanBalance'])
        entry['AmountsInterpreted'] = True
        entry['PaymentAmount'] = payment_amount
        entry['LoanAmount'] = loan_amount
        entry['InterestRate'] = interest_rate
        entry['InterestPayment'] = interest_payment
        entry['LoanBalance'] = loan_balance
    except ValueError:
        entry['AmountsInterpreted'] = False

    try:
        payment_date = parse_iso_str(entry['PaymentDate'])
        filed_date = parse_iso_str(entry['FiledDate'])
        loan_date = parse_iso_str(entry['LoanDate'])
        entry['DatesInterpreted'] = True
        entry['PaymentDate'] = payment_date
        entry['FiledDate'] = filed_date
        entry['LoanDate'] = loan_date
    except ValueError:
        entry['DatesInterpreted'] = False

    try:
        amended = parse_yes_no_str(entry['Amended'])
        amendment = parse_yes_no_str(entry['Amendment'])
        entry['BooleanFieldsInterpreted'] = True
        entry['Amended'] = amended
        entry['Amendment'] = amendment
    except ValueError:
        entry['BooleanFieldsInterpreted'] = False

    return entry


def interpret_loan_data(entries):
    """Interpret data fields within CO-TRACER expenditure reports.

    Interpret the payment amount, loan amount, interest rate, interest payment,
    loan balance, payment date, filed date, loan date, amended, and amendment
    fields of the provided entries. All dates are interpreted together and, if
    any fails, all within an entry will retain their original value. However,
    other entries in the same collection will be interpreted and edited
    independently. Likewise, amended and amendment are interpreted together and
    if one is malformed, both will retain their original value in that entry.
    Finally, all floating point amounts are interpreted transactionally and,
    again, all will retain their original value if any fail.

    Entries may be edited in place and side-effects are possible in coupled
    code. However, client code should use the return value to guard against
    future changes.

    A value with the key 'AmountsInterpreted' will be set to True or False in
    the returned entries if floating point values were successfully interpreted
    or not respectively for that entry.

    A value with the key 'DatesInterpreted' will be set to True or False in
    the returned entries if ISO 8601 strings were successfully interpreted
    or not respectively for that entry.

    A value with the key 'BooleanFieldsInterpreted' will be set to True or
    False in the returned entries if boolean strings were successfully
    interpreted or not respectively for that entry.

    @param entries: The loan report data to manipulate / interpret.
    @type entries: collection of dict
    @return: The entry passed 
    @raise ValueError: Raised if any expected field cannot be found in atleast
        one of the provided entries.
    """
    return map(interpret_loan_entry, entries)
