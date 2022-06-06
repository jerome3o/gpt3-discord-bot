import os
import logging
from typing import List, Optional, Tuple

import openai

from gptbot.db import (
    add_summary,
    get_latest_summary,
    get_dialog_since,
    get_latest_ai_name,
)
from gptbot.helpers import dialog_list_to_string
from gptbot.model import Summary, Dialog

_logger = logging.getLogger(__name__)

_DEFAULT_MODEL = "text-davinci-002"
_DEFAULT_TEMPERATURE = 0.6
_DEFAULT_MAX_TOKENS = 300

TEMPERATURE = float(os.environ.get("GPT3_TEMPERATURE", _DEFAULT_TEMPERATURE))
MAX_TOKENS = int(os.environ.get("GPT3_MAX_TOKENS", _DEFAULT_MAX_TOKENS))
MODEL = os.environ.get("GPT3_MODEL", _DEFAULT_MODEL)


def query_gpt3(prompt: str) -> str:
    _logger.info(f"Querying GPT-3 with {len(prompt)} character prompt")
    response = openai.Completion.create(
        prompt=prompt,
        engine=MODEL,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        presence_penalty=2,
    )
    return response.choices[0].text


def resummarise_if_needed(context_id: str) -> Optional[Summary]:
    # TODO(j.swannack): Opinions

    summary, dialog_list, ai_name = get_contextual_info(context_id)
    if len(dialog_list) < 10:
        return None

    ts = dialog_list[-1].timestamp

    prompt = _construct_prompt(summary, dialog_list, ai_name, add_ai_prompt=False)
    prompt += "\n\nWrite a short overview of the recent events:\n"

    response = query_gpt3(prompt)

    summary = add_summary(
        Summary(timestamp=ts, context_id=context_id, summary=response)
    )
    return summary


def get_contextual_info(context_id: str) -> Tuple[Summary, List[Dialog], str]:
    summary = get_latest_summary(context_id)
    dialog_list = get_dialog_since(context_id, summary.timestamp)
    ai_name = get_latest_ai_name(context_id=context_id)
    return summary, dialog_list, ai_name


def construct_prompt(context_id: str, add_ai_prompt: bool = True):
    # TODO(j.swannack): Actions
    summary, dialog_list, ai_name = get_contextual_info(context_id)
    return _construct_prompt(
        summary=summary,
        dialog_list=dialog_list,
        ai_name=ai_name,
        add_ai_prompt=add_ai_prompt,
    )


def _construct_prompt(
    summary: Summary,
    dialog_list: List[Dialog],
    ai_name: str,
    add_ai_prompt: bool = True,
):

    dialog = dialog_list_to_string(dialog_list)
    prompt = f"{summary.summary}\n\n{dialog}"

    if add_ai_prompt:
        prompt += f"\n{ai_name}: "

    return prompt
