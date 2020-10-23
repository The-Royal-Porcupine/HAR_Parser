# Side functions for getting Dataframes from objects lists

import pandas as pd
import numpy as np
import statistics
from datetime import datetime, timedelta

import objects

# Dataframe for Widgets from Contentlib (all used in Story)
# All widgets existing in Story (from ContentLib)


def get_widgets_from_contentlib_frame(widgets):
    columns = ['Story Name', 'Page Title', 'Widget Class', 'Widget ID', 'Widget Title']
    if not widgets:
        widgets_from_contentlib_frame = pd.DataFrame(columns=columns)
    else:
        widgets_from_contentlib_frame = pd.DataFrame([i.story_entity_name, i.page_title, i.widget_class, i.widget_id, i.widget_title]
                                                     for i in widgets)
        widgets_from_contentlib_frame.index = np.arange(1, len(widgets_from_contentlib_frame) + 1)
        widgets_from_contentlib_frame.columns = columns
    return widgets_from_contentlib_frame

# Dataframe for Widgets from Events (Executed by opening pages of story) and Dataframe for Gantt Chart of all widgets
# [0] - Get Events Widgets Frame
# [1] - Get Frame for Gantt Chart with All Widgets Timeline


def get_widgets_from_events_frame(widgets):
    columns_widgets_table = ['Widget ID', 'Type', 'Title', 'Duration', 'Widget Start Time', 'Widget Finish Time', 'User Action', 'User Action Start Time']
    columns_widgets_gantt = ['Widget ID', 'Label', 'Widget Start', 'Widget Duration', 'Widget Finish', 'User Action', 'User Action Start']
    widgets_gantt_frame = pd.DataFrame()

    if not widgets:
        get_widgets_from_events_frame = pd.DataFrame(columns=columns_widgets_table)
    else:
        get_widgets_from_events_frame = pd.DataFrame()
        for user_action in widgets:
            # As Is (in str) put in first dataframe
            get_widgets_from_events_frame_tmp = pd.DataFrame([widget.widget_id, widget.widget_type,
                                                          widget.widget_name, widget.widget_duration,
                                                          widget.widget_timestamp, widget.widget_finish_timestamp,
                                                          widget.user_action, widget.user_action_timestamp] for widget in widgets[user_action])
            get_widgets_from_events_frame = pd.concat([get_widgets_from_events_frame, get_widgets_from_events_frame_tmp], ignore_index=True)

            # For Gantt we need timestamps
            for widget in widgets[user_action]:
                widget_start_time = datetime.strptime(widget.widget_timestamp, '%Y-%m-%d %H:%M:%S.%f')
                widget_finish_time = datetime.strptime(widget.widget_finish_timestamp, '%Y-%m-%d %H:%M:%S.%f')
                widget_duration = widget_finish_time - widget_start_time
                widget_start_time_time = datetime.strptime(widget_start_time.strftime('%H:%M:%S.%f'), '%H:%M:%S.%f')
                widget_finish_time_time = datetime.strptime(widget_finish_time.strftime('%H:%M:%S.%f'), '%H:%M:%S.%f')
                widget_duration_time = datetime.strptime(str(widget_duration), '%H:%M:%S.%f')
                user_action_start = datetime.strptime(widget.user_action_timestamp, '%Y-%m-%d %H:%M:%S.%f')
                user_action_start_time = datetime.strptime(user_action_start.strftime('%H:%M:%S.%f'), '%H:%M:%S.%f')
                widget_label = widget.widget_type + ' (' + widget.widget_name + ')'
                widgets_gantt_frame = widgets_gantt_frame.append([[widget.widget_id,
                                                                   widget_label, widget_start_time_time,
                                                                   widget_duration_time, widget_finish_time_time,
                                                                   widget.user_action, user_action_start_time]])
        get_widgets_from_events_frame.index = np.arange(1, len(get_widgets_from_events_frame) + 1)
        get_widgets_from_events_frame.columns = columns_widgets_table
        widgets_gantt_frame.index = np.arange(1, len(widgets_gantt_frame) + 1)
        widgets_gantt_frame.columns = columns_widgets_gantt

    return get_widgets_from_events_frame, widgets_gantt_frame

