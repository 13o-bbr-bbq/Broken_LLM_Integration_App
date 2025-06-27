import requests
import time
from pathlib import Path
from typing import Optional
from time import sleep
from nemoguardrails import RailsConfig
from nemoguardrails.integrations.langchain.runnable_rails import RunnableRails

from .settings import settings

# Define NeMo-Guardrails.
def load_nemo_guardrails(is_sql=False):
    current_dir = Path(__file__).parent
    nemo_config = RailsConfig.from_path(str(current_dir / "nemo_config" / "config.yml"))
    if is_sql:
        nemo_config = RailsConfig.from_path(str(current_dir / "nemo_config" / "config_for_sql.yml"))
        return RunnableRails(nemo_config, input_key="input")
    return RunnableRails(nemo_config)


# Generate DeepKeep header.
def _dk_generate_headers() -> dict[str, str]:
    return {"x-api-key": settings.DK_TOKEN}


# Session start with DeepKeep.
def dk_start_conversation(firewall_id: str, system_instruction: Optional[str]=None) -> str:
    body = {"system_prompt": system_instruction} if system_instruction else {}
    conversation_res = requests.post(f"{settings.DK_API_URL}/monitoring/{firewall_id}/conversation",
                                     headers=_dk_generate_headers(), json=body)

    if not conversation_res.ok:
        raise Exception(f"failed to create a new conversation on {firewall_id} due to error: {conversation_res.reason}")

    conversation = conversation_res.text.strip('"')

    if not conversation:
        raise Exception("failed to create a conversation due to general error.")
    return conversation


# Get statistics from DeepKeep.
def dk_get_statistics(request_id: str):
    for _retry in range(5):
      sleep(0.5)
      _res_verbose = requests.get(url=f"{settings.DK_API_URL}/report/statistics/message/{request_id}", headers=_dk_generate_headers())
      if _res_verbose.ok:
        return {"statistics": _res_verbose.json()}
      else:
        print(_res_verbose.reason)
    return {"statistics": None}


# Send request to DeepKeep Input Filters.
def dk_request_filter(firewall_id: str, conversation_id: str, prompt: str, logs: bool = False, verbose: bool = False):
    input_prompt_params = {"content": prompt, "logs": logs}
    start_time = time.perf_counter()
    request_filter_res = requests.post(f"{settings.DK_API_URL}/monitoring/{firewall_id}/conversation/{conversation_id}/check_user_input",
                                     json=input_prompt_params,
                                     headers=_dk_generate_headers())
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    if not request_filter_res.ok:
        print(request_filter_res.json())
        return {}, elapsed_time

    firewall_response = request_filter_res.json()

    if verbose:
        _res_verbose = dk_get_statistics(request_id=firewall_response.get("request_id"))
        firewall_response |= _res_verbose

    return firewall_response, elapsed_time


# Send response to DeepKeep Output Filters.
def dk_response_filter(firewall_id: str, conversation_id: str, prompt: str, logs: bool = False, verbose: bool = False):
    input_prompt_params = {"content": prompt, "logs": logs}
    start_time = time.perf_counter()
    response_filter_res = requests.post(f"{settings.DK_API_URL}/monitoring/{firewall_id}/conversation/{conversation_id}/check_model_output",
                                        json=input_prompt_params, headers=_dk_generate_headers())
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    if not response_filter_res.ok:
        print(response_filter_res.json())
        return {}, elapsed_time

    firewall_response = response_filter_res.json()
    if verbose:
        _res_verbose = dk_get_statistics(request_id=firewall_response.get("request_id"))
        firewall_response |= _res_verbose

    return firewall_response, elapsed_time
