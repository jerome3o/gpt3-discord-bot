from gptbot.db import get_latest_summary, get_dialog_since, get_latest_ai_name
from gptbot.helpers import dialog_list_to_string


def construct_prompt(context_id: str, add_ai_prompt: bool = True):
    summary = get_latest_summary(context_id)
    dialog_list = get_dialog_since(context_id, summary.timestamp)
    ai_name = get_latest_ai_name(context_id=context_id)

    # TODO(j.swannack): Actions?

    dialog = dialog_list_to_string(dialog_list)
    prompt = f"{summary.summary}\n\n{dialog}"

    if add_ai_prompt:
        prompt += f"\n{ai_name}: "

    return prompt
