import os
from pathlib import Path
import shutil

from argparse import ArgumentParser

from jinja2 import Environment, FileSystemLoader

import yaml
from dacite import from_dict
from utils.nodes import Resume

dir = Path(os.path.dirname(os.path.realpath(__file__)))
cwd = Path('.')


def load_translation(language: str) -> dict:
    translation_file = dir / "translations" / f"{language}.yaml"
    with open(translation_file, "r") as f:
        return yaml.safe_load(f)


def main(*, path: str, language: str | None):
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

    os.makedirs(generated, exist_ok=True)

    resume = generated / "resume.html"
    with open(resume, "w") as file:
        file.write(template_resume.render(resume=resume_data,
                                          translation=translation))

    shutil.copy(styles / "resume.css", generated / "resume.css")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--path", required=True, type=str)
    parser.add_argument("--language", required=False, default=None, type=str)
    args = parser.parse_args()

    main(path=args.path, language=args.language)
