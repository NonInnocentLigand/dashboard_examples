import pandas as pd

state_bounds_json = "/Users/leoparsons/Downloads/us-state-boundaries.json"

us_state_boundaries = pd.read_json(state_bounds_json)

lower_48 = ['Maryland', 'Nevada', 'Iowa', 'Kansas', 'Oregon', 'Georgia', 'Montana', 'Michigan', 'North Dakota',
            'Pennsylvania', 'District of Columbia', 'Texas', 'Florida', 'Arkansas', 'New Hampshire', 'California',
            'Rhode Island', 'New Mexico', 'Massachusetts', 'Wyoming', 'New Jersey', 'Virginia', 'Arizona', 'Louisiana',
            'South Carolina', 'Missouri', 'West Virginia', 'Indiana', 'Maine', 'Illinois', 'Wisconsin', 'New York',
            'Minnesota', 'Washington', 'Ohio', 'Delaware', 'Connecticut', 'Kentucky', 'South Dakota', 'North Carolina',
            'Vermont', 'Oklahoma', 'Utah', 'Alabama', 'Tennessee', 'Nebraska', 'Idaho', 'Mississippi', 'Colorado']


def get_coord_vectors(list_of_cords):
    lng = []
    lat = []
    for coordinates in list_of_cords:
        if len(coordinates) != 2:  # this catches some inconsistencies in the st_asgeojson data
            for sub_coordinates in coordinates:
                lng.append(sub_coordinates[0])
                lat.append(sub_coordinates[1])
        else:
            lng.append(coordinates[0])
            lat.append(coordinates[1])
    return lng, lat


def make_state_outlines_dictionary(us_state_boundaries: pd.DataFrame):
    state_outlines_dictionary = {}
    index = 0
    for row in us_state_boundaries.itertuples():
        state_1_geojson = us_state_boundaries.st_asgeojson.loc[index]
        if row[5] in lower_48:
            lat, lng = get_coord_vectors(state_1_geojson["geometry"]["coordinates"][0])
            state_outlines_dictionary[row[5]] = (lat, lng)
        index += 1

    return state_outlines_dictionary

