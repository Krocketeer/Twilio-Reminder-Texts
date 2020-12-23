import json
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse
from flask import Flask, request, abort
from functools import wraps
import NumberList

app = Flask(__name__)

with open("API_Keys.json") as json_file:
    file = json.load(json_file)
    _account_sid = file["SID"]
    _auth_token = file["Token"]
    client = Client(_account_sid, _auth_token)

roster = "2020-2021 Roster.csv"
remind_message = "Hey {}, this is a reminder that your {} class starts in 10 mins at {} PM (PST). "\
                 "Please be sure to come on time. If you would like to opt out of these reminder " \
                 "messages, reply with 'STOP'."
oh_message = "Hey {}, this is a reminder that {} has office hours in 10 mins from {} (PST). Feel " \
             "free to drop by if you need any additional help. If you would like to opt out of " \
             "these reminder messages, reply with 'STOP'."


def validate_cron_request(f):
    """
    Validates that incoming requests genuinely originated from GAE Cron Scheduler
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('X-AppEngine-Cron') is None:
            app.logger.info("Error — Not sent from Cron Job")
            return abort(403)
        else:
            return f(*args, **kwargs)

    return decorated_function


@app.route("/text-reply", methods=["GET", "POST"])
def text_reply():
    response = MessagingResponse()
    form = "https://website.com/attendance"
    response.message(f"Sorry, staff does not receive replies to this "
                     f"number. If you are going to be absent, please "
                     f"fill out this form: {form}")
    return str(response)


@app.route("/voice-reply", methods=["GET", "POST"])
def phone_reply():
    response = VoiceResponse()
    response.say("Sorry, staff does not actively monitor this number for "
                 "calls. If you have any questions please email us. Thank you!",
                 voice='alice')
    return str(response)


@app.route("/send-test")
@validate_cron_request
def send_test():
    number_dict = {"Firstname Lastname": "+1234567890"}
    for person in number_dict:
        msg = client.messages.create(
            body=remind_message.format(person, "English", "3:00 AM"),
            from_="+1234567890",
            to=number_dict[person]
        )
        return msg.sid


@app.route("/send/language/<path:class_name>")
@validate_cron_request
def send_class_text(class_name):
    app.logger.info(class_name)
    number_dict = NumberList.get_lang_dict(csv=roster, class_name=class_name)
    for person in number_dict:
        class_title = person["Language Class"]
        language = class_title[0: class_title.find(":")]

        class_time = class_title.split()[-1]
        time = class_time[0: class_time.find("-")]
        msg = client.messages.create(
            body=remind_message.format(person["First Name"], language, time),
            from_="+1234567890",
            to=person["Phone Number"]
        )
        # print(remind_message.format(person["First Name"], language, time))
    return class_name


@app.route("/send/leadership/<path:cohort>")
@validate_cron_request
def send_leadership_text(cohort):
    time = "2:45" if cohort == "ARABIC" else "3:45"
    number_dict = NumberList.get_leadership_dict(csv=roster, leadership_cohort=cohort)
    for person in number_dict:
        msg = client.messages.create(
            body=remind_message.format(person["First Name"], "Leadership", time),
            from_="+1234567890",
            to=person["Phone Number"]
        )
    return cohort


@app.route("/send/office_hours/<path:teacher>")
@validate_cron_request
def send_office_hours_text(teacher):
    number_dict = NumberList.get_office_hours_dict(csv=roster, teacher=teacher)
    hours = {"Teacher1": "2:45 PM - 3:45 PM", "Teacher2": "11:00 AM - 12:00 PM",
             "Teacher3": "3:00 PM - 4:00 PM", "Teacher4": "12:00 PM - 1:00 PM ",
             "Teacher5": "5:20 PM - 5:50 PM", "Teacher6": "2:45 PM - 3:45 PM"}
    for person in number_dict:
        msg = client.messages.create(
            body=oh_message.format(person["First Name"], teacher, hours[teacher]),
            from_="+1234567890",
            to=person["Phone Number"]
        )
    return teacher


def main():
    print("Hello World")


if __name__ == '__main__':
    app.run(port=3000, debug=True)
    main()
