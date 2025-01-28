from .models import Message
from .blacklists import INPUT_BLACKLIST, OUTPUT_BLACKLIST, contains_blacklisted_pattern


# Input validator.
def input_filter(message: Message) -> Message:
    filtered_text = ''
    user_text = message.text or ""
    if contains_blacklisted_pattern(user_text, INPUT_BLACKLIST):
        raise ValueError('Blocked by input filter. (Potential malicious request)')
    else:
        filtered_text = user_text
    return Message(text=filtered_text)


# Output validator.
def output_filter(answer_text: str) -> str:
    filtered_text = ''
    if contains_blacklisted_pattern(answer_text, OUTPUT_BLACKLIST):
        raise ValueError('Blocked by output filter. (Potential data leak)')
    else:
        filtered_text = answer_text
    return filtered_text
