from __future__ import absolute_import, unicode_literals

import datetime
import decimal
import json
import uuid
from django.db.models import QuerySet
from django.forms import model_to_dict
from django.utils import six
from django.utils.duration import duration_iso_string
from django.utils.functional import Promise
from django.utils.timezone import is_aware
from django.utils import timezone
from gerapy.server.core.models import Client
from gerapy.server.core.time import DATE_TIME_FORMAT


class JSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time, decimal types and UUIDs.
    """
    
    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            return timezone.localtime(o).strftime(DATE_TIME_FORMAT)
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            if is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, datetime.timedelta):
            return duration_iso_string(o)
        elif isinstance(o, decimal.Decimal):
            return str(o)
        elif isinstance(o, uuid.UUID):
            return str(o)
        elif isinstance(o, Promise):
            return six.text_type(o)
        elif isinstance(o, QuerySet):
            return list(o.values())
        elif isinstance(o, Client):
            return model_to_dict(o)
        else:
            return super(JSONEncoder, self).default(o)
