import unittest
from dogdays import DateRange, DateRangeList, WorkRegimen
from datetime import datetime, date, time

class DateRangeTest(unittest.TestCase):
    
    def setUp(self):
        self.date1 = datetime(2015, 1, 1, 0, 0, 0)
        self.date2 = datetime(2015, 1, 1, 12, 0, 0)
        self.date3 = datetime(2015, 1, 2, 0, 0, 0)
        self.date4 = datetime(2015, 1, 2, 12, 0, 0)
        self.date5 = datetime(2015, 1, 3, 0, 0, 0)
        self.date6 = datetime(2015, 1, 3, 12, 0, 0)
    
    def tearDown(self):
        pass
    
    def test_it_creates_a_range(self):
        range = DateRange(self.date1, self.date2)
    
    def test_it_fails_to_create_a_negative_range(self):
        with self.assertRaises(ValueError):
            range = DateRange(self.date2, self.date1)

    def test_it_returns_the_duration_in_hours(self):
        range = DateRange(self.date1, self.date2)
        self.assertAlmostEqual(range.duration, 12.0)
    
    def test_it_implements_equality(self):
        range1 = DateRange(self.date1, self.date2)
        range2 = DateRange(self.date1, self.date2)
        range3 = DateRange(self.date1, self.date3)
        self.assertEqual(range1, range2)
        self.assertNotEqual(range1, range3)
    
    def test_it_encompasses_other_range(self):
        range1 = DateRange(self.date1, self.date4)
        range2 = DateRange(self.date2, self.date4)
        self.assertTrue(range1.encompasses(range2))

    def test_it_does_not_encompass_other_range(self):
        range1 = DateRange(self.date3, self.date4)
        left_disjoint = DateRange(self.date1, self.date2)
        right_disjoint = DateRange(self.date5, self.date5)
        left_intersect = DateRange(self.date1, self.date3)
        right_intersect = DateRange(self.date3, self.date6)
        
        self.assertFalse(range1.encompasses(left_disjoint))
        self.assertFalse(range1.encompasses(right_disjoint))
        self.assertFalse(range1.encompasses(left_intersect))
        self.assertFalse(range1.encompasses(right_intersect))
    
    def test_it_is_encompassed_by_other_range(self):
        range1 = DateRange(self.date2, self.date4)
        range2 = DateRange(self.date1, self.date4)
        self.assertTrue(range1.encompassed_by(range2))

    def test_it_is_not_encompassed_by_other_range(self):
        range1 = DateRange(self.date3, self.date4)
        left_disjoint = DateRange(self.date1, self.date2)
        right_disjoint = DateRange(self.date5, self.date5)
        left_intersect = DateRange(self.date1, self.date3)
        right_intersect = DateRange(self.date3, self.date6)
        
        self.assertFalse(left_disjoint.encompassed_by(range1))
        self.assertFalse(right_disjoint.encompassed_by(range1))
        self.assertFalse(left_intersect.encompassed_by(range1))
        self.assertFalse(right_intersect.encompassed_by(range1))

    def test_it_returns_the_leftmost_range(self):
        range1 = DateRange(self.date1, self.date3)
        range2 = DateRange(self.date3, self.date4)
        self.assertEqual(range1.leftmost(range2), range1)

    def test_it_returns_the_rightmost_range(self):
        range1 = DateRange(self.date1, self.date3)
        range2 = DateRange(self.date3, self.date4)
        self.assertEqual(range1.rightmost(range2), range2)    
        
    def test_it_is_disjoint_from_another_range(self):
        range1 = DateRange(self.date1, self.date2)
        range2 = DateRange(self.date3, self.date4)
        self.assertTrue(range1.disjoint(range2))
    
    def test_it_is_not_disjoint_from_another_range(self):
        range1 = DateRange(self.date1, self.date2)
        range2 = DateRange(self.date2, self.date4)
        self.assertFalse(range1.disjoint(range2))

    def test_it_returns_the_intersection_of_two_equal_ranges(self):
        range1 = DateRange(self.date1, self.date3)
        range2 = DateRange(self.date1, self.date3)
        range3 = DateRange(self.date1, self.date3)
        self.assertEqual(range1.intersection(range2), range3)
    
    def test_it_returns_the_intersection_of_disjoint_ranges(self):
        range1 = DateRange(self.date1, self.date2)
        range2 = DateRange(self.date3, self.date4)
        self.assertTrue(range1.intersection(range2) is None)
    
    def test_it_returns_the_intersection_with_an_encompassing_range(self):
        range1 = DateRange(self.date1, self.date2)
        range2 = DateRange(self.date1, self.date4)
        range3 = DateRange(self.date1, self.date2)
        self.assertEqual(range1.intersection(range2), range3)
    
    def test_it_returns_the_intersection_with_an_encompassed_range(self):
        range1 = DateRange(self.date1, self.date4)
        range2 = DateRange(self.date1, self.date2)
        range3 = DateRange(self.date1, self.date2)
        self.assertEqual(range1.intersection(range2), range3)

    def test_it_returns_the_intersection_with_a_range(self):
        range1 = DateRange(self.date3, self.date4)
        range2 = DateRange(self.date1, self.date3)
        range3 = DateRange(self.date3, self.date3)
        self.assertEqual(range1.intersection(range2), range3)
    
    def test_it_intersects(self):
        range1 = DateRange(self.date3, self.date4)
        range2 = DateRange(self.date1, self.date3)
        self.assertTrue(range1.intersection(range2))
    
    def test_it_iterates_the_days_between_two_dates(self):
        range = DateRange(self.date1, self.date6)
        expected = [ date(2015, 1, 1), date(2015, 1, 2), date(2015, 1, 3) ]
        result = [ day for day in range.iterdates() ]
        self.assertEqual(expected, result)

