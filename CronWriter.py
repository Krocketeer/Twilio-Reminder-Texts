"""
* Kenny "Ackerson" Le
* 11/25/20
* CronWriter
* Description: Writes cron.yaml file
"""

import pandas as pd
import urllib.parse
import datetime


def cron_writer(csv):
    df = pd.read_csv(csv)
    language_classes = df["Language Class"].to_list()
    language_classes_set = sorted(set(language_classes))

    leadership_cohorts = df["Leadership Cohort"].to_list()
    leadership_cohorts_set = sorted(set(leadership_cohorts))

    office_hours = df["Teacher"].to_list()
    office_hours_set = sorted(set(office_hours))

    print(office_hours_set)

    office_hours_times = {"Teacher1": ["wed", "14:35"],
                          "Teacher2": ["sat", "10:50"],
                          "Teacher3": ["sat", "14:50"],
                          "Teacher4": ["sun", "11:50"],
                          "Teacher5": [["mon, wed"], "17:10"],
                          "Teacher6": ["mon", "14:35"]}

    class1_dates = {"dec": ["9"], "jan": ["13", "27"],
                    "feb": ["10"], "mar": ["3", "17", "31"],
                    "apr": ["28"], "may": ["12", "26"], "jun": ["9"]}
    class2_class3_dates = {"dec": ["4"], "jan": ["8", "22"],
                           "feb": ["5", "26"], "mar": ["12", "26"],
                           "apr": ["23"], "may": ["7", "21"], "jun": ["4"]}
    class4_dates = {"dec": ["11"], "jan": ["15", "29"],
                    "feb": ["12"], "mar": ["5", "19"],
                    "apr": ["2", "30"], "may": ["14", "28"], "jun": ["11"]}
    class5_dates = {"dec": ["10"], "jan": ["14", "28"],
                    "feb": ["11"], "mar": ["4", "18"],
                    "apr": ["1", "29"], "may": ["13", "27"], "jun": ["10"]}

    program_dates = {"Class1": class1_dates, "Class 2 & Class 3": class2_class3_dates,
                     "Class4": class4_dates, "Class5": class5_dates}

    with open("cron.yaml", "w") as file:
        file.write("cron:\n")

        # Language Classes
        for language in language_classes_set:
            if language != "Class4":
                flask_url = urllib.parse.quote(language).replace("%3A", ":")
                if "%28" in flask_url:
                    flask_url = flask_url.replace("%28", '(')
                if "%29" in flask_url:
                    flask_url = flask_url.replace("%29", ')')

                if "M/W" in language:
                    days = "every monday, wednesday"
                elif "T/Th" in language:
                    days = "every tuesday, thursday"
                else:
                    days = "every wednesday"

                class_time = language.split()[-1]
                start = class_time[0:class_time.find("-")]
                if len(start) != 1:
                    hour = int(float(start[0:1])) + 12
                    minute = int(float(start[2:])) - 10
                    time24 = f"{hour}:{minute}"
                else:
                    hour = int(float(start[0:1])) + 11
                    time24 = f"{hour}:50"

                file.write(f"- description: '{language} Reminder'\n")
                file.write(f"  url: /send/language/{flask_url}\n")
                file.write(f"  schedule: {days} {time24}\n")
                file.write(f"  timezone: America/Los_Angeles\n")
                file.write(f"\n")

        # Leadership Cohorts
        for cohort in leadership_cohorts_set:
            if cohort != "Class" and cohort != "Section":
                flask_url = urllib.parse.quote(cohort)
                if "%26" in flask_url:
                    flask_url = flask_url.replace("%26", "&")

                date = datetime.datetime.now()
                month = date.strftime("%b").lower()
                session_date = ", ".join(str(e) for e in program_dates[cohort][month])
                time24 = "14:35" if cohort == "Class" else "15:35"

                file.write(f"- description: '{cohort} Leadership Reminder'\n")
                file.write(f"  url: /send/leadership/{flask_url}\n")
                file.write(f"  schedule: {session_date} of {month} {time24}\n")
                file.write(f"  timezone: America/Los_Angeles\n")
                file.write(f"\n")

        # Office Hours
        for teacher in office_hours_set:
            if teacher != "Teacher7":
                encode = urllib.parse.urlencode({"temp": teacher})
                flask_url = encode[encode.find("=") + 1:]

                if teacher == "Teacher5":
                    day = ''.join(char for char in office_hours_times[teacher][0])
                else:
                    day = office_hours_times[teacher][0]
                time24 = office_hours_times[teacher][1]
                file.write(f"- description: '{teacher} Office Hours Reminder'\n")
                file.write(f"  url: /send/office_hours/{flask_url}\n")
                file.write(f"  schedule: every {day} {time24}\n")
                file.write(f"  timezone: America/Los_Angeles\n")
                file.write(f"\n")


def main():
    print("Creating Cron Schedule")
    cron_writer("2020-2021 Roster.csv")
    print("Finished")


if __name__ == '__main__':
    main()
