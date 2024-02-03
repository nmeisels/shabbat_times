from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import csv
import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")


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
                    mincha_time = (datetime.datetime.combine(datetime.date.today(), in_time) + datetime.timedelta(
                        minutes=10)).time()
                    shabbat_time = f"פרשת {parsha}<br>מנחה ע״ש - {mincha_time.strftime('%H:%M')}<br>שחרית - 8:30<br>מנחה - {(datetime.datetime.combine(datetime.date.today(), in_time) + datetime.timedelta(minutes=-30)).strftime('%H:%M')}<br>ערבית - {out_time}<br>שבת שלום"
                    return shabbat_time

            print(f"No data found for {today}")

    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    csv_file_path = 'shabbat_times.csv'
    shabbat_time = get_shabbat_time_for_week(csv_file_path)
    return templates.TemplateResponse("index.html", {"request": request, "shabbat_time": shabbat_time})


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
