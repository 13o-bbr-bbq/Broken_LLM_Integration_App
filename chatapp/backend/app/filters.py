from guardrails.hub import RegexMatch, DetectPII
from guardrails import Guard

from .models import Message

# Use the Guard with the validator (samples).
pii_output_guard = Guard().use(
    DetectPII, ["EMAIL_ADDRESS"], "exception"
)
regex_output_guard = Guard().use(
    RegexMatch, regex="dt5\-ctf\:.*", on_fail="exception"
)


# Input validator.
def input_filter(message: Message) -> Message:
    # Please write your input validation codes here.
    filtered_text = ''
    try:
        filtered_text = message.text
    except Exception as e:
        filtered_text = 'Input validation error: Your instruction is invalid.'
    return Message(text=filtered_text)


# Output validator.
def output_filter(answer_text: str) -> str:
    # Please write your output validation codes here.
    filtered_text = ''
    try:
        filtered_text = answer_text
    except Exception as e:
        filtered_text = 'Output validation error: Your instruction is invalid.'
    return filtered_text
