import os
import re

import pandas as pd
import yaml

from connectors import CREDENTIALS, SEGMENTATION_SCHEMA, BigQueryConnector

ENTITY_MAP = {
    "account": "account_id",
    "merchant": "merchant_id",
    "driver": "driver_id",
    "item": "item_id"
}


def load_segmentation(id):
    segmentation_path = 'segmentations/{}.yaml'.format(id)
    return _load_yaml_file(segmentation_path)


def _load_yaml_file(file_path):
    with open(file_path, 'r') as f:
        yml = yaml.safe_load(f)
    return yml


def list_files(folder):
    filenames = next(os.walk(folder), (None, None, []))[2]
    return [re.sub(r'.yaml', '', f) for f in filenames]


def list_segmentations(entity, folder='segmentations'):
    segmentation_files = list_files(folder)
    entity_files = []
    for id in segmentation_files:
        segmentation = load_segmentation(id)
        if segmentation["entity"] == entity:
            entity_files.append(id)
    return entity_files


def load_segmentation_data(id, entity_col, segmentation_column):
    table_name = id.replace("-", "_")
    conn = BigQueryConnector(credentials=CREDENTIALS, segmentation_schema=SEGMENTATION_SCHEMA)
    return conn.get_segmentation(table_name, entity_col, segmentation_column)