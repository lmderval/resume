import os
from pathlib import Path

from argparse import ArgumentParser

from jinja2 import Environment, FileSystemLoader

dir = Path(os.path.dirname(os.path.realpath(__file__)))


def main(*, path: str):
    templates = dir / "templates"
    generated = dir / "generated"
    env = Environment(
        loader=FileSystemLoader(templates),
        keep_trailing_newline=True,
    )
    template_resume = env.get_template("resume.html.jinja")

    os.makedirs(generated, exist_ok=True)

    resume = generated / "resume.html"
    with open(resume, "w") as file:
        file.write(template_resume.render())


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--path", required=True, type=str)
    args = parser.parse_args()

    main(path=args.path)
