import uuid

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from .llm_models import *
from .llm_prompt_templates import *
from .llm_db_chain import create_db_chain
from .llm_shell_chain import create_shell_chain_math_prompt, create_shell_chain_native


# Ask questions to the LLM using Database.
def p2sql_injection_lv1(question: str) -> str:
    try:
        prompt = p2sql_injection_lv1_template.format(
            top_k=5,
            table_info="users, chats, memberships, messages, user_settings",
            question=question
        )
        answer = create_db_chain().run(prompt)
        return ','.join(answer) if isinstance(answer, list) else str(answer)
    except Exception as e:
        return f"Error in ask_question_db: {', '.join(map(str, e.args))}"


# Ask questions to the LLM using Database.
def p2sql_injection_lv2(question: str) -> str:
    try:
        prompt = p2sql_injection_lv2_template.format(
            top_k=5,
            table_info="users, chats, memberships, messages, user_settings",
            question=question
        )
        answer = create_db_chain().run(prompt)
        return ','.join(answer) if isinstance(answer, list) else str(answer)
    except Exception as e:
        return f"Error: {', '.join(map(str, e.args))}"


# Ask questions to the LLM using Database. This level is implemented prompt hardener.
def p2sql_injection_lv3(question: str) -> str:
    try:
        prompt = p2sql_injection_lv3_template.format(
            top_k=5,
            table_info="users, chats, memberships, messages, user_settings",
            question=question,
            SECURE_TAG=uuid.uuid4()
        )
        answer = create_db_chain().run(prompt)
        return ','.join(answer) if isinstance(answer, list) else str(answer)
    except Exception as e:
        return f"Error: {', '.join(map(str, e.args))}"


# Ask questions to the LLM.
def prompt_leaking_lv1(question: str) -> str:
    prompt = PromptTemplate(template=prompt_leaking_lv1_template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=create_chat_openai_model())
    answer = llm_chain.run(question)
    return answer


# Ask questions to the LLM using system files.
def llm4shell_lv1(question: str) -> str:
    try:
        prompt_template = PromptTemplate(template=llm4shell_template, input_variables=["question"])
        answer = create_shell_chain_math_prompt(prompt_template, question)
        return answer if isinstance(answer, dict) else str(answer)
    except Exception as e:
        return f"Error in ask_question_shell: {', '.join(map(str, e.args))}"


# Ask questions to the LLM using system files.
def llm4shell_lv2(question: str) -> str:
    try:
        prompt_template = PromptTemplate(template=llm4shell_template, input_variables=["question"])
        answer = create_shell_chain_native(prompt_template, question)
        return answer if isinstance(answer, dict) else str(answer)
    except Exception as e:
        return f"Error in ask_question_shell: {', '.join(map(str, e.args))}"


# Ask questions to the LLM using system files. This level is implemented prompt hardener.
def llm4shell_lv3(question: str) -> str:
    try:
        prompt_template = PromptTemplate(template=llm4shell_lv3_template, input_variables=["question", "random_salt"])
        answer = create_shell_chain_native(prompt_template, {"question": question, "random_salt": uuid.uuid4()})
        return answer if isinstance(answer, dict) else str(answer)
    except Exception as e:
        return f"Error in ask_question_shell: {', '.join(map(str, e.args))}"
