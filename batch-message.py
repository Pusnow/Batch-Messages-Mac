from applescript import AppleScript
import argparse
from string import Formatter

APPLE_SCRIPT = """
on run {arg1, arg2}
    set textMessage to arg1
    set phoneNumber to arg2
    tell application "Messages"
        send textMessage to buddy phoneNumber of service "SMS"
    end tell
end run
"""

PARSER = argparse.ArgumentParser()
PARSER.add_argument("-d", "--dry", help="Dry run", action="store_true")
PARSER.add_argument("list", type=str, help="Sending list")
PARSER.add_argument("message", type=str, help="Sending text")
ARGS = PARSER.parse_args()


def parse_files(sending_list_file, message_file):
    text_message = open(message_file).read()
    formatter = Formatter()
    number_of_fields = len(list(formatter.parse(text_message)))
    sending_list = []
    line_num = 0
    for line in open(sending_list_file).read().splitlines():
        line_num = 1
        receiver = line.split(",")
        if len(receiver) is not number_of_fields + 1:
            raise Exception(
                "The number of fields must be {}. (line {})".format(
                    number_of_fields + 1, line_num))

        sending_list.append(receiver)

    return {"message": text_message, "sending_list": sending_list}


def send_messages(sending_list, text_message):
    for receiver in sending_list:
        phone_number, *fields = receiver
        formatted_message = text_message.format(*fields)
        applescript = AppleScript(source=APPLE_SCRIPT)
        applescript.run(formatted_message, phone_number)




PARSED = parse_files(ARGS.list, ARGS.message)
send_messages(PARSED["sending_list"], PARSED["message"])
