# Side functions for getting Dataframes from objects lists

import pandas as pd
import numpy as np
import statistics

def get_story_runtime_data(calls):
    columns = ['URL', 'Start Timestamp', 'Total Time', 'Runtime', 'Body Size', 'Resource Type', 'Status',
               'Transfer Size']
    story_runtime_data = pd.DataFrame([i.url, i.start_timestamp, i.total_time, i.runtime, i.body_size, i.resource_type,
                                       i.status, i.transfer_size] for i in calls)
    story_runtime_data.index = np.arange(1, len(story_runtime_data) + 1)
    story_runtime_data.columns = columns
    timings = pd.DataFrame(i.timings for i in calls)
    timings.index = np.arange(1, len(timings) + 1)
    story_runtime_data = pd.concat((story_runtime_data, timings), axis=1)
    return story_runtime_data


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
        sum_data[key] = sum(map(lambda x: x[key] / 1000, timings_list))
        min_data[key] = min(filter(lambda x: x != 0, map(lambda x: x[key] / 1000, timings_list)))
        max_data[key] = max(filter(lambda x: x != 0, map(lambda x: x[key] / 1000, timings_list)))
        avg_data[key] = statistics.mean(filter(lambda x: x != 0, map(lambda x: x[key] / 1000, timings_list)))
    story_summary = pd.DataFrame({**pd.DataFrame(sum_data, index=['total_runtime']).T,
                                  **pd.DataFrame(avg_data, index=['average_runtime']).T,
                                  **pd.DataFrame(min_data, index=['minimum_runtime']).T,
                                  **pd.DataFrame(max_data, index=['maximum_runtime']).T})
    return story_summary


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


def get_widget_frame(widget_info):
    columns = ['Widget Id', 'Widget Type', 'Widget Name', 'Time To First Byte', 'Widget Duration', 'Widget Timestamp']
    if widget_info == {}:
        widget_frame = pd.DataFrame(columns=columns)
    else:
        widget_frame = pd.DataFrame([widget.widget_id, widget.widget_type, widget.widget_name,
                                     widget.widget_ttfb, widget.widget_duration, widget.widget_timestamp] for widget in
                                     widget_info.values())
        widget_frame.columns = columns
    return widget_frame

# Function for checking right timings (excluding -1)


def check_time(timings):
    timings_res = {}
    for time in timings:
        if  timings[time] != -1:
            timings_res[time] = timings[time]
        else:
            timings_res[time] = 0

    return timings_res