# Dataframe for Widgets from MDS/Batch Requests = result[0]
# And DataFrame for Gantt Chart - MDS + Widgets Timeframes = result[1]


def get_widgets_from_mds_frame(calls, widgets):
    import HAR_Analysis
    columns_wfm = ['Widget Type', 'Widget Title', 'Widget Duration', 'Widget Started', 'Widget Finished', 'MDS Number',
               'HTTP', 'MDS Time', 'TTFB (Wait)', 'TTFB - MDS', 'User Action']
    columns_gantt = ['MDS Number', 'Start Mark', 'Before MDS Duration', 'MDS Duration', 'After MDS Duration', 'User Action']
    get_widgets_from_mds_frame = pd.DataFrame()
    widgets_and_mds_runtime_frame = pd.DataFrame()
    mds_number = 1
    for call in calls:
        if isinstance(call, objects.Call_2):
            if call.get_response_type == 'Batch' and call.widgets != {}:
                for id in call.widgets:
                    for user_action in widgets:
                        try: widget = next((x for x in widgets[user_action] if x.widget_id == id))
                        except StopIteration: continue
                        if widget != None:
                         # Возможно, временная мера из-за файлов, где МДСы начинаются раньше виджетов

                            widget_start_time = datetime.strptime(widget.widget_timestamp, '%Y-%m-%d %H:%M:%S.%f')
                            mds_start_time = datetime.strptime(call.start_timestamp, '%Y-%m-%d %H:%M:%S.%f')
                            widget_finish_time = datetime.strptime(widget.widget_finish_timestamp, '%Y-%m-%d %H:%M:%S.%f')
                            mds_finish_time = datetime.strptime(call.start_timestamp, '%Y-%m-%d %H:%M:%S.%f') + timedelta(seconds=float(call.total_time))
                            if mds_start_time >= widget_start_time and mds_finish_time <= widget_finish_time:
                                get_widgets_from_mds_frame = get_widgets_from_mds_frame.append([[widget.widget_type, widget.widget_name,
                                                                            widget.widget_duration, widget.widget_timestamp,
                                                                            widget.widget_finish_timestamp, mds_number,
                                                                            call.total_time, call.runtime, round(call.timings['wait'], 3),
                                                                            round(call.timings['wait'] - call.runtime, 3), widget.user_action]], ignore_index=True)

                                # For Gantt Chart. 1. Widget Start Mark
                                widget_start_time_time = datetime.strptime(widget_start_time.strftime('%H:%M:%S.%f'), '%H:%M:%S.%f')
                                # 2. MDS_Start(call.start_timestamp = call['startedDateTime']) - Widget_Start
                                before_widget_delta = mds_start_time - widget_start_time
                                before_widget_time = datetime.strptime(str(before_widget_delta), '%H:%M:%S.%f')
                                # 3. Widget_End - MDS_End (MDS_Start + MDS_Runtime (call['total_time']))
                                after_widget_delta = widget_finish_time - mds_finish_time
                                after_widget_time = datetime.strptime(str(after_widget_delta), '%H:%M:%S.%f')
                                # 4. MDS Label
                                mds_label = f'MDS {mds_number} ({call.get_response_type})'
                                # 5. MDS Duration
                                mds_duration_time = datetime.strptime(datetime.strptime(call.total_time, '%S.%f').strftime('%H:%M:%S.%f'),
                                                  '%H:%M:%S.%f')

                                widgets_and_mds_runtime_frame = widgets_and_mds_runtime_frame.append([[mds_label,
                                                                                                       widget_start_time_time,
                                                                                                       before_widget_time,
                                                                                                       mds_duration_time,
                                                                                                       after_widget_time,
                                                                                                       widget.user_action]])
                            else: continue
                mds_number = mds_number+1
    get_widgets_from_mds_frame.columns = columns_wfm
    get_widgets_from_mds_frame.index = np.arange(1, len(get_widgets_from_mds_frame) + 1)
    widgets_and_mds_runtime_frame.columns = columns_gantt
    widgets_and_mds_runtime_frame.index = np.arange(1, len(widgets_and_mds_runtime_frame) + 1)
    return get_widgets_from_mds_frame, widgets_and_mds_runtime_frame

