# ENG5338 CW2 — 钢板缺陷分类 / Steel Plates Fault Classification

供老师复现小组实验的完整仓库：原中文版 notebook、中文便携入口、原数据集、冻结 SVM、历史结果和固定版本环境。原文件位于 [`original/ENG5338_CW2_notebook_GROUP_ID_ZH.ipynb`](original/ENG5338_CW2_notebook_GROUP_ID_ZH.ipynb)，按原始字节保留；运行请使用根目录的 [`ENG5338_CW2_notebook_GROUP_ID_ZH_PORTABLE.ipynb`](ENG5338_CW2_notebook_GROUP_ID_ZH_PORTABLE.ipynb)。

This repository contains the original Chinese notebook and a separate portable Chinese entry point, together with the dataset, frozen model, historical evidence and pinned dependencies. Use the root portable notebook to reproduce the experiment. The original is a byte-preserved reference.

## 1. 下载 / Download

```bash
git clone https://github.com/AS1WA/CW2.git
cd CW2
```

也可点击 GitHub **Code → Download ZIP**，完整解压到可写目录。不要仅下载 notebook；它需要同目录的数据、模型和缓存。

Alternatively, download and extract the complete ZIP into a writable directory. Downloading only the notebook is insufficient.

## 2. 安装环境 / Install the environment

推荐 Miniconda / Anaconda。原环境使用 Python 3.11.16；复现入口要求 Python 3.11。

```bash
conda create -n cw2-reproduce python=3.11 -y
conda activate cw2-reproduce
python -m pip install -r requirements.txt
python run_portable.py --check
```

或使用配置文件：`conda env create -f environment.yml`，然后 `conda activate cw2-reproduce`。

Already have Python 3.11? Use a virtual environment instead:

```bash
python -m venv .venv
```

Windows PowerShell：`.\.venv\Scripts\Activate.ps1`；macOS / Linux：`source .venv/bin/activate`。然后执行相同的 `pip install` 和 `--check` 命令。

Installation needs internet access. The repository includes environment specifications, not Python binaries or offline wheels. `requirements.txt` pins the runtime packages. `requirements-lock-windows.txt` records the complete original Windows pip environment; it is a Windows reference, not a cross-platform lock. All modelling code remains in the notebook.

Windows 上如需固定到本次全新安装验证的全部间接依赖，可将安装命令换成 `python -m pip install -r requirements-lock-tested-windows.txt`。该文件与 `validation/tested-environment-freeze-windows.txt` 一致。它和原电脑的环境快照分别保留。

For the complete Windows dependency set used by this fresh-install validation, install `requirements-lock-tested-windows.txt` instead. The original computer's freeze and the tested clean environment are recorded separately.

中文绘图优先使用 Microsoft YaHei。没有该字体时可安装 Noto Sans CJK；Linux 可使用系统的 `fonts-noto-cjk` 包。字体选择只影响显示。

For Chinese plot labels, install Microsoft YaHei or Noto Sans CJK. A missing CJK font affects label rendering, not model calculations.

## 3. 完整复现 / Run the full experiment

```bash
python run_portable.py
```

运行器用当前 Python 启动新内核，依次执行全部 22 个代码单元，并导出 notebook 和 HTML。需要几分钟，实际耗时取决于硬件与负载。不要同时运行多个完整实验。

The runner starts a fresh kernel with the current interpreter, executes all 22 code cells and exports an executed notebook and HTML. Allow several minutes. Avoid concurrent full runs.

交互运行 / Interactive use:

```bash
python -m ipykernel install --user --name cw2-portable --display-name "CW2 portable"
python -m jupyterlab ENG5338_CW2_notebook_GROUP_ID_ZH_PORTABLE.ipynb
```

选择 **CW2 portable**，重启内核并运行全部单元。也可在 VS Code 选择该 Python 环境。请从仓库根目录启动 JupyterLab。

Select **CW2 portable**, restart the kernel and run all cells. VS Code can use the same environment. Start JupyterLab from the repository root.

## 4. 快速核对 / Verify saved results only

```bash
python run_portable.py --check
python run_portable.py --verify-cache
```

第一条核对环境和不可变输入；第二条从已保存的 389 条留出集预测重新计算指标，不训练模型，也不调用模型预测。

`--check` verifies the environment and input hashes. `--verify-cache` recomputes metrics from the 389 saved holdout predictions without training or calling model prediction.

| 指标 / Metric | 保存结果 / Saved value |
|---|---:|
| Accuracy | 0.7480719794344473 |
| Macro F1 | 0.7817135463992829 |
| Pastry recall | 18/32 = 0.5625 |

