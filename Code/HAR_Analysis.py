import json
import pandas as pd
from tabulate import tabulate
from datetime import datetime, date
from abc import ABC, abstractmethod, abstractproperty

import settings
import utils

pd.options.display.max_columns = None
pd.options.display.width = None


# Descriptive classes

class Widget:

    def __init__(self, widget_id, widget_type, widget_name, widget_duration, widget_timestamp):
        self.widget_id = widget_id
        self.widget_type = widget_type
        self.widget_name = widget_name
        self.widget_ttfb = 0
        self.widget_duration = widget_duration
        self.widget_timestamp = widget_timestamp.strftime('%m.%d.%Y %H:%M:%S')

    def __str__(self) -> str:
        return f'widget_id: {self.widget_id}, widget_type: {self.widget_type}, widget_name: {self.widget_name},' \
               f'widget_ttfb: {self.widget_ttfb}, widget_duration: {self.widget_duration}, ' \
               f'widget_timestamp: {self.widget_timestamp}'


class StoryInterface(ABC):

    def __init__(self, story_id, story_name):
        self.story_id = story_id or ''
        self.story_name = story_name or ''

    @abstractmethod
    def __str__(self) -> str:
        pass


class Story(StoryInterface):

    def __init__(self, story_id, story_name, story_timestamp):
        super().__init__(story_id, story_name)
        self.story_timestamp = story_timestamp or ''

    def __str__(self) -> str:
        return f'story_id: {self.story_id}, story_name: {self.story_name}, ' \
               f'story_timestamp: {self.story_timestamp}'


class Story_2(StoryInterface):

    def __init__(self, story_id, story_name, story_description,
                 story_createdby, story_createdtime, story_modifiedby, story_modifiedtime):
        super().__init__(story_id, story_name)
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


