import uuid

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from .llm_models import *
from .llm_prompt_templates import *
from .llm_db_chain import create_db_chain
from .llm_shell_chain import run_pal_chain_native
from .guardrails import *
from .settings import settings


# This level is no guard.
def prompt_leaking_lv1(question: str) -> str:
    try:
        prompt = PromptTemplate(template=prompt_leaking_lv1_template, input_variables=["question"])
        llm_chain = LLMChain(prompt=prompt, llm=create_chat_openai_model())
        answer = llm_chain.run(question)
        return answer
    except Exception as e:
        print(e)
        return f"Error in ask_question_leaking: {e}"


# This level is implemented input/output filters.
def prompt_leaking_lv2(question: str) -> str:
    try:
        prompt = PromptTemplate(template=prompt_leaking_lv1_template, input_variables=["question"])
        llm_chain = LLMChain(prompt=prompt, llm=create_chat_openai_model())
        answer = llm_chain.run(question)
        return answer
    except Exception as e:
        return f"Error in ask_question_leaking: {', '.join(map(str, e.args))}"


# This level is implemented prompt hardener.
def prompt_leaking_lv3(question: str) -> str:
    try:
        prompt = PromptTemplate(template=prompt_leaking_lv3_template, input_variables=["question", "secure_tag"])
        llm_chain = LLMChain(prompt=prompt, llm=create_chat_openai_model())
        answer = llm_chain.run({"question": question, "secure_tag": uuid.uuid4()})
        return answer
    except Exception as e:
        return f"Error in ask_question_leaking: {', '.join(map(str, e.args))}"


# This level is implemented NeMo-Guardrails.
async def prompt_leaking_lv4(question: str) -> str:
    try:
        guardrails = load_nemo_guardrails()
        prompt_template = PromptTemplate(template=prompt_leaking_lv1_template, input_variables=["question"])
        model = create_chat_openai_model()
        chain_with_guardrails = prompt_template | (guardrails | model)
        answer = await chain_with_guardrails.ainvoke({'question': question})
        return answer
    except Exception as e:
        return f"Error in ask_question_leaking: {', '.join(map(str, e.args))}"


# This level is implemented DeepKeep.
async def prompt_leaking_lv5(question: str) -> str:
    try:
        _conversation_id = dk_start_conversation(firewall_id=settings.DK_FIREWALL_ID)

        # Input Firewall.
        request_res = dk_request_filter(
            firewall_id=settings.DK_FIREWALL_ID,
            conversation_id=_conversation_id,
            prompt=question,
            verbose=False
        )
        print(f"Request firewall data: {request_res.get('content')}")
        if len(request_res) != 0:
            print(f"Question: {question}")
            prompt = PromptTemplate(template=prompt_leaking_lv1_template, input_variables=["question"])
            llm_chain = LLMChain(prompt=prompt, llm=create_chat_openai_model())
            answer = llm_chain.run(question)
            print(f"Answer: {answer}")
            response_res = dk_response_filter(
                firewall_id=settings.DK_FIREWALL_ID,
                conversation_id=_conversation_id,
                prompt=answer,
                verbose=False
            )
            print(response_res)
            if len(response_res) == 0:
                raise ValueError('Prompt Attack Detected in response by DeepKeep.')
            return answer
        else:
            raise ValueError('Prompt Attack Detected in request by DeepKeep.')
    except Exception as e:
        return f"Error in ask_question_leaking: {', '.join(map(str, e.args))}"


# This level is no guard.
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


# This level is implemented input/output filters.
def p2sql_injection_lv2(question: str) -> str:
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


# This level is implemented defensive prompt template.
def p2sql_injection_lv3(question: str) -> str:
    try:
        prompt = p2sql_injection_lv3_template.format(
            top_k=5,
            table_info="users, chats, memberships, messages, user_settings",
            question=question
        )
        answer = create_db_chain().run(prompt)
        return ','.join(answer) if isinstance(answer, list) else str(answer)
    except Exception as e:
        return f"Error in ask_question_db: {', '.join(map(str, e.args))}"


# This level is implemented prompt hardener.
def p2sql_injection_lv4(question: str) -> str:
    try:
        prompt = p2sql_injection_lv4_template.format(
            top_k=5,
            table_info="users, chats, memberships, messages, user_settings",
            question=question,
            secure_tag=uuid.uuid4()
        )
        answer = create_db_chain().run(prompt)
        return ','.join(answer) if isinstance(answer, list) else str(answer)
    except Exception as e:
        return f"Error in ask_question_db: {', '.join(map(str, e.args))}"