pastry 的召回率未达到 0.60，所以该流水线不能称为满足全部约束的可部署系统。留出集曾在 CW1 和原 CW2 被使用，重放不构成新的独立测试。

Pastry recall fails the 0.60 target. This remains a development candidate, not a validated deployment-ready system. The holdout was previously exposed in CW1 and the original CW2; replay is not new independent validation.

## 5. 文件与输出 / Files and outputs

| 路径 / Path | 用途 / Purpose |
|---|---|
| `original/` | 原中文版，保留原有输出、成员信息和说明 / Byte-preserved source notebook |
| `data/steel-plates-faults.csv` | 原 CSV；1,941 行，27 个特征，7 类缺陷 / Original dataset |
| `archive/` | 冻结模型和历史选型、计时证据 / Frozen model and historical evidence |
| `final_test/` | 原始留出集预测和指标，运行时不覆盖 / Immutable holdout record |
| `reference/` | 对应原中文版运行的参考表、环境快照及适配清单 / Source-run reference tables and provenance |
| `input_manifest.json` | 输入的相对路径 SHA-256 清单 / Input integrity manifest |
| `validation/` | 本仓库验证证据 / Package validation evidence |
| `base/results/`, `supplement/results/` | 每次新训练与计时结果 / New development runs |
| `reproduced_holdout/` | 从保存预测重新计算的表和图 / Recomputed holdout tables and plots |
| `executed/` | 新执行的 notebook 与 HTML / Executed notebook and HTML |
| `qa/` | 当前运行的检查记录和内核临时目录 / Current-run verification |

运行产生的目录不作为历史证据覆盖上传。`distribution_manifest.json` 记录发布文件哈希。

Generated experiment directories are ignored by Git. `distribution_manifest.json` records the shipped file hashes.

## 6. 复现边界 / Reproduction scope

- 四模型：逻辑回归、RBF SVM、随机森林、直方图梯度提升。保留原预处理、参数、分层划分、随机种子 0 和五折交叉验证。
- 最终冻结模型：中位数填补、标准化、RBF SVM，`C=33.33333333333333`、`gamma=0.03`、`class_weight='balanced'`。
- 原 notebook 原样归档。便携入口改用包内相对路径检查、当前解释器、可用中文字体、按参数定位 SVM 代表配置，以及只读测试缓存。
- 跨电脑浮点差异写入 `supplement/results/<run>/reproduction_differences.csv` 和 `reproduction_diagnostics.json`，不隐瞒差异，不据此更换冻结模型。
- 训练与预测耗时随机器变化。历史计时、本次复现和实际目标硬件上的 20 ms 预算必须分开解释。
- 输入缺失或哈希变化会报错。不要删除 `final_test/` 来生成新的测试预测。
- 源 notebook 中已有成员、贡献和 AI 辅助说明原样保留；环境打包不代表重新核实个人贡献。

The algorithms, preprocessing, seed, splits and thresholds are retained. The portable entry adapts filesystem checks, kernel selection, fonts, parameter-based reference lookup, numerical diagnostics and read-only holdout replay. Numerical drift is reported explicitly. Input identity and saved prediction identity remain strict. Timing equality across computers is not guaranteed. Original member and AI-use statements are preserved as supplied.

仅加载你信任来源的 joblib 文件；本仓库校验所附原冻结模型的哈希。

Load joblib files only from trusted sources. This package verifies the bundled original model hash.


## 7. 验证结果 / Validation result

2026-11-15，在独立 Python 3.11.16 环境重新安装 107 个依赖包后，从含空格和中文的移位路径，以新内核执行全部 22 个代码单元：0 个错误，14 张图。运行时在 notebook 内核禁止读取原项目目录，22 项不可变输入保持原哈希。原 notebook 字节不变；故意改动 CSV 会被拒绝。389 条保存预测的准确率和宏平均 F1 核对通过，没有新增留出集预测。

On 2026-11-15, a fresh Python 3.11.16 environment installed 107 dependencies. A fresh kernel executed all 22 code cells from a relocated path with spaces and Chinese characters: zero errors and 14 figures. Original-project reads were blocked in the notebook kernel. All 22 manifest inputs retained their hashes, the original notebook remained byte-identical and an altered CSV was rejected. Saved holdout metrics were verified without new holdout prediction calls.

详见 [validation/package_verification.json](validation/package_verification.json)。这是本地 Windows 验证；未独立验证 macOS / Linux，也不保证其他电脑计时相同。

See the validation records for the actual run and numerical diagnostics. Validation covers local Windows, not independently tested macOS / Linux systems or cross-hardware timing guarantees.
