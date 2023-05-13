from typing import Dict
from collections import namedtuple


GroupsInfo = namedtuple("GroupsInfo", ["element_id", "markers_pattern_re", "label_sep"])


def get_mapping_cols(element: str, marker_id: str, sep: str) -> Dict:
    return {
        element + sep + marker_id + " " + "X": "X (m)",
        element + sep + marker_id + " " + "Y": "Y (m)",
        element + sep + marker_id + " " + "Z": "Z (m)",
        element + sep + marker_id + " " + "speed (m/s)": "speed (m/s)",
    }


def get_mapping_cols_tobii(element: str, element_number: str, sep: str) -> Dict:
    return {
        element + sep + element_number + "_G3D_X": "TB_G3D X (m)",
        element + sep + element_number + "_G3D_Y": "TB_G3D Y (m)",
        element + sep + element_number + "_G3D_Z": "TB_G3D Z (m)",
    }


def get_mapping_cols_centroids(element: str, element_number: str, sep: str) -> Dict:
    return {
        element + sep + element_number + " " + "Centroid_X": "Centroid X (m)",
        element + sep + element_number + " " + "Centroid_Y": "Centroid Y (m)",
        element + sep + element_number + " " + "Centroid_Z": "Centroid Z (m)",
    }
