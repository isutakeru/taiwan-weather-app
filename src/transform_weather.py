import pandas as pd

def transform_weather_data(json_data):
    location = json_data["records"]["location"][0]
    city = location["locationName"]
    elements = location["weatherElement"]
    element_dict = {e["elementName"]: e["time"] for e in elements}

    records = []
    for i in range(len(element_dict["Wx"])):
        record = {
            "City": city,
            "Start Time": element_dict["Wx"][i]["startTime"],
            "End Time": element_dict["Wx"][i]["endTime"],
            "Weather": element_dict["Wx"][i]["parameter"]["parameterName"],
            "Rain (%)": element_dict["PoP"][i]["parameter"]["parameterName"],
            "Min Temp": element_dict["MinT"][i]["parameter"]["parameterName"],
            "Max Temp": element_dict["MaxT"][i]["parameter"]["parameterName"],
            "Comfort": element_dict["CI"][i]["parameter"]["parameterName"]
        }
        records.append(record)

    return pd.DataFrame(records)
