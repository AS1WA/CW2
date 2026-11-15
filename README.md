# ENG5338 CW2 — Group 5

Steel plate fault classification using logistic regression, RBF SVM, random forest and histogram gradient boosting. The repository includes the dataset, frozen model, reference results and pinned dependencies.

**Start with the [English notebook](ENG5338_CW2_notebook_GROUP_5_EN_PORTABLE.ipynb).** The default runner, `run_portable.py`, executes this English version.

## Download and install

Clone the repository, or use **Code → Download ZIP** and extract the complete folder. The notebook requires the accompanying data, model and saved predictions.

With Miniconda or Anaconda:

```bash
git clone https://github.com/AS1WA/CW2.git
cd CW2
conda create -n cw2-reproduce python=3.11 -y
conda activate cw2-reproduce
python -m pip install -r requirements.txt
python run_portable.py --check
```

Python 3.11 is required. Installation needs internet access; Python binaries and offline wheels are not bundled. For the complete dependency set used in the Windows validation, install `requirements-lock-tested-windows.txt` instead of `requirements.txt`. The original Windows environment is recorded separately in `requirements-lock-windows.txt`.

Alternatively, run `conda env create -f environment.yml`, then activate `cw2-reproduce`.

If Python 3.11 is already installed, create a virtual environment with `python -m venv .venv`. Activate it using `.\.venv\Scripts\Activate.ps1` in Windows PowerShell, or `source .venv/bin/activate` on macOS/Linux, then install `requirements.txt`.

## Run the English experiment

From the repository folder:

```bash
python run_portable.py
```

This starts a fresh kernel with the current Python interpreter and executes all 22 code cells in the English notebook. Allow several minutes, depending on hardware and load. `python run_english.py` is an equivalent explicit English entry point.

The executed notebook and HTML preview are written to `executed/`. New training and timing results are written to `base/results/` and `supplement/results/`. Recomputed holdout tables and figures are written to `reproduced_holdout/`.

For interactive use:

```bash
python -m ipykernel install --user --name cw2-portable --display-name "CW2 portable"
python -m jupyterlab ENG5338_CW2_notebook_GROUP_5_EN_PORTABLE.ipynb
```

Select **CW2 portable**, restart the kernel and run all cells. Start JupyterLab from the repository folder. VS Code can use the same Python environment.

## Verify the saved results

```bash
python run_portable.py --check
python run_portable.py --verify-cache
```

`--check` verifies package versions and input hashes. `--verify-cache` recomputes metrics from the 389 saved holdout predictions without training or making new predictions.

| Metric | Saved result |
|---|---:|
| Accuracy | 0.7480719794344473 |
| Macro F1 | 0.7817135463992829 |
| Pastry recall | 18/32 = 0.5625 |

The frozen pipeline uses median imputation, standardisation and RBF SVM with `C=33.33333333333333`, `gamma=0.03` and `class_weight='balanced'`. Pastry recall fails the 0.60 target, so the pipeline has not met all deployment constraints. The holdout was previously exposed in CW1 and the original CW2; replaying it is not new independent validation.

## Files and reference notebooks

| Path | Purpose |
|---|---|
| [English portable notebook](ENG5338_CW2_notebook_GROUP_5_EN_PORTABLE.ipynb) | Default runnable notebook |
| [English reference notebook](original/ENG5338_CW2_notebook_GROUP_5_EN.ipynb) | Translation retaining the Chinese source's recorded numerical results |
| [Chinese source notebook](original/ENG5338_CW2_notebook_GROUP_5_ZH.ipynb) | Archived source with Group 5 naming |
| `data/steel-plates-faults.csv` | Original CSV: 1,941 rows, 27 features and seven defect classes |
| `archive/` | Frozen SVM and historical selection and timing evidence |
| `final_test/` | Immutable saved holdout predictions and metrics |
| `reference/` | Source-run tables, environment records and provenance |
| `validation/` | Translation checks and execution evidence |
| `input_manifest.json` | SHA-256 checks for immutable inputs |
| `distribution_manifest.json` | Hashes of published files |

Generated experiment directories are ignored by Git. Missing or altered immutable inputs stop execution. Keep `final_test/` intact; reproduction reads the existing prediction record.

## Chinese version

The [Chinese portable notebook](ENG5338_CW2_notebook_GROUP_5_ZH_PORTABLE.ipynb) remains available with the same environment:

```bash
python run_chinese.py
```

Chinese plot labels require Microsoft YaHei or Noto Sans CJK. The default English notebook does not require a Chinese font.

## Validation and limits

The English portable notebook completed a fresh-kernel run on Windows with Python 3.11.16: **22 code cells, zero errors, 14 figures and 23 verified inputs**. The copied package ran from a separate path containing spaces and Chinese characters, while notebook-kernel reads of the original project folders were blocked. Saved holdout metrics were checked without new holdout predictions. See [English execution verification](validation/english_portable_execution.json) and [translation verification](validation/english_translation.json).

The default runner uses the same English execution code as that validated run. The reference translation preserves the source notebook's values; the portable notebook shows its separate reproduction results. Algorithms, parameters, preprocessing, seed and data splits are retained. Numerical differences are recorded in each new supplement run's `reproduction_differences.csv` and `reproduction_diagnostics.json`.

Training and prediction times depend on hardware and load. The 20 ms timing budget must be checked on the intended machine. macOS and Linux have not been independently validated. Load joblib files only from trusted sources; this package checks the bundled model's hash.
