# FEPyio - Python library for FEBio

## Getting Started

1. Install Python 3.9
2. Install Poetry according to: [python-poetry/poetry#installation](https://github.com/python-poetry/poetry#installation).
    > You may need to restart your environment for changes to take effect
3. Clone this project and navigate to its folder
4. Setup Poetry
    1. Set the Poetry config:

        ```bash
        poetry config virtualenvs.in-project true --local
        ```

        > You may ommit the `--local` flag if you want to set the option globally

    2. (Optional) If you do not have an explicit reference to Python 3.9 in your
       path and it is not your default version of Python, run:

        ```bash
        poetry env use path/to/python39
        ```

        > On Windows, this is probably:
        >
        > ```bash
        > poetry env use %LOCALAPPDATA%\Programs\Python\Python39\python.exe
        > ```

    3. Install Python dependencies

        ```bash
        poetry install
        ```

5. Install Pre-Commit hooks

    ```bash
    pre-commit install
    ```

6. Copy and rename all `.vscode/*.template.json` files to `.vscode/*.json`
   i.e: `.vscode/tasks.template.json` -> `.vscode/tasks.json`
