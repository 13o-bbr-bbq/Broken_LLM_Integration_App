import uuid

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from .llm_models import *
from .llm_prompt_templates import *
from .llm_db_chain import create_db_chain
from .llm_shell_chain import run_pal_chain_math_prompt, run_pal_chain_native
from .guardrails import load_nemo_guardrails


# Ask questions to the LLM.
def prompt_leaking_lv1(question: str) -> str:
    try:
        prompt = PromptTemplate(template=prompt_leaking_lv1_template, input_variables=["question"])
        llm_chain = LLMChain(prompt=prompt, llm=create_chat_openai_model())
        answer = llm_chain.run(question)
        return answer
    except Exception as e:
        return f"Error in ask_question_leaking: {', '.join(map(str, e.args))}"


# Ask questions to the LLM. This level is implemented prompt hardener.
def prompt_leaking_lv2(question: str) -> str:
    try:
        prompt = PromptTemplate(template=prompt_leaking_lv2_template, input_variables=["question", "secure_tag"])
        llm_chain = LLMChain(prompt=prompt, llm=create_chat_openai_model())
        answer = llm_chain.run({"question": question, "secure_tag": uuid.uuid4()})
        return answer
    except Exception as e:
        return f"Error in ask_question_leaking: {', '.join(map(str, e.args))}"


# Ask questions to the LLM. This level is implemented NeMo-Guardrails.
async def prompt_leaking_lv3(question: str) -> str:
    try:
        guardrails = load_nemo_guardrails()
        prompt_template = PromptTemplate(template=prompt_leaking_lv1_template, input_variables=["question"])
        model = create_chat_openai_model()
        chain_with_guardrails = prompt_template | (guardrails | model)
        answer = await chain_with_guardrails.ainvoke({'question': question})
        return answer
    except Exception as e:
        return f"Error in ask_question_leaking: {', '.join(map(str, e.args))}"


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
        return f"Error in ask_question_db: {', '.join(map(str, e.args))}"


# Ask questions to the LLM using Database. This level is implemented prompt hardener.
def p2sql_injection_lv3(question: str) -> str:
    try:
        prompt = p2sql_injection_lv3_template.format(
            top_k=5,
            table_info="users, chats, memberships, messages, user_settings",
            question=question,
            secure_tag=uuid.uuid4()
        )
        answer = create_db_chain().run(prompt)
        return ','.join(answer) if isinstance(answer, list) else str(answer)
    except Exception as e:
        return f"Error in ask_question_db: {', '.join(map(str, e.args))}"


# Ask questions to the LLM using Database. This level is implemented LLM-as-a-Judge.
def p2sql_injection_lv4(question: str) -> str:
    try:
        # LLM-as-a-Judge.
        judge_prompt = PromptTemplate(
            template=p2sql_injection_lv4_template_for_judge,
            input_variables=["question", "secure_tag"]
        )
        judge_llm_chain = LLMChain(prompt=judge_prompt, llm=create_chat_openai_model())
        judge_result = judge_llm_chain.run({"question": question, "secure_tag": uuid.uuid4()})

        answer = ''
        print(judge_result)
        if judge_result.lower() == 'yes':
            prompt = p2sql_injection_lv1_template.format(
                top_k=5,
                table_info="users, chats, memberships, messages, user_settings",
                question=question
            )
            answer = create_db_chain().run(prompt)
        else:
            raise ValueError('Prompt Attack Detected.')
        return ','.join(answer) if isinstance(answer, list) else str(answer)
    except Exception as e:
        return f"Error in ask_question_db: {', '.join(map(str, e.args))}"


# Ask questions to the LLM using system files.
def llm4shell_lv1(question: str) -> str:
    try:
        answer = run_pal_chain_math_prompt(question)
        return answer if isinstance(answer, dict) else str(answer)
    except Exception as e:
        return f"Error in ask_question_shell: {', '.join(map(str, e.args))}"


# Ask questions to the LLM using system files.
def llm4shell_lv2(question: str) -> str:
    try:
        prompt_template = PromptTemplate(template=llm4shell_template, input_variables=["question"])
        answer = run_pal_chain_native(prompt_template, question)
        return answer if isinstance(answer, dict) else str(answer)
    except Exception as e:
        return f"Error in ask_question_shell: {', '.join(map(str, e.args))}"


# Ask questions to the LLM using system files. This level is implemented prompt hardener.
def llm4shell_lv3(question: str) -> str:
    try:
        prompt_template = PromptTemplate(template=llm4shell_lv3_template, input_variables=["question", "secure_tag"])
        answer = run_pal_chain_native(prompt_template, {"question": question, "secure_tag": uuid.uuid4()})
        return answer if isinstance(answer, dict) else str(answer)
    except Exception as e:
        return f"Error in ask_question_shell: {', '.join(map(str, e.args))}"


# Ask questions to the LLM using system files. This level is implemented LLM-as-a-Judge.
def llm4shell_lv4(question: str) -> str:
    try:
        # LLM-as-a-Judge.
        judge_prompt = PromptTemplate(
            template=llm4shell_lv4_template_for_judge,
            input_variables=["question", "secure_tag"]
        )
        judge_llm_chain = LLMChain(prompt=judge_prompt, llm=create_chat_openai_model())
        judge_result = judge_llm_chain.run({"question": question, "secure_tag": uuid.uuid4()})

        answer = ''
        print(judge_result)
        if judge_result.lower() == 'yes':
            prompt_template = PromptTemplate(template=llm4shell_template, input_variables=["question"])
            answer = run_pal_chain_native(prompt_template, question)
        else:
            raise ValueError('Prompt Attack Detected.')
        return answer
    except Exception as e:
        return f"Error in ask_question_shell: {', '.join(map(str, e.args))}"
