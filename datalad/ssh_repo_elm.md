## 🧠 Datalad for Students: Minimal Reproducible Workflow

### 📦 1. Create a Datalad Dataset for Data (on `elm`)

**On your local machine:**

```bash
datalad create -c text2git image10k-zooniverse
cd image10k-zooniverse
```

**Annex the big files (e.g. CSVs):**

```bash
echo "*.csv annex.largefiles=anything" >> .gitattributes
datalad save -m "Set annex rules for CSVs"
```

**Push data to `elm`:**

```bash
datalad create-sibling \
  --name elm \
  --site datalad \
  --sshurl ssh://elm/data/simexp/pbellec/image10k-zooniverse \
  --shared all

datalad push --to elm --data anything
```

**Push Git-only metadata to GitHub (optional):**

```bash
datalad create-sibling-github courtois-neuromod image10k-zooniverse \
  --github-organization courtois-neuromod \
  --access-protocol ssh

datalad push --to origin
```

---

### 👩‍💻 2. For Students: Install and Use

**Clone the dataset from GitHub or `elm`:**

```bash
# Option A: from GitHub (metadata only)
datalad install git@github.com:courtois-neuromod/image10k-zooniverse.git

# Option B: from elm (knows about the data)
datalad install ssh://elm/data/simexp/pbellec/image10k-zooniverse.git
```

**Navigate and get data:**

```bash
cd image10k-zooniverse
datalad get Zooniverse_Results_2022_01_28.csv
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
