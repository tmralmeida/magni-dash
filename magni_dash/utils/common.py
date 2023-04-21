from typing import Dict


def get_mapping_cols(element: str, marker_id: str, sep: str) -> Dict:
    return {
        element + sep + marker_id + " " + "X": "X (m)",
        element + sep + marker_id + " " + "Y": "Y (m)",
        element + sep + marker_id + " " + "Z": "Z (m)",
        element + sep + marker_id + " " + "speed (m/s)": "speed (m/s)",
    }
