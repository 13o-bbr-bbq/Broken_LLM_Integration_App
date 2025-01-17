from .models import Message


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
