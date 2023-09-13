# TODO: move to testing directory and conform to best practice
from time_editor_date_helper import TimeEditorDateHelper

dh = TimeEditorDateHelper()

year_test_after = dh.get_adjacent_date("1973-??-??", True)
year_test_before = dh.get_adjacent_date("1973-??-??", False)

print(year_test_after)
print(year_test_before)

month_test_after = dh.get_adjacent_date("1973-12-??", True)
month_test_before = dh.get_adjacent_date("1973-01-??", False)

print(month_test_after)
print(month_test_before)

simple_test_after = dh.get_adjacent_date("1973-01-31", True)
simple_test_before = dh.get_adjacent_date("1973-01-31", False)

print(simple_test_after)
print(simple_test_before)




