import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from make_us_state_boundry_map import make_state_outlines_dictionary

#  Loading data
household_income_us_path = "/Users/leoparsons/.cache/kagglehub/datasets/goldenoakresearch/" \
                        "us-household-income-stats-geo-locations/versions/8/kaggle_income.csv"

state_bounds_json = "/Users/leoparsons/Downloads/us-state-boundaries.json"
us_state_boundaries = pd.read_json(state_bounds_json)
state_boundaries = make_state_outlines_dictionary(us_state_boundaries)

world_cities_path = "/Users/leoparsons/.cache/kagglehub/datasets/juanmah/world-cities/versions/8/worldcities.csv"

world_cities_df = pd.read_csv(world_cities_path)
print(list(world_cities_df))
world_cities_df["scaled_population"] = world_cities_df["population"]/max(world_cities_df["population"])

world_cities_df_with_population = world_cities_df.dropna(axis=0, subset=["scaled_population"])

all_states = list(world_cities_df_with_population[(world_cities_df_with_population["country"].isin(["United States"]))]["admin_name"])
all_states = set(all_states)
lower_48 = all_states
lower_48.remove("Alaska")
lower_48.remove("Hawaii")
lower_48 = list(lower_48)

us_cities = world_cities_df_with_population[(world_cities_df_with_population["country"].isin(["United States"])) &
                                            world_cities_df_with_population["admin_name"].isin(lower_48)]


def make_summed_bins(dataframe: pd.DataFrame, column_to_bin: str, column_to_sum: str, number_of_bins: int):
    summed_bins = {}
    bin_spacing = (max(dataframe[column_to_bin]) - min(dataframe[column_to_bin])) / number_of_bins
    lower_bound = min(dataframe[column_to_bin])
    cities = []
    for i in range(number_of_bins):
        upper_bound = lower_bound + bin_spacing
        subset_of_df = dataframe[(dataframe[column_to_bin] >= lower_bound) & (dataframe[column_to_bin] <= upper_bound)]
        largest_value_index = subset_of_df[column_to_sum].idxmax()
        largest_value_row = subset_of_df.loc[largest_value_index]
        city_name = largest_value_row["city"]
        cities.append(city_name)
        sum = subset_of_df[column_to_sum].sum()
        summed_bins[i] = [round((upper_bound + lower_bound)/2, 2), sum]
        lower_bound = upper_bound
    return summed_bins, cities


def remove_axis_ticks(axis_name):
    ax[axis_name].set_xticks([])
    ax[axis_name].set_yticks([])


summed_bins_lat, lat_cities = make_summed_bins(us_cities, "lat", "population", 50)
summed_bins_lat_df = pd.DataFrame.from_dict(summed_bins_lat, orient="index", columns=["lat", "sum_population"])
summed_bins_lng, lng_cities = make_summed_bins(us_cities, "lng", "population", 50)
summed_bins_lng_df = pd.DataFrame.from_dict(summed_bins_lng, orient="index", columns=["lng", "sum_population"])


fig, ax = plt.subplot_mosaic([["plot_2", "plot_2", "text_1"],
                              ["world_map", "world_map", "plot_1"],
                              ["world_map", "world_map", "plot_1"],
                              ["world_map", "world_map", "plot_1"],
                              ],
                             figsize=(14, 8))

x_upper_limit = max(us_cities["lng"]) * 1 / 1.05
x_lower_limit = min(us_cities["lng"]) * 1.05

y_upper_limit = max(us_cities["lat"]) * 1.05
y_lower_limit = min(us_cities["lat"]) * 1/1.05

# plotting the data
ax["world_map"].scatter(x=us_cities["lng"], y=us_cities["lat"], s=us_cities["scaled_population"] * 100,
           c=us_cities["population"], cmap="Greens", vmin=0, vmax=1)

plot_1_container = sns.barplot(data=summed_bins_lat_df, x="sum_population", y="lat", native_scale=True, orient="y",
                               ax=ax["plot_1"], hue="sum_population", legend=False, palette="Greens")

plot_2_container = sns.barplot(data=summed_bins_lng_df, x="lng", y="sum_population", native_scale=True, ax=ax["plot_2"],
                               hue="sum_population", legend=False, palette="Greens")

ax["text_1"].text(x=0.5, y=0.5, s="population density by latitude and longitude",
                  ha="center", va="center")
ax["text_1"].set_frame_on(False)
remove_axis_ticks("text_1")

# making sure axis are all equal
ax["world_map"].set_xlim(x_lower_limit, x_upper_limit)
ax["world_map"].set_ylim(y_lower_limit, y_upper_limit)
ax["plot_1"].set_ylim(y_lower_limit, y_upper_limit)
ax["plot_2"].set_xlim(x_lower_limit, x_upper_limit)

ax["world_map"].grid(ls="--", c="#dae6da", visible=True)
ax["plot_1"].grid(ls="--", c="#dae6da", visible=True, axis="y")
ax["plot_2"].grid(ls="--", c="#dae6da", visible=True, axis="x")

# labeling axis
ax["plot_1"].tick_params(labelbottom=False, labelleft=False)
ax["plot_2"].tick_params(labelbottom=False, labelleft=False)

ax["world_map"].set_ylabel("latitude")
ax["world_map"].set_xlabel("longitude")

ax["plot_1"].set_ylabel("")
ax["plot_2"].set_xlabel("")


# for i in range(len(plot_1_container.containers)):
#     ax["plot_1"].bar_label(plot_1_container.containers[i], labels=lat_cities[i])
#     ax["plot_2"].bar_label(plot_2_container.containers[i], labels=lng_cities[i])

ax["plot_1"].set_xlabel("relative_population")
ax["plot_2"].set_ylabel("relative_population")

for k in state_boundaries:
    lng = state_boundaries[k][0]
    lat = state_boundaries[k][1]
    ax["world_map"].plot(lng, lat, c="black", ls="-", lw=0.2)

plt.savefig('/Users/leoparsons/Desktop/Coding_Projects/Data Visualization Examples/make_us_state_boundry_map.png')
plt.show()
