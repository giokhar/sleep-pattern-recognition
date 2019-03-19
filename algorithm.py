import pandas as pd, json
from datetime import datetime, timedelta

def datetime_str_to_object(fitbit_str):
    """Helper function to convert fitbit datetime str into python datetime object"""
    return datetime.strptime(fitbit_str, "%Y-%m-%dT%H:%M:%S.000")


def main():
	with open('data/alta_hr/2019.03.19.heart.json') as f:
		data = json.load(f)

	print(data)


if __name__ == '__main__':
	main()