# Dataframe for Product information


def get_product_frame(product_info):
    columns = ['Product Host', 'Product Patch', 'Product Version', 'Product Installation ID']
    if product_info == {}:
        product_frame = pd.DataFrame(columns=columns)
    else:
        product_frame = pd.DataFrame([product.product_host, product.product_patch, product.product_version,
                                      product.product_installationid] for product in product_info.values())
        product_frame.columns = columns
        product_frame = product_frame.T
    return product_frame

# Dataframe for Story information


def get_story_frame(story_info):
    columns = ['Story ID', 'Story Name', 'Story Description', 'Story Modified Time', 'Story Modified By',
               'Story Created Time', 'Story Created By']
    if story_info == {}:
        story_frame = pd.DataFrame(columns=columns)
    else:
        story_frame = pd.DataFrame([story.story_id, story.story_name, story.story_description,
                                      story.story_modifiedtime, story.story_modifiedby, story.story_createdtime,
                                      story.story_createdby] for story in story_info.values())
        story_frame.columns = columns
        story_frame = story_frame.T
    return story_frame

# Dataframe for PieCharts with Calls Summary
# Get Calls Summary (for PieCharts)


def get_story_summary(calls):
    timings_list = []
    for call in calls:
        timings_list.append(call.timings)
    sum_data = {"blocked": [0], "_blocked_queueing": [0], "dns": [0], "connect": [0], "send": [0], "wait": [0],
                "receive": [0], "ssl": [0]}
    min_data = {"blocked": [0], "_blocked_queueing": [0], "dns": [0], "connect": [0], "send": [0], "wait": [0],
                "receive": [0], "ssl": [0]}
    max_data = {"blocked": [0], "_blocked_queueing": [0], "dns": [0], "connect": [0], "send": [0], "wait": [0],
                "receive": [0], "ssl": [0]}
    avg_data = {"blocked": [0], "_blocked_queueing": [0], "dns": [0], "connect": [0], "send": [0], "wait": [0],
                "receive": [0], "ssl": [0]}
    for key in sum_data.keys():
        sum_data[key] = sum(map(lambda x: x[key], timings_list))
        min_data[key] = min(filter(lambda x: x != 0, map(lambda x: x[key], timings_list)))
        max_data[key] = max(filter(lambda x: x != 0, map(lambda x: x[key], timings_list)))
        avg_data[key] = statistics.mean(filter(lambda x: x != 0, map(lambda x: x[key], timings_list)))
    story_summary = pd.DataFrame({**pd.DataFrame(sum_data, index=['total_runtime']).T,
                                  **pd.DataFrame(avg_data, index=['average_runtime']).T,
                                  **pd.DataFrame(min_data, index=['minimum_runtime']).T,
                                  **pd.DataFrame(max_data, index=['maximum_runtime']).T})
#    float_format = lambda x: "{:,.2f}".format(x)
#    story_summary.apply(float_format)
    return story_summary

# Create table with MDS Timings for MDS Call (MDS Details Slides)


def get_mds_timings_frame(call_2, index):
    columns = ['MDS Index', 'HTTP Runtime', 'MDS Runtime', 'Wait Time', 'Wait - MDS', 'Send', 'Receive', 'Block']
    get_mds_timings_frame = pd.DataFrame([[str(index), call_2.total_time, call_2.runtime, round(call_2.timings['wait'], 3),
                                          round((call_2.timings['wait']-call_2.runtime),3), round(call_2.timings['send'], 3),
                                          round(call_2.timings['receive'], 3), round(call_2.timings['blocked'], 3)]])
    get_mds_timings_frame.columns = columns
    get_mds_timings_frame = get_mds_timings_frame.T
    return get_mds_timings_frame

