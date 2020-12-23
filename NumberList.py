"""
* Kenny "Ackerson" Le
* 11/20/20
* NumberList
* Description: Generates the appropriate list of numbers from the main roster
"""

import pandas as pd


def get_lang_dict(csv, class_name):
    df = pd.read_csv(csv)
    df = df.filter(["Status", "First Name", "Language Class", "Phone Number", "Twilio Status"])

    is_enrolled = df["Status"] == "Enrolled"
    is_class = df["Language Class"] == class_name
    can_text = (df["Twilio Status"] != "Unsubscribed") & (df["Twilio Status"] != "Error")

    df = df[is_enrolled & is_class & can_text]
    return format_number(df.to_dict("records"))


def get_leadership_dict(csv, leadership_cohort):
    df = pd.read_csv(csv)
    df = df.filter(["Status", "First Name", "Leadership Cohort", "Phone Number", "Twilio Status"])

    is_enrolled = df["Status"] == "Enrolled"
    is_class = df["Leadership Cohort"] == leadership_cohort
    can_text = (df["Twilio Status"] != "Unsubscribed") & (df["Twilio Status"] != "Error")

    df = df[is_enrolled & is_class & can_text]
    return format_number(df.to_dict("records"))


def get_office_hours_dict(csv, teacher):
    df = pd.read_csv(csv)
    df = df.filter(["Status", "First Name", "Teacher", "Phone Number", "Twilio Status"])

    is_enrolled = df["Status"] == "Enrolled"
    has_teacher = df["Teacher"] == teacher
    can_text = (df["Twilio Status"] != "Unsubscribed") & (df["Twilio Status"] != "Error")

    df = df[is_enrolled & has_teacher & can_text]
    return format_number(df.to_dict("records"))


def format_number(num_list):
    for student in num_list:
        num = student["Phone Number"]
        student["Phone Number"] = "+1" + ''.join(char for char in num if char.isalnum())

    return num_list


def main():
    print("Hello World")


if __name__ == '__main__':
    main()
