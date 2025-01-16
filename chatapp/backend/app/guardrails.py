from pathlib import Path
from nemoguardrails import RailsConfig
from nemoguardrails.integrations.langchain.runnable_rails import RunnableRails


# Define NeMo-Guardrails.
def load_nemo_guardrails(is_sql=False):
    current_dir = Path(__file__).parent
    nemo_config = RailsConfig.from_path(str(current_dir / "nemo_config" / "config.yml"))
    if is_sql:
        nemo_config = RailsConfig.from_path(str(current_dir / "nemo_config" / "config_for_sql.yml"))
        return RunnableRails(nemo_config, input_key="input")
    return RunnableRails(nemo_config)
