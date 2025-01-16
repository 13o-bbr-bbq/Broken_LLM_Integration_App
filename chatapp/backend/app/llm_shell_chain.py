from langchain.chains import LLMChain
from langchain_experimental.pal_chain.base import PALChain, PALValidation

from .llm_models import create_chat_openai_model


# Create PALChain using math prompt.
def create_pal_chain_math_prompt():
    pal_chain = PALChain.from_math_prompt(
        llm=create_chat_openai_model(),
        verbose=True,
        allow_dangerous_code=True
    )
    return pal_chain

# Run PALChain using math prompt.
def run_pal_chain_math_prompt(user_prompt):
    pal_chain = create_pal_chain_math_prompt()
    return pal_chain.run(user_prompt)

# Create PALChain using native.
def create_pal_chain_native(prompt_template):
    try:
        # Define LLMChain.
        llm = LLMChain(
            prompt=prompt_template,
            llm=create_chat_openai_model(),
        )
        # Define PALChain.
        pal_chain = PALChain(
            llm_chain=llm,
            allow_dangerous_code=True,
            code_validations=PALValidation(
                allow_imports=True,
                allow_command_exec=True
            ),
            stop='\n\n\n',
            verbose=True,
        )
        return pal_chain
    except Exception as e:
        print(f"Invalid question!: {e}")
        return 'Finish'

# Run PALChain using native.
def run_pal_chain_native(prompt_template, user_prompt):
    pal_chain = create_pal_chain_native(prompt_template)
    return pal_chain.run(user_prompt)
