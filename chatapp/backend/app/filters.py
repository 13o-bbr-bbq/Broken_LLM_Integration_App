from .models import Message


def input_filter(message: Message) -> Message:
    # Please write your input value filter codes here.
    filtered_text = message.text
    print(f'Input filtered:\n{filtered_text}')
    return Message(text=filtered_text)


def output_filter(answer_text: str) -> str:
    # Please write your output value filter codes here.
    filtered_text = answer_text
    print(f'Output filter:\n{filtered_text}')
    return filtered_text
