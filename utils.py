import os

import pandas as pd
import yaml

ENTITY_MAP = {
    "account": "account_id",
    "merchant": "merchant_id",
    "driver": "driver_id",
    "item": "catalog_item_id"
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
    return [f.strip('.yaml') for f in filenames]


def load_segmentation_data(id, entity_col, segmentation_column):
    segmentation_path = 'data/{}.csv'.format(id)
    df = pd.read_csv(segmentation_path)
    return df[[entity_col, segmentation_column]]