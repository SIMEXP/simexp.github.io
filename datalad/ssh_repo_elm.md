## 🧠 Datalad for Students: Minimal Reproducible Workflow

### 📦 1. Create a Datalad Dataset for Data (on `elm`)

**On your local machine:**

```bash
datalad create -c text2git REPONAME
cd REPONAME
```

**Annex the big files (e.g. CSVs):**
It is important to properly configure `.gitattributes` such that the right files get annexed. The `text2git` configuration typically configures text files to be stored in `git` instead of being annexed. More info in the [datalad documentation](https://handbook.datalad.org/en/latest/basics/101-124-procedures.html). But you may want to manually set rules to ensure the content you want annexed indeed is. For example if you plan to store you data in `csv` files:

```bash
echo "*.csv annex.largefiles=anything" >> .gitattributes
datalad save -m "Set annex rules for CSVs"
```

**Add data to the repository:**
You can just add files in the repository and save its current state with the following command:
```
datalad save -m "Adding some data"
```
**Create a new sibling of the repository on `elm`:**
(update the path to a location under your own USERNAME):
```bash
datalad create-sibling \
  --name elm \
  ssh://elm/data/simexp/USERNAME/REPONAME \
  --existing=skip \
```
**Push data to `elm`:**
You can now easily maintain a versionized backup of your data on elm.
```
datalad push --to elm
```

**Create a github record of meta-data:**
First, create a repo called REPONAME on github, under some organization ORGNAME (for example `courtois-neuromod`). Keep it blank, no README or LICENSE. Then, add this repo as sibling of the dataset:
```bash
datalad siblings add -s origin --url git@github.com:ORGNAME/REPONAME.git
```

**Push Git-only metadata to GitHub (optional):**
It is now easy to push metadata to github:
```
datalad push --to origin
```
Note that if you misconfigured datalad you may push sensitive data on github. First, check using `ls -alsh` that the sensitive data appears as links pointing to git-annex rather than actual files. Second, start by making the repo private until you're share no sensitive data was pushed by mistake. If you pushed sensitive data by mistake, just delete the repository and start fresh if you can. Otherwise you'll need to edit the git+git-annex history of the repository, good luck :/

---

### 👩‍💻 2. For Students: Install and Use

**Clone the dataset from GitHub or `elm`:**

```bash
# Option A: from GitHub (metadata only)
datalad install git@github.com:courtois-neuromod/image10k-zooniverse.git

# Option B: from elm (with the actual data)
datalad install ssh://elm/data/simexp/pbellec/image10k-zooniverse.git
```

**Navigate and get data:**

```bash
datalad get EXAMPLEFILE.csv
```

---

### 🖼 3. Managing Outputs (Optional)

**Create a separate dataset for outputs:**

```bash
datalad create image10k-zooniverse.plots
cd image10k-zooniverse.plots

echo "*.png annex.largefiles=anything" >> .gitattributes
datalad save -m "Track plots in annex"
```

**Link it back into the analysis repo:**

```bash
cd image10k-zooniverse
datalad install -d . -s ../image10k-zooniverse.plots plots
```

---

### ⚠️ Tips & Troubleshooting

* If `datalad get` fails with `annex-ignore`, you likely cloned from GitHub only. Clone once from `elm` to propagate sibling config.
* To inspect siblings:

```bash
datalad siblings
```

* To pull subdataset updates:

```bash
datalad update --merge
```