class Call:

    def __init__(self, url, start_timestamp='', total_time=0, body_size=0,
                 resource_type=0, status=0, transfer_size=0, timings=None,
                 stories=None, widgets=None, runtime=0, measurements=None):
        self.url = url or ''
        if start_timestamp != '':
            temp_start_timestamp = datetime.strptime(start_timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
            self.start_timestamp = temp_start_timestamp.strftime('%m.%d.%Y %H:%M:%S')
        self.total_time = total_time or 0
        self.body_size = body_size or 0
        self.resource_type = resource_type or ''
        self.status = status or ''
        self.transfer_size = transfer_size or 0
        self.timings = timings or {}
        self.stories = stories or []
        self.widgets = widgets or []
        self.runtime = runtime or 0
        self.measurements = measurements or []


# class Model:
#
#     def __init__(self, model_id, model_timestamp, model_datasourcetype, model_createdby,
#                  model_modifiedby, model_modifiedtime, model_instance, model_schema):
#         self.model_id = model_id or ''
#         self.model_timestamp = model_timestamp or ''
#         self.model_datasourcetype = model_datasourcetype or ''
#         self.model_createdby = model_createdby or ''
#         self.model_modofiedby = model_modifiedby or ''
#         self.model_modifiedtime = model_modifiedtime or ''
#         self.model_instance = model_instance or ''
#         self.model_schema = model_schema or ''


class Product:

    def __init__(self, product_installationid, product_patch, product_version, product_host):
        self.product_installationid = product_installationid or ''
        self.product_patch = product_patch or ''
        self.product_version = product_version or ''
        self.product_host = product_host or ''


# Functional class

class StoryAnalyzer:

    def __init__(self, path):
        self.file_path = path
        self.calls = self.read_har_file()

    def read_har_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            har_parser = json.loads(f.read())
            return har_parser['log']['entries']

    # def get_story_info(self):
    #     story_info = {}
    #     for call in self.calls:
    #         if call['request']['url'].__contains__('userFriendlyPerfLog'):
    #             facts = json.loads(call['response']['content']['text'])['fact']
    #             for fact in facts:
    #                 if ('storyId' not in fact) or (fact['storyId'] in story_info.keys()):
    #                     continue
    #                 else:
    #                     story_info[fact['storyId']] = Story(
    #                         fact['storyId'],
    #                         fact['storyName'],
    #                         fact['storyTstamp'])
    #     return story_info

    def get_story_info_2(self):
        story_info = {}
        for call in self.calls:
            if call['request']['url'].__contains__('contentlib'):
                address_of_info = json.loads(call['response']['content']['text'])
                if isinstance(json.loads(call['response']['content']['text']), list):
                    continue
                elif "resource" in json.loads(call['response']['content']['text']).keys():
                    story_tmp = Story_2(story_id=address_of_info['resource']['resourceId'],
                                        story_name=address_of_info['resource']['name'],
                                        story_description=address_of_info['resource']['description'],
                                        story_createdby=address_of_info['resource']['createdByDisplayName'],
                                        story_createdtime=address_of_info['resource']['createdTime'],
                                        story_modifiedby=address_of_info['resource']['modifiedByDisplayName'],
                                        story_modifiedtime=datetime.strptime(
                                            address_of_info['resource']['modifiedTime'], "%Y-%m-%dT%H:%M:%S.%fZ"))
                    story_info[address_of_info['resource']['resourceId']] = story_tmp
                elif "resourceId" in json.loads(call['response']['content']['text']).keys():
                    story_tmp = Story_2(story_id=address_of_info['resourceId'],
                                        story_name=address_of_info['name'],
                                        story_description=address_of_info['description'],
                                        story_createdby=address_of_info['createdBy'],
                                        story_createdtime=address_of_info['createdTime'],
                                        story_modifiedby=address_of_info['modifiedBy'],
                                        story_modifiedtime=address_of_info['modifiedTime'])
                    story_info[address_of_info['resourceId']] = story_tmp
        return story_info

    # def get_model_info(self):
    #     model_info = {}
    #     for call in self.calls:
    #         if call['request']['url'].__contains__('contentlib'):
    #             model_tmp = Model()
    #             address_of_info = json.loads(call['response']['content']['text'])
    #             if isinstance(json.loads(call['response']['content']['text']), dict):
    #                 continue
    #             elif json.loads(call['response']['content']['text'])[0]['resourceType'] == 'CUBE':
    #                 model_tmp.model_id = address_of_info[0]['resourceId']
    #                 model_tmp.model_timestamp = address_of_info[0]['name']
    #                 model_tmp.model_datasourcetype = address_of_info[0]['description']
    #                 model_tmp.model_createdby = address_of_info[0]['createdByDisplayName']
    #                 model_tmp.model_modifiedby = address_of_info[0]['createdTime']
    #                 model_tmp.model_modifiedtime = address_of_info[0]['modifiedByDisplayName']
    #                 model_tmp.model_instance = address_of_info[0]['modifiedTime']
    #                 model_tmp.model_schema = address_of_info[0]['']
    #                 model_info[address_of_info['resource']['resourceId']] = story_tmp
    #
    #     model_id, model_timestamp, model_datasourcetype, model_createdby,
    #     model_modifiedby, model_modifiedtime, model_instance, model_schema
    #     return story_info

    def get_product_info(self):
        product_info = {}
        for call in self.calls:
            if call['request']['url'].__contains__('application/data') and call['request']['postData'][
                'text'].__contains__('installationID'):
                if json.loads(call['request']['postData']['text'])['installationID'] not in product_info.keys():
                    product_info[json.loads(call['request']['postData']['text'])['installationID']] = Product(
                        json.loads(call['request']['postData']['text'])['installationID'],
                        json.loads(call['request']['postData']['text'])['productpatch'],
                        json.loads(call['request']['postData']['text'])['productversion'],
                        json.loads(call['request']['postData']['text'])['publichost'])
        return product_info

    # Not sure if the last field is needed

    def get_widgets_info(self):
        widgets = {}
        for call in self.calls:
            if call['request']['url'].__contains__('userFriendlyPerfLog'):
                facts = json.loads(call['response']['content']['text'])['fact']
                for fact in facts:
                    if fact.__contains__('widgetId'):
                        if fact['widgetId'] in widgets.keys() and fact['ttfb'] != None:
                            widgets[fact['widgetId']].widget_ttfb = fact['ttfb']
                        else:
                            widgets[fact['widgetId']] = (Widget(
                                fact['widgetId'],
                                fact['widgetType'],
                                fact['widgetName'],
                                fact['widgetDuration'],
                                datetime.strptime(fact['widgetTstamp'], "%Y-%m-%d %H:%M:%S.%f")
                            ))
        return widgets

    # сначала соьрать виджеты и все остальное, потом вызвать конструктор

    def get_calls_info(self):
        calls = []
        for call in self.calls:
            tmp_stories = []
            tmp_widgets = []
            tmp_measurements = []
            tmp_runtime = 0
            if call['request']['url'].__contains__('GetResponse'):
                # Getting Story Name:
                if "ClientInfo" in json.loads(call['request']['postData']['text']).keys():
                    tmp_stories.append(
                        json.loads(call['request']['postData']['text'])['ClientInfo']['Context']['StoryName'])
                    # Getting Widget IDs
                    if "WidgetId" in json.loads(call['request']['postData']['text'])['ClientInfo']['Context'].keys():
                        for widget in json.loads(call['request']['postData']['text'])['ClientInfo']['Context'][
                            'WidgetId']:
                            widget = widget.replace('-', '')
                            if widget not in set(tmp_widgets):
                                tmp_widgets.append(widget)
                # Getting Runtime
                if 'PerformanceData' in json.loads(call['response']['content']['text']).keys():
                    tmp_runtime = json.loads(call['response']['content']['text'])['PerformanceData']['Runtime']
                    #                    call_tmp.runtime = json.loads(call['response']['content']['text'])['PerformanceData']['Runtime']
                    # Getting Measurements. Measurements is a list of dictionaries formatted like {'Description': '',
                    # 'Time': '', 'Calls': ''}
                    for measure in json.loads(call['response']['content']['text'])['PerformanceData']['Measurements']:
                        tmp_measurements.append(measure)
            #                    call_tmp.measurements = measurements
            call_tmp = Call(url=call['request']['url'],
                            start_timestamp=call['startedDateTime'],
                            total_time=call['time'],
                            body_size=call['request']['bodySize'],
                            resource_type=call['_resourceType'],
                            status=call['response']['status'],
                            transfer_size=call['response']['_transferSize'],
                            timings=utils.check_time(call['timings']),
                            stories=tmp_stories,
                            widgets=tmp_widgets,
                            runtime=tmp_runtime,
                            measurements=tmp_measurements)
            calls.append(call_tmp)
            del call_tmp
        return calls


# Export Part

test_analysis = StoryAnalyzer(settings.HAR_PATH)
test_analysis.read_har_file()
test_calls = test_analysis.get_calls_info()
test_products = test_analysis.get_product_info()
test_widgets = test_analysis.get_widgets_info()
test_story = test_analysis.get_story_info_2()

story_runtime = utils.get_story_runtime_data(test_calls)
story_summary = utils.get_story_summary(test_calls)
widgets_frame = utils.get_widget_frame(test_widgets)

product_frame = utils.get_product_frame(test_products)
story_frame = utils.get_story_frame(test_story)
story_product_frame = pd.concat((product_frame, story_frame))

with pd.ExcelWriter('story_tables_generated.xlsx', mode='A') as writer:
    story_runtime.to_excel(writer, sheet_name='story_runtime')
    story_summary.to_excel(writer, sheet_name='story_metadata')
    story_product_frame.to_excel(writer, sheet_name='general_info')
    widgets_frame.to_excel(writer, sheet_name='widget_runtime')

writer.save()

#
# widget_info = test_analysis.get_widgets_info()
# print(get_widget_frame(widget_info))
#
calls_test = test_analysis.get_calls_info()
widgets_test = test_analysis.get_widgets_info()
for call in calls_test:
    if call.measurements:
        print(call.url)
        measurements = pd.DataFrame(i for i in call.measurements)
        datatabulate = lambda data: tabulate(measurements, headers='keys', tablefmt='psql')
        print(datatabulate(measurements))
    if call.widgets:
        for i in call.widgets:
            print((i))
            if i in widgets_test.keys():
                print(widgets_test[i].widget_name, widgets_test[i].widget_duration)
            widgets = pd.DataFrame((i for i in call.widgets), columns=['Widget ID'])
            datatabulate = lambda data: tabulate(widgets, headers='keys', tablefmt='psql')
            print(datatabulate(widgets))

# datatabulate = lambda data: tabulate(data, headers='keys', tablefmt='psql')
# print(datatabulate(data))
#

# ##\\табличка со стори инфой//
#
# data_story = pd.DataFrame([[i.story_id] for i in test_analysis.get_story_info().values()], columns = ['Story ID'])
# data_story['Story Name'] = pd.DataFrame([[i.story_name] for i in test_analysis.get_story_info().values()])
# data_story['Story Timestamp'] = pd.DataFrame([[i.story_timestamp] for i in test_analysis.get_story_info().values()])
#
# datatabulate = lambda data: tabulate(data_story, headers='keys', tablefmt='psql')
# print(datatabulate(data_story))
