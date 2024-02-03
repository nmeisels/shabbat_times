import csv
import datetime


def get_shabbat_time_for_week(csv_file_path):
    try:
        today = datetime.date.today()
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                parsha = row['Parsha']
                date_str = row['Date']
                in_time = datetime.datetime.strptime(row['In'], '%H:%M').time()
                out_time = row['Out']
                shabbat_date = datetime.datetime.strptime(date_str, '%d/%m/%Y').date()

                if shabbat_date >= today:
                        mincha_time = (datetime.datetime.combine(datetime.date.today(), in_time) + datetime.timedelta(minutes=10)).time()
                        print(f"פרשת {parsha}")
                        print(f"מנחה ע״ש - {mincha_time.strftime('%H:%M')}")
                        print(f"שחרית - 8:30")
                        print(f"מנחה - {(datetime.datetime.combine(datetime.date.today(), in_time) + datetime.timedelta(minutes=-30)).strftime('%H:%M')}")
                        print(f"ערבית - {out_time}")
                        print(f"שבת שלום")
                        return

            print(f"No data found for {today}")

    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
csv_file_path = 'shabbat_times.csv'
get_shabbat_time_for_week(csv_file_path)
