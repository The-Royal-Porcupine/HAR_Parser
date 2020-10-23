#  Import section

import json
from datetime import datetime, date
from datetime import timedelta
import re
from bs4 import BeautifulSoup

import objects
import utils


# Functional class

class StoryAnalyzer:

    def __init__(self, path):
        self.file_path = path
        self.calls = self.read_har_file()

    def read_har_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            har_parser = json.loads(f.read())
            return har_parser['log']['entries']

    def get_story_info_2(self):
        story_info = {}
        for call in self.calls:
            if call['request']['url'].__contains__('contentlib'):
                address_of_info = json.loads(call['response']['content']['text'])
                if isinstance(json.loads(call['response']['content']['text']), list):
                    continue
                elif "resource" in json.loads(call['response']['content']['text']).keys():
                    story_tmp = objects.Story(story_id=address_of_info['resource']['resourceId'],
                                        story_name=address_of_info['resource']['name'],
                                        story_description=address_of_info['resource']['description'],
                                        story_createdby=address_of_info['resource']['createdByDisplayName'],
                                        story_createdtime=address_of_info['resource']['createdTime'],
                                        story_modifiedby=address_of_info['resource']['modifiedByDisplayName'],
                                        story_modifiedtime=address_of_info['resource']['modifiedTime'])
                    story_info[address_of_info['resource']['resourceId']] = story_tmp
                elif "resourceId" in json.loads(call['response']['content']['text']).keys():
                    story_tmp = objects.Story(story_id=address_of_info['resourceId'],
                                        story_name=address_of_info['name'],
                                        story_description=address_of_info['description'],
                                        story_createdby=address_of_info['createdBy'],
                                        story_createdtime=address_of_info['createdTime'],
                                        story_modifiedby=address_of_info['modifiedBy'],
                                        story_modifiedtime=address_of_info['modifiedTime'])
                    story_info[address_of_info['resourceId']] = story_tmp
        return story_info

    def get_product_info(self):
        product_info = {}
        for call in self.calls:
            try:
                if call['request']['url'].__contains__('application/data') and call['request']['postData'][
                    'text'].__contains__('installationID'):
                    if json.loads(call['request']['postData']['text'])['installationID'] not in product_info.keys():
                        product_info[json.loads(call['request']['postData']['text'])['installationID']] = objects.Product(
                            json.loads(call['request']['postData']['text'])['installationID'],
                            json.loads(call['request']['postData']['text'])['productpatch'],
                            json.loads(call['request']['postData']['text'])['productversion'],
                            json.loads(call['request']['postData']['text'])['publichost'])
            except KeyError:
                continue
        return product_info

    # Widgets Info from Content Lib (all existing in a story)

    def get_widgets_contentlib_info(self):
        calls = []
        widgets = []
        tmp_calc_entities = []
        calc_entities = []
        widget_id_set = set()
        for call in self.calls:
            if call['request']['url'].__contains__('contentlib'):
                address_of_info = json.loads(call['response']['content']['text'])
                if isinstance(json.loads(call['response']['content']['text']), dict):
                    if 'cdata' in address_of_info.keys():
                        entities_address = address_of_info['cdata']['content']['entities']
                    elif 'resource' in address_of_info.keys():
                        if 'cdata' in address_of_info['resource'].keys():
                            entities_address = address_of_info['resource']['cdata']['content']['entities']
                    for entry in address_of_info:
                        for entity in entities_address:
                            if entity['type'] == 'story':
                                for page in entity['data']['pages']:
                                    for widget in page['content']['widgets']:
                                        if widget is not None:
                                            widget_id_tmp = widget['id'].replace('-', '')
                                            if widget_id_tmp not in widget_id_set:
                                                widget_id_set.add(widget_id_tmp)
                                                story_entity_id_tmp = entity['data']['id'].replace('-', '')
                                                story_entity_name_tmp = entity['data']['title']
                                                page_title_tmp = page['title']
                                                widget_class_tmp = widget['class'].split('.')[-1]
                                                if widget_class_tmp == 'InfochartVizWidget':
                                                    widget_title_tmp = \
                                                        widget['definition']['vizContent']['vizDefinition'][
                                                            'chart'][
                                                            'title'] + ' ' + \
                                                        widget['definition']['vizContent']['vizDefinition'][
                                                            'chart'][
                                                            'subTitle']
                                                    widget_title_tmp = widget_title_tmp.strip()
                                                elif widget_class_tmp == 'TextWidget':
                                                    widget_title_tmp = widget['definition']['text']
                                                    soup = BeautifulSoup(widget_title_tmp, features="lxml")
                                                    for node in soup.findAll('p'):
                                                        widget_title_tmp = node.text
                                                elif widget_class_tmp == 'DynamicTableWidget':
                                                    description_path = widget['definition']['content']['dataSource'][
                                                        '__data__']
                                                    if 'description' in description_path.keys():
                                                        widget_title_tmp = \
                                                            widget['definition']['content']['dataSource']['__data__'][
                                                                'description']
                                                    else:
                                                        widget_title_tmp = 'No title'
                                                else:
                                                    widget_title_tmp = 'No title'
                                                widget_content_lib_tmp = objects.WidgetContentLib(
                                                    story_entity_id=story_entity_id_tmp,
                                                    story_entity_name=story_entity_name_tmp,
                                                    page_title=page_title_tmp,
                                                    widget_class=widget_class_tmp,
                                                    widget_id=widget_id_tmp,
                                                    widget_title=widget_title_tmp)
                                                widgets.append(widget_content_lib_tmp)
                            if entity['type'] == 'calculation':
                                calculation_entities = entity['entities']

                                for calc_entity in calculation_entities:
                                    if calc_entity['id']['id'] not in set(tmp_calc_entities):
                                        tmp_calc_entities.append(calc_entity['id']['id'])
                                        tmp_calc_entity = objects.CalcEntity(
                                            id=calc_entity['id']['id'],
                                            name=calc_entity['name'],
                                            type=calc_entity['id']['type'])
                                        calc_entities.append(tmp_calc_entity)
                                        del tmp_calc_entity

        return widgets, calc_entities

    # Widgets Info from User Friendly Perf Log (All had been loaded)

    def get_widgets_info(self):
        widgets = {}
        for call in self.calls:
            if call['request']['url'].__contains__('userFriendlyPerfLog'):
                # Only events count for now (request of perflog), seems like response adds no new info
                # facts = json.loads(call['response']['content']['text'])['fact']
                events = json.loads(call['request']['postData']['text'])['Events'][0]['DataArray']
                for event in events:
                    try:
                        if 'marker' in event.keys():
                            tmp_widget_id = re.sub(r'.*ID: (.*)', r'\1', event['marker']).replace('-', '')
                            tmp_widget_type = re.search('Type: \w*', event['marker']).group(0).split(' ')[1]
                            tmp_widget_name_no_blanks = event['customInfo']['widgetTitle'].strip()
                            tmp_widget_name = tmp_widget_name_no_blanks[:30]+'..' if len(tmp_widget_name_no_blanks) > 30 \
                                else tmp_widget_name_no_blanks
                            tmp_widget_timestamp = datetime.strptime(event['tstamp'][:-1], '%Y-%m-%d %H:%M:%S.%f') - \
                                                   timedelta(milliseconds=round(float(event['duration']), 3))
                            tmp_widget_user_action = event['lastAction']
                            tmp_widget_user_action_timestamp = datetime.strptime(event['actionTstamp'][:-1],'%Y-%m-%d %H:%M:%S.%f')
                            tmp_widget_duration = round(float(event['duration']), 1)
                            tmp_finish_timestamp = datetime.strptime(event['tstamp'][:-1], '%Y-%m-%d %H:%M:%S.%f')
                            tmp_widget_ttfb = None
                    except KeyError:
                        pass
                    if tmp_widget_user_action not in widgets.keys():
                        widgets[tmp_widget_user_action] = []
                    if tmp_widget_id not in [x.widget_id for x in widgets[tmp_widget_user_action]]:
                        widgets[tmp_widget_user_action].append(objects.Widget(widget_id=tmp_widget_id,
                                                         widget_type=tmp_widget_type,
                                                         widget_name=tmp_widget_name,
                                                         widget_ttfb=tmp_widget_ttfb,
                                                         widget_duration=tmp_widget_duration,
                                                         widget_timestamp=tmp_widget_timestamp,
                                                         widget_finish_timestamp=tmp_finish_timestamp,
                                                         user_action=tmp_widget_user_action,
                                                         user_action_timestamp=tmp_widget_user_action_timestamp))
                    else: continue
        return widgets

    # All links' info + MDS Collecting

    def get_calls_info(self, calc_entities):
        calls = []
        for call in self.calls:
            tmp_stories = []
            tmp_widgets = []
            tmp_measurements = []
            tmp_runtime = 0
            tmp_get_response_type = ''
            tmp_ds_runtime = 0
            tmp_datasources = []

            if call['request']['url'].__contains__('GetResponse'):

                # Getting Get_Response call type: Batch/Analytics/Planning:

                if 'Metadata' in json.loads(call['request']['postData']['text']).keys():
                    tmp_get_response_type = json.loads(call['request']['postData']['text'])['Metadata']['Context']
                elif 'Planning' in json.loads(call['request']['postData']['text']).keys():
                    tmp_get_response_type = 'Planning'

                # If it is Batch, collect Views/Dimensions/DataSources/Runtime Info

                elif 'Batch' in json.loads(call['request']['postData']['text']).keys():
                    tmp_get_response_type = 'Batch'
                    batches_request = json.loads(call['request']['postData']['text'])['Batch']
                    batches_response = json.loads(call['response']['content']['text'])['Batch']
                    for batch_req in batches_request:
                        dim_members = {}
                        # DS ID only for getting runtime from response + cache info
                        tmp_ds_id = batch_req['Analytics']['DataSource']['InstanceId']
                        for batch_res in batches_response:
                            if batch_res['DataSource']['InstanceId'] == tmp_ds_id:
                                tmp_ds_runtime = round(float(batch_res['PerformanceData']['Runtime']), 3)
                                for message in batch_res['Grids'][0]['Messages']:
                                    if 'cache' in message['Text']:
                                        tmp_cache = str(message['Text']).replace(' (post process)', '')

                        # tmp_ds_type = batch_req['Analytics']['DataSource']['Type']
                        if 'Name' in batch_req['Analytics']['Definition'].keys():
                            tmp_view = batch_req['Analytics']['Definition']['Name']
                            try:
                                calc_entity = next((x for x in calc_entities if x.id == tmp_view))
                            except StopIteration:
                                continue
                            if calc_entity:
                                tmp_ds_name = calc_entity.name
                                tmp_ds_type = calc_entity.type
                        else:
                            tmp_view = 'Result Set'
                            tmp_ds_name = 'Fetching Result Set'
                            tmp_ds_type = 'Result Set'

                        dim_number = 1
                        for dimension in batch_req['Analytics']['Definition']['Dimensions']:
                            dim_name = str(dim_number) + '. ' + dimension['Name']
                            dim_number += 1
                            dim_members[dim_name] = []
                            if dimension['Axis'] == 'Columns' and 'Members' in dimension.keys():
                                for member in dimension['Members']:
                                    if 'Name' in member.keys():
                                        try: calc_entity = next((x for x in calc_entities if x.id == member['Name'].rstrip('.ID')))
                                        except StopIteration: continue
                                        if calc_entity:
                                            if tmp_view != 'Result Set': tmp_member_name = member['Name'] + ' (' + \
                                                                                           calc_entity.name + ' \ ' + \
                                                                                           calc_entity.type + ') '
                                        dim_members[dim_name].append(tmp_member_name)

                        datasource_tmp = objects.DataSource(ds_id=tmp_ds_id,
                                                            dimensions=dim_members,
                                                            ds_runtime=tmp_ds_runtime,
                                                            view=tmp_view,
                                                            ds_name=tmp_ds_name,
                                                            ds_type=tmp_ds_type,
                                                            ds_cache=tmp_cache)
                        tmp_datasources.append(datasource_tmp)
                        del datasource_tmp

                # Getting Story Name:

                if "ClientInfo" in json.loads(call['request']['postData']['text']).keys():
                    tmp_stories.append(
                        json.loads(call['request']['postData']['text'])['ClientInfo']['Context']['StoryName'])

                    # Getting Widget IDs:

                    if "WidgetId" in json.loads(call['request']['postData']['text'])['ClientInfo']['Context'].keys():
                        for widget in json.loads(call['request']['postData']['text'])['ClientInfo']['Context'][
                            'WidgetId']:
                            widget = widget.replace('-', '')
                            if widget not in set(tmp_widgets):
                                tmp_widgets.append(widget)

                # Getting Common Runtime:

                if 'PerformanceData' in json.loads(call['response']['content']['text']).keys():
                    tmp_runtime = json.loads(call['response']['content']['text'])['PerformanceData']['Runtime']

                    # Getting Measurements. Measurements is a list of dictionaries formatted like {'Description': '',
                    # 'Time': '', 'Calls': ''}

                    for measure in json.loads(call['response']['content']['text'])['PerformanceData']['Measurements']:
                        tmp_measurements.append(measure)

                # Create Call of type Get_Response:

                call_2_tmp = objects.Call_2(url=call['request']['url'],
                                    get_response_type=tmp_get_response_type,
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
                                    measurements=tmp_measurements,
                                    datasources=tmp_datasources)
                calls.append(call_2_tmp)
                del call_2_tmp

            # If it's not a Get_Response call, create a basic Call object

            else:
                call_tmp = objects.Call(url=call['request']['url'],
                                start_timestamp=call['startedDateTime'],
                                total_time=call['time'],
                                body_size=call['request']['bodySize'],
                                resource_type=call['_resourceType'],
                                status=call['response']['status'],
                                transfer_size=call['response']['_transferSize'],
                                timings=utils.check_time(call['timings']))
                calls.append(call_tmp)
                del call_tmp
        return calls





