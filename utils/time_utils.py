from datetime import timezone, timedelta, datetime

IST = timezone(timedelta(hours=5, minutes=30))


def convert_utc_to_ist(data):

    if isinstance(data, list):
        return [convert_utc_to_ist(item) for item in data]

    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():

            if isinstance(value, datetime):
                new_data[key] = value.astimezone(IST).strftime("%Y-%m-%d %H:%M:%S")

            else:
                new_data[key] = convert_utc_to_ist(value)

        return new_data

    return data