# Create table with views info


def get_view_info_table(call_2):
    columns = ['View', 'Name', 'Type', 'Cache', 'Runtime']
    get_view_info_table = pd.DataFrame([ds.view, ds.ds_name, ds.ds_type, ds.ds_cache,
                                        ds.ds_runtime] for ds in call_2.datasources)
    get_view_info_table.index = np.arange(1, len(get_view_info_table) + 1)
    get_view_info_table.columns = columns
    return get_view_info_table

# Dataframe for Calculation Entities in Appendix


def get_calc_entities_frame(calc_entities):
    columns = ['Calculation Entity ID', 'Name', 'Type']
    calc_entities_frame = pd.DataFrame([ce.id, ce.name, ce.type] for ce in calc_entities)
    calc_entities_frame.index = np.arange(1, len(calc_entities_frame) + 1)
    calc_entities_frame.columns = columns
    return calc_entities_frame

# Formatting time to '%Y-%m-%d %H:%M:%S.%f' 3 digits


def format_time(t):
    if t.microsecond % 1000 >= 500:  # check if there will be rounding up
        t = t + timedelta(milliseconds=1)  # manually round up
    return t.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

# Function for checking right timings (excluding -1)


def check_time(timings):
    timings_res = {}
    for time in timings:
        if  timings[time] != -1:
            timings_res[time] = round(float(timings[time]), 3)
        else:
            timings_res[time] = 0

    return timings_res

# Check widget type - short name


def check_widget_type(widget_type):
    if widget_type.__contains__('Text'): widget_type = 'Text'
    elif widget_type.__contains__('Shape'): widget_type = 'Shape'
    elif widget_type.__contains__('Infochart'): widget_type = 'Infochart'
    elif widget_type.__contains__('PageFilter'): widget_type = 'PageFilter'
    elif widget_type.__contains__('CalcInputControl'): widget_type = 'CalcInputControl'
    elif widget_type.__contains__('DynamicTable'): widget_type = 'DynamicTable'
    elif widget_type.__contains__('Image'): widget_type = 'Image'
    return widget_type





