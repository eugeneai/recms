import pytz
import datetime

def convert_datetime(dt, tz_from, tz_to):
    """
    Convert a naive datetime.datetime "dt" from one timezone to another.
    tz_from and tz_to may be either pytz.timezone instances, or timezone strings.
    Examples:
    Convert UTC datetime to US/Eastern:
    convert_datetime(datetime.datetime.utcnow(), pytz.utc, 'US/Eastern')

    Convert US/Eastern datetime to UTC:
    convert_datetime(datetime.datetime.now(), 'US/Eastern', pytz.utc)

    Convert US/Eastern datetime to ES/Pacific:
    convert_datetime(datetime.datetime.now(), 'US/Eastern', 'US/Pacific')
    """
    if type(tz_from) == str:
        tz_from = pytz.timezone(tz_from)
    if type(tz_to) == str:
        tz_to = pytz.timezone(tz_to)
    dt = make_naive(dt)
    if tz_from == tz_to: return dt.replace(tzinfo=tz_to)
    return tz_from.normalize(tz_from.localize(dt)).astimezone(tz_to)

def convert_from_utc(dt, tz_to):
    return convert_datetime(dt, pytz.utc, tz_to)

def convert_to_utc(dt, tz_from):
    return convert_datetime(dt, tz_from, pytz.utc)

def make_naive(dt):
    return dt.replace(tzinfo=None)

def make_aware(dt):
    return dt.replace(tzinfo=pytz.utc)

def get_timezone_for_request(request=None, default='UTC'):
    # FIXME: consider making this a user preference
    if request:
        return request.registry.settings.get('default_timezone', default)
    else:
        return default

def convert_from_utc_to_request_tz(dt, request):
    return convert_from_utc(dt, get_timezone_for_request(request))

def convert_to_utc_from_request_tz(dt, request):
    return convert_to_utc(dt, get_timezone_for_request(request))

def today_for_request_tz(request):
    """ Return "today's date" for the request's timezone.
    Kinda tricky since at any moment there are always two current dates, depending on your local timezone.
    On the other hand, there's only one UTC date at any moment.
    """
    return convert_from_utc_to_request_tz(datetime.datetime.utcnow(), request).date()

def utcnow(zero_seconds=False):
    """ Returns a timezone aware version of utcnow.
    If zero_seconds, the datetime will be rounded down to the minute.
    """
    now = datetime.datetime.now(pytz.utc)
    if zero_seconds: return now.replace(second=0, microsecond=0)
    return now

