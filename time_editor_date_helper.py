

"""Handles uncertain dates etc."""

import datetime
import dateutil.parser
import re

from qgis.PyQt.QtCore import QVariant


class TimeEditorDateHelper():

    def __init__(self):
        pass

    # TODO: what is the use case for adjacent???
    def date_within_lifespan(self, date_str, life_start, life_end, adjacent=False):
        life_start = str(life_start)
        life_end = str(life_end)
        if adjacent:
            # try:
            #     life_start = self.get_adjacent_date(life_start, False)
            # except OverflowError:
            #     pass
            life_start = self.get_adjacent_date(life_start, False)
            life_end = self.get_adjacent_date(life_end, True)
        if life_start != 'NULL':
            # It's safe to replace ?? with 01 as we need to expand both
            # month and day to the respective beginnings
            if "??" in life_start:
                life_start = life_start.replace("??", "01")
        if life_end != 'NULL':
            # for the end of the time span we need to expand to 12
            # and 31 (don't mind about the actual validity)
            if "??" in life_end:
                life_end_split = life_end.split("-")
                if life_end_split[1] == "??":
                    life_end_split[1] = "12"
                if life_end_split[2] == "??":
                    life_end_split[2] = "31"
                life_end = "-".join(life_end_split)
        # TODO: Handle ?? cases for the date_str parameter
        return (life_start <= date_str or life_start == 'NULL') and (date_str <= life_end or life_end == 'NULL')

    def dates_touch(self, date_str_a, date_str_b):
        """If date_str_a is incremented, does it return date_str_b"""
        adjacent_date = self.get_adjacent_date(str(date_str_a))
        return adjacent_date == str(date_str_b)

    def validate_date_string(self, date):
        """Validates a date string"""
        if isinstance(date, QVariant):
            if date.isNull():
                return (True, "")
            else:
                text_str = str(date)
            # return (True, "")
        elif isinstance(date, str):
            text_str = date
        if text_str.strip() == "":
            return (False, "Empty strings are not allowed. Use NULL instead")
        base_match = re.match("\d{4}-[?\d]{2}-[?\d]{2}$", text_str)
        if not base_match:
            return (False, "Date does not match YYYY-MM-DD Format")
        if "?" not in text_str:
            try:
                date_split = text_str.split("-")
                dates = [int(date_part) for date_part in date_split]
                dt = datetime.date(dates[0], dates[1], dates[2])
            except ValueError as e:
                return (False, text_str + " is not a valid date")
        return (True, "")

    def get_adjacent_date(self, date_str, after=True):
        """Finds the date adjacent to the provided datestring, if 
        date contains ?? the date is expanded to the next value, 
        e.g. 1973-01-?? leads to 1973-02-??, 1973-??-?? to 1974-??-??"""
        # NULL values can have no adjacent dates, so direct return
        if date_str == None or date_str == 'NULL' or date_str == '':
            return date_str
        # Getting adjacent date
        # If the date matches the ISO-Format simply convert and
        # apply delta operation
        if re.match("\d{4}-\d{2}-\d{2}$", date_str):
            dt = dateutil.parser.parse(date_str)
            if after:
                dt = dt + datetime.timedelta(days=1)
            else:
                dt = dt - datetime.timedelta(days=1)
            return datetime.date.strftime(dt, "%Y-%m-%d")
        # In case ?? are present, check which part is involved and
        # construct neighbouring datestrings
        else:
            date_parts = date_str.split("-")
            # check if month is unset -> return adjacent year
            if date_parts[1] == "??":
                year = int(date_parts[0])
                if after:
                    year += 1
                else:
                    year -= 1
                return "-".join([str(year).rjust(4, "0"), date_parts[1], date_parts[2]])
            # check if day is unset and construct adjacent month
            if date_parts[2] == "??":
                year = int(date_parts[0])
                month = int(date_parts[1])
                if after:
                    month += 1
                    if month == 13:
                        year += 1
                        month = 1
                else:
                    month -= 1
                    if month == 0:
                        year -= 1
                        month = 12

                return "-".join([str(year).rjust(4, "0"), str(month).rjust(2, "0"), date_parts[2]])

    def build_filter_string(self, layer, date_str):
        life_start_name = layer.customProperty("te_time_start")
        life_end_name = layer.customProperty("te_time_end")
        filter_str = f"""
(
    "{life_start_name}" <= '{date_str}' 
        OR 
    (
        "{life_start_name}" is NULL 
            AND
        (
            "{life_end_name}" >= '{date_str}' 
                OR 
            "{life_end_name}" is NULL
        )
    )
)	
    AND 
(
    "{life_end_name}" >= '{date_str}' 
        OR 
    (
        "{life_end_name}" is NULL 
            AND 
        (
            "{life_start_name}" <= '{date_str}'
                OR
            "{life_start_name}" is NULL
        )
    )
)"""
        return filter_str