# def get_story_runtime_data(calls):
#     import HAR_Analysis
#     columns = ['URL', 'Start Timestamp', 'Total Time', 'Body Size', 'Resource Type', 'Status',
#                'Transfer Size']
#     story_runtime_data = pd.DataFrame([i.url, i.start_timestamp, i.total_time, i.body_size, i.resource_type,
#                                        i.status, i.transfer_size] for i in calls)
#     story_runtime_data.index = np.arange(1, len(story_runtime_data) + 1)
#     story_runtime_data.columns = columns
#     story_runtime_data['Get Response Type'] = [i.get_response_type if isinstance(i, HAR_Analysis.Call_2) else '' for i in calls]
#     story_runtime_data['Runtime'] = [i.runtime if isinstance(i, HAR_Analysis.Call_2) else 0 for i in calls]
#     story_runtime_data['URL'] = story_runtime_data['URL'].apply(lambda x: check_name_url(x))
#     timings = pd.DataFrame(i.timings for i in calls)
#     timings.index = np.arange(1, len(timings) + 1)
#     story_runtime_data = pd.concat((story_runtime_data, timings), axis=1)
#     return story_runtime_data
#
#
# #self.timings = {k: float('{:,.2f}'.format(v/1000)) for k, v in timings.items()}
#
#
# def get_widget_frame(widget_info):
#     columns = ['Widget Id', 'Widget Type', 'Widget Name', 'Time To First Byte', 'Widget Duration', 'Widget Start Timestamp',
#                'Widget Finish Timestamp']
#     if widget_info == {}:
#         widget_frame = pd.DataFrame(columns=columns)
#     else:
#         widget_frame = pd.DataFrame([widget.widget_id, widget.widget_type, widget.widget_name,
#                                      widget.widget_ttfb, widget.widget_duration, widget.widget_timestamp,
#                                      widget.widget_finish_timestamp] for widget in
#                                      widget_info.values())
#         widget_frame.columns = columns
#     return widget_frame
#
#
# def get_common_widget_frame(widget_info):
#     columns = ['Story Entity ID', 'Story Name', 'Page Title', 'Widget Id', 'Widget Class',
#                'Widget Title', 'Widget Type', 'Widget Name', 'Time To First Byte',
#                'Widget Duration', 'Widget Timestamp']
#     if widget_info == {}:
#         widget_frame = pd.DataFrame(columns=columns)
#     else:
#         widget_frame = pd.DataFrame([widget.story_entity_id, widget.story_entity_name, widget.page_title,
#                                      widget.widget_id, widget.widget_class, widget.widget_title,
#                                      widget.widget_type, widget.widget_name, widget.widget_ttfb,
#                                      widget.widget_duration, widget.widget_timestamp] for widget in
#                                      widget_info.values())
#         widget_frame.columns = columns
#     return widget_frame
#
#
# def get_response_frames(call, widgets):
#     frames = []
#     measurements = pd.DataFrame(i for i in call.measurements)
#     columns = ['Start Timestamp', 'Total Time', 'Runtime', 'Body Size', 'Status', 'Transfer Size']
#     widget_columns = ['Story Name', 'Page Title', 'Widget ID', 'Widget Class', 'Widget Title',
#                       'Widget Name', 'Widget TTFB' ]
#     call_info = pd.DataFrame([[call.start_timestamp, call.total_time, call.runtime, call.body_size, call.status, call.transfer_size]], columns=columns)
#     timings = pd.DataFrame([call.timings])
#     timings.index = np.arange(1, len(timings) + 1)
#     widget_info = pd.DataFrame()
#     for id in call.widgets:
#         if id in widgets.keys():
#             widget_info = pd.DataFrame([[widgets[id].story_entity_name, widgets[id].page_title,
#                                         widgets[id].widget_id, widgets[id].widget_class,
#                                         widgets[id].widget_title, widgets[id].widget_name, widgets[id].widget_ttfb]], columns=widget_columns)
#             widget_info = widget_info.fillna(0)
#             widget_info.index = np.arange(1, len(widget_info) + 1)
#     call_info.index = np.arange(1, len(call_info) + 1)
#     get_response_data = pd.concat((call_info, widget_info), axis=1)
#     get_response_data = pd.concat((get_response_data, timings), axis=1)
#     frames.append(measurements)
#     frames.append(get_response_data)
#     return frames
#
#
# def check_name_url(url):
#     if   url.find('contentlib')!=-1: url = 'Content Library'
#     elif url.find('Pusher')!=-1: url = 'Pusher'
#     elif url.find('GetResponse') != -1: url = 'Get Response'
#     elif url.find('photo') != -1: url = 'Picture Loading'
#     elif url.find('uiAssets/img') != -1: url = 'Image Loading'
#     elif url.find('get-static-content') != -1: url = 'Static Content Loading'
#     elif url.find('inputScheduleVersions') != -1: url = 'Load Versions Info'
#     elif url.find('application/data') != -1: url = 'Get Application Data'
#     elif url.find('application/data') != -1: url = 'Get Application Data'
#     elif url.find('queryStatistics') != -1: url = 'Get Statistics'
#     elif url.find('userFriendlyPerfLog') != -1: url = 'Get User Friendly Performance Log'
#     elif url.find('commenting') != -1: url = 'Get Comments'
#     elif url.find('fonts') != -1: url = 'Fonts Uploading'
#     elif url.find('commenting') != -1: url = 'Get Comments'
#     elif url.find('indexeddb.worker') != -1: url = 'Scripts or Something'
#     return url
#
#




