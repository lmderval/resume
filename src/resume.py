import os
from pathlib import Path
import shutil

from argparse import ArgumentParser

from jinja2 import Environment, FileSystemLoader

import yaml
from dacite import from_dict
from utils.nodes import Resume

dir = Path(os.path.dirname(os.path.realpath(__file__)))
cwd = Path(".")


def load_translation(language: str) -> dict:
    translation_file = dir / "translations" / f"{language}.yaml"
    with open(translation_file, "r") as f:
        return yaml.safe_load(f)


def main(*, path: str, language: str | None, variant: str | None):
    styles = dir / "styles"
    templates = dir / "templates"
    generated = cwd / "generated"
    env = Environment(
        loader=FileSystemLoader(templates),
        keep_trailing_newline=True,
    )
    template_resume = env.get_template("resume.html.jinja")

    with open(path, "r") as file:
        data = yaml.safe_load(file)
        resume_data = from_dict(Resume, data)

    resolved_language = language or data.get("language", "en")
    translation = load_translation(resolved_language)

    if variant is not None:
        resume_data.variant = (variant == "yes")

    os.makedirs(generated, exist_ok=True)

    resume = generated / "resume.html"
    if os.path.exists(resume):
        os.remove(resume)
    with open(resume, "w") as file:
        file.write(template_resume.render(resume=resume_data,
                                          translation=translation))
    os.chmod(resume, 0o444)

    css = generated / "resume.css"
    if os.path.exists(css):
        os.remove(css)
    shutil.copy(styles / "resume.css", css)
    os.chmod(css, 0o444)


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Convert a YAML resume source file into an HTML resume."
    )
    parser.add_argument(
        "--path",
        required=True,
        type=str,
        help="Path to the YAML resume source file.",
    )
    parser.add_argument(
        "--language",
        required=False,
        default=None,
        type=str,
        help=(
            "ISO language code for UI strings (e.g. 'fr', 'en'). "
            "Overrides the 'language' field in the YAML file. "
            "Defaults to the value from the YAML file, or 'en' if not set."
        ),
    )
    parser.add_argument(
        "--variant",
        required=False,
        default=None,
        choices=["yes", "no"],
        help=(
            "Override the 'variant' attribute from the YAML file. "
            "Defaults to the value from the YAML file, or 'no' (False) "
            "if not set."
        ),
    )
    args = parser.parse_args()

    main(path=args.path, language=args.language, variant=args.variant)