class DateRangeListTest(unittest.TestCase):
    
    def setUp(self):
        self.date1 = datetime(2015, 1, 1, 0, 0, 0)
        self.date2 = datetime(2015, 1, 1, 12, 0, 0)
        self.date3 = datetime(2015, 1, 2, 0, 0, 0)
        self.date4 = datetime(2015, 1, 2, 12, 0, 0)
        self.date5 = datetime(2015, 1, 3, 0, 0, 0)
        self.date6 = datetime(2015, 1, 3, 12, 0, 0)
        self.list = DateRangeList()
        
    def tearDown(self):
        pass
    
    def test_it_adds_date_ranges(self):
        range1 = DateRange(self.date1, self.date2)
        self.list.add(self.date1, self.date2)
        self.assertIn(range1, self.list)
        
    def test_it_sums_the_workhours(self):
        range1 = DateRange(self.date1, self.date2)
        range2 = DateRange(self.date3, self.date4)
        range3 = DateRange(self.date5, self.date6)
        self.list.add_range(range1).add_range(range2).add_range(range3)
        self.assertEqual(self.list.total_hours, 36.0)
    
    def test_it_keeps_the_ranges_sorted(self):
        range1 = DateRange(self.date5, self.date6)
        range2 = DateRange(self.date3, self.date4)
        range3 = DateRange(self.date1, self.date2)
        self.list.add_range(range1).add_range(range2).add_range(range3)
        expected = [ range3, range2, range1 ]
        self.assertEqual(self.list.ranges, expected)
    
    def test_it_does_not_add_intersecting_ranges(self):
        range1 = DateRange(self.date1, self.date2)
        range2 = DateRange(self.date3, self.date6)        
        range3 = DateRange(self.date5, self.date6)
        self.list.add_range(range2).add_range(range1)
        with self.assertRaises(ValueError):
            self.list.add_range(range3)

class WorkRegimenTest(unittest.TestCase):
    """
        January 2015
    su mo tu wd th fr sa
                 1  2  3
     4  5  6  7  8  9 10
    11 12 13 14 15 16 17
    18 19 20 21 22 23 24
    25 26 27 28 29 30 31

    Holiday = 1
    """

    def setUp(self):
        self.work_regimen = WorkRegimen()
        self.jan1st = date(2015, 1, 1)
        self.saturday = date(2015, 1, 3)
        self.sunday = date(2015, 1, 4)
        self.monday = date(2015, 1, 5)
        self.tuesday = date(2015, 1, 6)
        self.wednesday = date(2015, 1, 7)
        self.work_regimen.add_holiday(self.jan1st)
        self.work_regimen.work_hours = [ (time(9), time(17)) ]
    def tearDown(self):
        pass
        
    def test_it_knows_a_holiday_is_not_a_working_day(self):
        result = self.work_regimen.is_working_day(self.jan1st)
        self.assertFalse(result)
    
    def test_it_knows_weekends_are_a_working_days(self):
        result = self.work_regimen.is_working_day(self.saturday)
        self.assertFalse(result)
        result = self.work_regimen.is_working_day(self.sunday)
        self.assertFalse(result)
    
    def test_it_knows_non_weekend_days_are_working_days(self):
        result = self.work_regimen.is_working_day(self.monday)
        self.assertTrue(result)
    
    def test_it_returns_empty_working_hours_for_a_non_working_day(self):
        result = self.work_regimen.work_hours_for(self.jan1st)
        self.assertEqual(result, DateRangeList())
    
    def test_it_returns_working_hours_for_a_working_day(self):
        begin = datetime.combine(self.monday, time(9))
        end = datetime.combine(self.monday, time(17))
        expected = DateRangeList().add(begin, end)
        result = self.work_regimen.work_hours_for(self.monday)
        self.assertEqual(result, expected)

    def test_it_returns_working_hours_for_a_working_day_with_a_long_lunch(self):
        self.work_regimen.work_hours = [ (time(9), time(12)), (time(13), time(18)) ]
        begin = datetime.combine(self.monday, time(9))
        end = datetime.combine(self.monday, time(12))
        morning = DateRange(begin, end)    
        begin = datetime.combine(self.monday, time(13))
        end = datetime.combine(self.monday, time(18))
        afternoon = DateRange(begin, end)
        expected = DateRangeList(morning, afternoon)
        result = self.work_regimen.work_hours_for(self.monday)
        self.assertEqual(result, expected)
        
    def test_it_returns_working_hours_for_a_night_worker(self):
        self.work_regimen.work_hours = [ (time(21), time(5)) ]
        begin = datetime.combine(self.monday, time(21))
        end = datetime.combine(self.tuesday, time(5))
        expected = DateRangeList( DateRange(begin, end) )
        result = self.work_regimen.work_hours_for(self.monday)
        self.assertEqual(result, expected)
    
    def test_it_returns_working_hours_for_a_30_hours_residency_shift(self):
        self.work_regimen.work_hours = [ (time(21), time(21)), (time(7), time(13)) ]
        
        begin = datetime.combine(self.monday, time(21))
        end = datetime.combine(self.tuesday, time(21))
        first_duty = DateRange(begin, end)
        
        begin = datetime.combine(self.wednesday, time(7))
        end = datetime.combine(self.wednesday, time(13))
        second_duty = DateRange(begin, end)
        
        expected = DateRangeList(first_duty, second_duty)
        result = self.work_regimen.work_hours_for(self.monday)
        self.assertEqual(result, expected)
        
class CalendarTest(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    