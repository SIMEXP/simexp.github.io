# Project and data management

To improve projects workflow, we divide these in differents units of work of differents types.

## Work units types

### Datasets
These as standardized (BIDS*(-ish)*) from data collection instruments:
eg. `mario` (as a short for `mario.bids`), or `mario.crowdsourced_curiosity`
Those are produced by data manager for most instruments, but can be contributed to by other members:
- a student doing a collection of data on a crowdsourcing platform: create a new dataset repo
- adding physio data to a BIDS dataset: branch+PR to existing repo

#### template(s)
For BIDS we have [template](https://github.com/courtois-neuromod/bids_template)
If we try to BIDS-ify all data, these could be validated by custom-schema with the new validator.

### Standard Derivatives
These are reuseable units of work that can be produced by anyone in the lab for the purpose of data release or on the journey of their own project.
These use a standard pipeline, and after choosing sensible parameters should to be ran once and for all.
`mario.fmriprep` , `things.glmsingle`, `floc.rois`, `things.memory_glm`, `mario.rois_timeseries`.


#### template

The [template](https://github.com/courtois-neuromod/derivatives_template) contains placeholders `README` and `dataset_description.json` and some standard github workflows to be ran on the dataset (eg. deploy test, bids-validator...)

### Analysis:

This is a unit that tests hypotheses following the scientific method.

eg. `mario.training_dependent_rsa`, the README would say:
> Here we test that practice of mario induces some reinforcement of scene-specific RSA patterns.
> Hypotheses:
> - 1: ratio of intra-scene vs. inter-scenes RSA distances in regions xxx increases with time of practice measured as cumulative duration of gameplay in the study. Only scenes where mario does not die are used to avoid an obvious bias.
> - 2: ...

If possible it should rely on `mario.scenes_rsa` that would have extracted brainwise RSA patterns by scenes that could be reused by others.

#### template
Project should start by forking a project template (to be designed+ implemented)

```
+-- .github/worflows/<selected_code_quality_tools|auto-docker-build_and_push_to_gh_reg|deploy_tests...>
+-- Dockerfile # optional: builds environment to run the code+notebooks, can use other files (eg. requirements.txt for pip...)
+-- README.md
+-- docs/ # if there is a need for more docs than the README, maybe not necessary
+-- sourcedata/<submodules> # all raw and derivatives datasets stored here
+-- src
|    +-- my_module.py
|    +-- my_module_test.py # encouraged
|    +-- my_script.py
+-- notebooks # (well formatted notebooks, all cells ran in order)
+-- playground|sandbox # mess (eg. dirty notebooks) that is not covered by tests, nor to be reviewed, nor used as final results
```

From the SIMEXP template we will derive a more specific neuromod template with the super-dataset pre-installed in sourcedata, an analysis bootstrap would be:
- GH: create from template, choose a good name
- `datalad install -s url_of_the_new_repo`
- `cd new_repo_clone && datalad create -f -d .`
- `datalad get -n sourcedata/cneuromod/{friends,movie10}/{timeseries,annotations}`
- ... the workflow below ...

#### Workflow

Iterating on a `dev` branch, then when ready for review and passing tests, open a PR to `main`, tag @PIs and @others for review, iterate on `dev` branch to address review.
Merge PR when it is approved (as all or majority agree this is an interesting and scientifically valid piece of work).
This cycle is repeated to improve or add analysis.

To follow scientific method:

- create the repo, add a README stating the hypotheses you want to test and a short method for each -> PR+review
- write dirty code for hypothesis #1 in the playground, get some interesting things, move/clean it to src/notebooks -> PR+review
- write code for hypothesis #2 in the playground, move/clean it to src/notebooks -> PR+review
- add another hypothesis #3 +method in the README -> PR+review (should move fast)
- write code for hypothesis #3 in the playground , move/clean it to src/notebooks -> PR+review
- improve code to test hypothesis #2 -> PR+review

Master level: if you want to work on multiple hypotheses at the same time, create more branches+PRs.

If analysis differs too much (done some RSA, now want to do encoding), create a new analysis repo.

### Papers
Likely a myst-article.

eg. a repo named `smb1_practice_induced_rsa_pattern_stabilization` created from [neurolibre/mystical-article](https://github.com/neurolibre/mystical-article)
Links the analysis repo as submodule, uses small 3d brain maps, matrices, tsvs,... from it to generate figures.
