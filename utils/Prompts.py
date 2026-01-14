from pathlib import Path


def load_prompt(file_name: str) -> str:

    prompt_path = Path(__file__).parent.parent / "prompts" / f"{file_name}.md"

    return prompt_path.read_text(encoding="utf-8")


def render_prompt(template: str, **kwargs) -> str:
    try:
        return template.format(**kwargs)
    except KeyError as e:
        raise ValueError(f"Missing required key: {e}")


def get_prompt(file_name: str, **kwargs) -> str:
    template = load_prompt(file_name)
    return render_prompt(template, **kwargs)
