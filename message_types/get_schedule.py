import pandas
import datetime

def get_schedule():
    df = pandas.read_csv("schedule/schedule_MPALG.csv")

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_date = "2023-09-18"
    current_time = datetime.datetime.now().strftime("%H:%M")
    current_time = "09:00"
    df = df.loc[(df["Begin date"] == current_date) & (df["Begin time"] >= current_time)]
    if len(df) == 0:
        return "You have nothing more to do today!"
    
    else: 
        next_activity = df.iloc[0]
        return f"""You have a {next_activity.Aktivitet} in {getattr(next_activity, 'Course name').split(',')[0]}, it starts at {getattr(next_activity, 'Begin time')} in {next_activity.Room}."""
    


print(get_schedule())