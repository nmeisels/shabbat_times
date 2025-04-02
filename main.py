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
                    
                    # Calculate initial shabbat_mincha_time
                    shabbat_mincha_time = (datetime.datetime.combine(datetime.date.today(), in_time) + datetime.timedelta(minutes=-30)).time()
                    
                    # Check if shabbat_mincha_time is after 18:00
                    is_late_mincha = shabbat_mincha_time >= datetime.time(18, 0)
                    if is_late_mincha:
                        shabbat_mincha_time = datetime.time(18, 0)
                    
                    # Calculate other times based on adjusted shabbat_mincha_time
                    parents_and_kids = (datetime.datetime.combine(datetime.date.today(), shabbat_mincha_time) + datetime.timedelta(minutes=-40)).strftime('%H:%M')
                    tehillim_time = (datetime.datetime.combine(datetime.date.today(), shabbat_mincha_time) + datetime.timedelta(minutes=-60)).strftime('%H:%M')
                    
                    # Prepare the mincha line with conditional text
                    mincha_line = f"מנחה - {shabbat_mincha_time.strftime('%H:%M')}"
                    if not is_late_mincha:
                        mincha_line += " (תוך כדי מנחה תהילים לילדים)"
                    
                    # Build the schedule with conditional tehillim line
                    schedule_lines = [
                        f"פרשת {parsha}",
                        f"מנחה ע״ש - {mincha_time.strftime('%H:%M')}",
                        "מניין ילדים אחרי לכה דודי",
                        "",
                        "שחרית - 8:30",
                        "מניין ילדים - 10:00",
                        "קידוש ספונטני - 10:30~"
                    ]
                    
                    if is_late_mincha:
                        schedule_lines.extend([
                            f"תהילים לילדים - {tehillim_time}",
                            f"הורים וילדים - {parents_and_kids}"
                        ])
                    else:
                        schedule_lines.append(f"הורים וילדים - {parents_and_kids}")
                    
                    schedule_lines.extend([
                        mincha_line,
                        f"ערבית - {out_time}",
                        "שבת שלום!"
                    ])
                    
                    shabbat_time = "<br>".join(schedule_lines)
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
    # return templates.TemplateResponse("index.html", {"request": request, "shabbat_time": ""})


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
