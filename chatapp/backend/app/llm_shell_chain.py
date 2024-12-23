from langchain.chains import LLMChain
from langchain_experimental.pal_chain.base import PALChain, PALValidation

from .llm_models import create_chat_openai_model


# Create Shell chain using math prompt.
def create_shell_chain_math_prompt(prompt_template, user_prompt):
    pal_chain = PALChain.from_math_prompt(llm=create_chat_openai_model(), verbose=True)
    return pal_chain.run(user_prompt)


# Create Shell chain using native.
def create_shell_chain_native(prompt_template, user_prompt):
    try:
        llm = LLMChain(prompt=prompt_template, llm=create_chat_openai_model())
        pal_chain = PALChain(
            llm_chain=llm,
            code_validations=PALValidation(allow_imports=True, allow_command_exec=True),
            stop='\n\n\n',
            verbose=True,
        )
        return pal_chain.run(user_prompt)
    except Exception as e:
        print(f"Invalid question!: {e}")
        return 'Finish'
