import json

def radar_bbox(radar_id, radar_product):
    json_bbox = json.load(open('./radar_bbox.json'))
    return json_bbox[radar_id]['bounding_coords'][f'{radar_id}_{radar_product}']