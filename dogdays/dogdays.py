from datetime import datetime, date, time, timedelta


class DateRange(object):

    def __init__(self, begin, end):
        if begin > end:
            raise ValueError("Invalid Range")
        self.begin = begin
        self.end = end
    
    @property
    def duration(self):
        return (self.end - self.begin).total_seconds() / (60 * 60)
    
    def __eq__(self, other):
        return     self.begin == other.begin and \
                self.end == other.end
    
    def __repr__(self):
        return "<DateRange begin:{}, end:{}>".format(self.begin, self.end)
        
    def disjoint(self, other):
        leftmost = self.leftmost(other)
        rightmost = self.rightmost(other)
        if leftmost == rightmost:
            return False
        else:
            return leftmost.end < rightmost.begin
    
    def intersects(self, other):
        return self.intersection(other) is not None
        
    def intersection(self, other):
        if self.encompassed_by(other):
            return DateRange(self.begin, self.end)
        elif self.encompasses(other):
            return DateRange(other.begin, other.end)
        elif self.disjoint(other):
            return None
        else:
            leftmost = self.leftmost(other)
            rightmost = self.rightmost(other)
            return DateRange(leftmost.end, rightmost.begin)

    def encompasses(self, other):
        return     self.begin <= other.begin and self.end >= other.end
    
    def encompassed_by(self, other):
        return other.encompasses(self)
        
    def leftmost(self, other):
        if self.begin <= other.begin:
            return self
        else:
            return other
    
    def rightmost(self, other):
        if self.end >= other.end:
            return self
        else:
            return other
    
    def iterdates(self):
        current = self.begin.date()
        end = self.end.date()
        while current <= end:
            yield current
            current += timedelta(1)

class DateRangeList(object):
    
    def __init__(self, *ranges):
        self.ranges = list(ranges)
    
    def add(self, begin, end):
        range = DateRange(begin, end)
        self.add_range(range)
        return self
    
    def add_range(self, range_to_add):
        if self.intersects_any(range_to_add):
            raise ValueError("Attempt to add intersecting range to a DateRangeList")
        for i, range_added in enumerate(self.ranges[:]):
            if range_to_add.begin < range_added.begin:
                self.ranges.insert(i, range_to_add)
                break
        else:
            self.ranges.append(range_to_add)
        return self
    
    def intersects_any(self, range):
        for range_added in self:
            if range_added.intersects(range):
                return True
        return False
        
    def __contains__(self, elmt):
        return elmt in self.ranges
    
    def __eq__(self, other):
        return self.ranges == other.ranges
        
    def __iter__(self):
        for range in self.ranges:
            yield range
    
    @property
    def total_hours(self):
        return sum([ range.duration for range in self ])
        
class BaseWorkRegimen(object):
    def work_hours_for(self, date):
        raise NotImplementedError
    
    def is_working_day(self, date):
        return True

class BusinessDayRegimen(BaseWorkRegimen):
    SATURDAY = 5
    SUNDAY = 6

    def __init__(self):
        self.holidays = set()

    def add_holiday(self, holiday):
        self.holidays.add(holiday)
    
    def is_working_day(self, date):
        if date.weekday() in (self.SATURDAY, self.SUNDAY):
            return False
        elif date in self.holidays:
            return False
        else:
            return True    
            
class FixedHoursRegimen(BaseWorkRegimen):

    DEFAULT_WORKHOURS = [ 
        (time(9), time(17))
    ]
    
    def __init__(self):
        self.holidays = set()
        self.work_hours = self.DEFAULT_WORKHOURS
    
    def work_hours_for(self, date):
        if self.is_working_day(date):
            return self._build_work_hours(date)
        else:
            return DateRangeList()
    
    def _build_work_hours(self, date):
        # This seems to have bugs yet to be found
        result = DateRangeList()
        date_offset = timedelta(0)
        last_begin_time = None
        for begin_time, end_time in self.work_hours:
            if last_begin_time and last_begin_time > begin_time:
                date_offset += timedelta(1)
            range = self._build_range(date + date_offset, begin_time, end_time)
            if range.begin.date() < range.end.date():
                date_offset += timedelta(1)
            result.add_range(range)
            last_begin_time = begin_time
        return result
        
    def _build_range(self, date, begin_time, end_time):
        begin_datetime = datetime.combine(date, begin_time)
        if begin_time < end_time:
            end_datetime = datetime.combine(date, end_time)
        else:
            end_datetime = datetime.combine(date + timedelta(1), end_time)
        return DateRange(begin_datetime, end_datetime)

class WorkRegimen(BusinessDayRegimen, FixedHoursRegimen):
    DEFAULT_WORKHOURS = [ 
        (time(9), time(17))
    ]

class Calendar(object):
    def __init__(self, work_regimen):
        self.regimen = work_regimen
    
    def work_hours_between(self, begin, end):
        work_hours = 0.0
        range = DateRange(begin, end)
        for day in range.iterdates():
            pass
            #work_hours += self.regimen.work_hours_for(date)