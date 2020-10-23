#  Import section

from datetime import datetime, date
from abc import ABC, abstractmethod, abstractproperty
import utils

# Interface of Widgets


class WidgetInterface(ABC):
    def __init__(self, widget_id):
        self.widget_id = widget_id or ''

    @abstractmethod
    def __str__(self) -> str:
        pass

# Widget from PerfLog


class Widget(WidgetInterface):

    def __init__(self, widget_id, widget_type,
                 widget_name, widget_ttfb,
                 widget_duration, widget_timestamp,
                 widget_finish_timestamp,
                 user_action,
                 user_action_timestamp):
        super().__init__(widget_id)
        if widget_type is not None:
            self.widget_type = utils.check_widget_type(widget_type)
        else:
            self.widget_type = widget_type
        self.widget_name = widget_name or 'N/A'
        if widget_ttfb is not None:
            # self.widget_ttfb = '{:,.2f}'.format(float(widget_ttfb) / 1000)
            self.widget_ttfb = '{:,.2f}'.format(float(widget_ttfb))
        else:
            self.widget_ttfb = widget_ttfb or 'N/A'
        self.widget_duration = widget_duration
        if widget_timestamp is not None:
            self.widget_timestamp = utils.format_time(widget_timestamp)
        else:
            self.widget_timestamp = widget_timestamp or 'N/A'
        if widget_finish_timestamp is not None:
            self.widget_finish_timestamp = utils.format_time(widget_finish_timestamp)
        else:
            self.widget_finish_timestamp = widget_finish_timestamp or 'N/A'
        self.user_action = user_action or ''
        if user_action_timestamp is not None:
            self.user_action_timestamp = utils.format_time(user_action_timestamp)
        else:
            self.user_action_timestamp = user_action_timestamp or 'N/A'

    @property
    def __str__(self) -> str:
        return f'widget_id: {self.widget_id}, widget_type: {self.widget_type}, widget_name: {self.widget_name},' \
               f'widget_ttfb: {self.widget_ttfb}, widget_duration: {self.widget_duration}, ' \
               f'widget_timestamp: {self.widget_timestamp}'

# Widget from Content Lib


class WidgetContentLib(WidgetInterface):

    def __init__(self, story_entity_id, story_entity_name, page_title, widget_class, widget_id, widget_title):
        super().__init__(widget_id)
        self.story_entity_id = story_entity_id or ''
        self.story_entity_name = story_entity_name or ''
        self.page_title = page_title or ''
        self.widget_class = utils.check_widget_type(widget_class) or ''
        self.widget_title = widget_title or ''

    def __str__(self) -> str:
        pass

# Story Object


class Story:

    def __init__(self, story_id, story_name, story_description,
                 story_createdby, story_createdtime, story_modifiedby, story_modifiedtime):
        self.story_id = story_id or ''
        self.story_name = story_name or ''
        self.story_createdby = story_createdby or ''
        temp_story_createdtime = datetime.strptime(story_createdtime, "%Y-%m-%dT%H:%M:%S.%fZ")
        self.story_createdtime = temp_story_createdtime.strftime('%m.%d.%Y %H:%M:%S') or ''
        self.story_modifiedby = story_modifiedby or ''
        temp_story_modifiedtime = datetime.strptime(story_modifiedtime, "%Y-%m-%dT%H:%M:%S.%fZ")
        self.story_modifiedtime = temp_story_modifiedtime.strftime('%m.%d.%Y %H:%M:%S') or ''
        self.story_description = story_description or ''

    def __str__(self) -> str:
        return f'story_id: {self.story_id}, story_name: {self.story_name}, ' \
               f'story_createdby: {self.story_createdby}, story_createdtime: {self.story_createdtime},' \
               f'story_modifiedby: {self.story_modifiedby}, story_modifiedtime: {self.story_modifiedtime}'

# For collecting DataSources Data, which are being requested by GetResponse:


class DataSource:

    def __init__(self, ds_id=0, dimensions={}, ds_runtime=0, view='', ds_name='', ds_type='', ds_cache=''):
        self.ds_id = ds_id or ''
        self.dimensions = dimensions or {}
        self.ds_runtime = ds_runtime or 0
        self.view = view or 'Result Set'
        self.ds_name = ds_name or 'Result Set'
        self.ds_type = ds_type or 'Result Set'
        self.ds_cache = ds_cache

# Calculation Entity


class CalcEntity:

    def __init__(self, id=0, name='', type=''):
        self.id = id or 0
        self.name = name or ''
        self.type = type or ''

# Basic Call


class Call:

    def __init__(self, url, start_timestamp='', total_time=0, body_size=0,
                 resource_type=0, status=0, transfer_size=0, timings=None):
        self.url = url or ''
        if start_timestamp != '':
            temp_start_timestamp = datetime.strptime(start_timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
            self.start_timestamp = utils.format_time(temp_start_timestamp)
        self.total_time = '{:,.2f}'.format(total_time / 1000) or 0
        self.body_size = body_size or 0
        self.resource_type = resource_type or ''
        self.status = status or ''
        self.transfer_size = transfer_size or 0
        self.timings = {k: float(v / 1000) for k, v in timings.items()}

# Call for Get Response (successor of class Call)


class Call_2(Call):

    def __init__(self, url, get_response_type, start_timestamp='', total_time=0, body_size=0,
                 resource_type=0, status=0, transfer_size=0, timings=None,
                 stories=None, widgets=None, runtime=0, measurements=None, datasources=None):
        super().__init__(url, start_timestamp, total_time, body_size,
                         resource_type, status, transfer_size, timings)
        self.get_response_type = get_response_type or ''
        self.stories = stories or []
        self.widgets = widgets or []
        self.runtime = round(runtime, 3) or 0
        self.measurements = measurements or []
        self.datasources = datasources or []


# Product Object


class Product:

    def __init__(self, product_installationid, product_patch, product_version, product_host):
        self.product_installationid = product_installationid or ''
        self.product_patch = product_patch or ''
        self.product_version = product_version or ''
        self.product_host = product_host or ''
