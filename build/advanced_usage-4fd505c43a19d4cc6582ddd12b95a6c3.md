# Advanced usage

[`uv`](https://docs.astral.sh/uv/) is a tool for creating virtual environments (along with many other features !) that can be useful for working on Alliance Canada resources.
For example, to download `uv` and [create a Python environment](https://docs.astral.sh/uv/pip/environments/) with [`datalad`](https://www.datalad.org/) installed:

```
# download uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# verify uv installation
uv -h

# create datalad venv
uv venv datalad --python=3.12

# activate datalad venv
source datalad/bin/activate

# install git-annex and datalad
uv pip install git-annex datalad

# verify datalad installation
datalad --help

# deactivate datalad venv
deactivate
```

We can then use this `datalad` environment to [access existing datasets on the local RIA store](https://handbook.datalad.org/en/latest/beyond_basics/101-147-riastores.html).
We will [use a `reckless --ephemeral` installation](https://docs.datalad.org/en/stable/generated/man/datalad-install.html#reckless-auto-ephemeral-shared) of the dataset such that we do not consume additional inodes, and our changes do not modify the original dataset.
As an example, to access the `cneuromod.things.fmriprep` dataset:

```
source datalad/bin/activate

# to install the cneuromod.things.fmriprep dataset from the Rorqual RIA store
datalad install --reckless 'ephemeral' ria+file://$HOME/links/projects/rrg-pbellec/ria-rorqual#~cneuromod.things.fmriprep
```