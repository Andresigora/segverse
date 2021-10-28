import yaml


def load_segmentation(id):
    segmentation_path = 'segmentations/{}.yaml'.format(id)
    return _load_yaml_file(segmentation_path)


def _load_yaml_file(file_path):
    with open(file_path, 'r') as f:
        yml = yaml.safe_load(f)
    return yml