# This level is implemented LLM-as-a-Judge.
def p2sql_injection_lv5(question: str) -> str:
    try:
        # LLM-as-a-Judge for Input.
        judge_prompt = PromptTemplate(
            template=p2sql_injection_lv5_template_for_input_judge,
            input_variables=["question", "secure_tag"]
        )
        judge_llm_chain = LLMChain(prompt=judge_prompt, llm=create_chat_openai_model())
        judge_result = judge_llm_chain.run({"question": question, "secure_tag": uuid.uuid4()})

        answer = ''
        print(f'Input judge result: {judge_result}')
        #judge_result = 'yes'
        if judge_result.lower() == 'yes':
            prompt = p2sql_injection_lv1_template.format(
                top_k=5,
                table_info="users, chats, memberships, messages, user_settings",
                question=question
            )
            answer = create_db_chain().run(prompt)

            # LLM-as-a-Judge for Output.
            judge_prompt = PromptTemplate(
                template=p2sql_injection_lv5_template_for_output_judge,
                input_variables=["answer", "secure_tag"]
            )
            judge_llm_chain = LLMChain(prompt=judge_prompt, llm=create_chat_openai_model())
            judge_result = judge_llm_chain.run({"answer": answer, "secure_tag": uuid.uuid4()})
            print(f'Output judge result: {judge_result}')
            if judge_result.lower() == 'no':
                raise ValueError('Confidential information Detected.')
        else:
            raise ValueError('Prompt Attack Detected.')
        return ','.join(answer) if isinstance(answer, list) else str(answer)
    except Exception as e:
        return f"Error in ask_question_db: {', '.join(map(str, e.args))}"


# This level is no guard.
def llm4shell_lv1(question: str) -> str:
    try:
        prompt_template = PromptTemplate(template=llm4shell_template, input_variables=["question"])
        answer = run_pal_chain_native(prompt_template, question)
        return answer if isinstance(answer, dict) else str(answer)
    except Exception as e:
        return f"Error in ask_question_shell: {', '.join(map(str, e.args))}"


# This level is implemented input/output filters.
def llm4shell_lv2(question: str) -> str:
    try:
        prompt_template = PromptTemplate(template=llm4shell_template, input_variables=["question"])
        answer = run_pal_chain_native(prompt_template, question)
        return answer if isinstance(answer, dict) else str(answer)
    except Exception as e:
        return f"Error in ask_question_shell: {', '.join(map(str, e.args))}"


# This level is implemented prompt hardener.
def llm4shell_lv3(question: str) -> str:
    try:
        prompt_template = PromptTemplate(template=llm4shell_lv3_template, input_variables=["question", "secure_tag"])
        answer = run_pal_chain_native(prompt_template, {"question": question, "secure_tag": uuid.uuid4()})
        return answer if isinstance(answer, dict) else str(answer)
    except Exception as e:
        return f"Error in ask_question_shell: {', '.join(map(str, e.args))}"


# This level is implemented LLM-as-a-Judge.
def llm4shell_lv4(question: str) -> str:
    try:
        # LLM-as-a-Judge.
        judge_prompt = PromptTemplate(
            template=llm4shell_lv4_template_for_input_judge,
            input_variables=["question", "secure_tag"]
        )
        judge_llm_chain = LLMChain(prompt=judge_prompt, llm=create_chat_openai_model())
        judge_result = judge_llm_chain.run({"question": question, "secure_tag": uuid.uuid4()})

        answer = ''
        print(f'Input judge result: {judge_result}')
        #judge_result = 'yes'
        if judge_result.lower() == 'yes':
            prompt_template = PromptTemplate(template=llm4shell_template, input_variables=["question"])
            answer = run_pal_chain_native(prompt_template, question)

            # LLM-as-a-Judge for Output.
            judge_prompt = PromptTemplate(
                template=llm4shell_lv4_template_for_output_judge,
                input_variables=["answer", "secure_tag"]
            )
            judge_llm_chain = LLMChain(prompt=judge_prompt, llm=create_chat_openai_model())
            judge_result = judge_llm_chain.run({"answer": answer, "secure_tag": uuid.uuid4()})
            print(f'Output judge result: {judge_result}')
            if judge_result.lower() == 'no':
                raise ValueError('Confidential information Detected.')
        else:
            raise ValueError('Prompt Attack Detected.')
        return answer
    except Exception as e:
        return f"Error in ask_question_shell: {', '.join(map(str, e.args))}"
