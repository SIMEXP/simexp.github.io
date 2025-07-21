# simexp.github.io
Website of the laboratory for brain simulation and exploration (SIMEXP). The codebase of this website is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by] and is based on the [Myst Markdown](https://mystmd.org/) framework.

## Usage

### Building the book

If you'd like to develop and/or build the SIMEXP website, you should:

1. Clone this repository
2. Run `pip install -r content/requirements.txt` (it is recommended you do this within a virtual environment)
3. (Optional) Edit the books source files located in the `content/` directory
4. Run `myst build --html` to create the website

A fully-rendered HTML version of the book will be built in `_build/html/`. If a change is merged into `main`, a github action will automatically publish an updated version of the website. 

## Contributors

We welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/simexp/simexp.github.io/graphs/contributors).

## Credits

This project is created using the excellent open source [Jupyter Book project](https://jupyterbook.org/) and the [executablebooks/cookiecutter-jupyter-book template](https://github.com/executablebooks/cookiecutter-jupyter-book).
