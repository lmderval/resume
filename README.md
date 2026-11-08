# Resume

A tool to convert YAML inputs into resumes.

## Usage

### Run directly

```sh
nix run . -- --path src/resumes/resume.yaml
```

Pass additional arguments after `--`:

```sh
nix run . -- --path src/resumes/resume.yaml --language fr
```

Pass `--variant` to override the side-panel colour variant:

```sh
nix run . -- --path src/resumes/resume.yaml --variant no
```

### Build & run the executable

```sh
nix build
./result/bin/resume --path src/resumes/resume.yaml
```

The built binary lives at `result/bin/resume`.

### Build the generated output only

Produces a ready-to-use `resume.html` and `resume.css` pair built from the
default `src/resumes/resume.yaml`:

```sh
nix build .#generated
```

The resulting files are placed in `result/`.

---

## Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--help`, `-h` | No | — | Show the help message and exit. |
| `--path PATH` | **Yes** | — | Path to the YAML resume source file. |
| `--language LANG` | No | value from YAML or `en` | ISO language code for UI strings (e.g. `fr`, `en`). Overrides the `language` field in the YAML file. |
| `--variant [yes\|no]` | No | value from YAML or `no` | Override the `variant` attribute (blue side panel). Defaults to the value from the YAML file, or `no` (`False`) if not set. |
