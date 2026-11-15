# 验证记录 / Validation evidence

This directory records validation of the Chinese portable package, separately from the original notebook's historical results.

- `fresh_install_report.json`: condensed pip report for the independent Python 3.11 environment, including downloaded package versions, wheel URLs and hashes. The environment does not inherit system site-packages. `pip check` passed.
- `tested-environment-freeze-windows.txt`: complete pip package set of that clean Windows environment; identical to root `requirements-lock-tested-windows.txt`.
- `execution_verification.json`: fresh-kernel execution summary, immutable input checks, source-byte identity, corrupted CSV rejection and recomputed cached holdout metrics.
- `base_completion.json`: completion record written after the four-model comparison's assertions passed.
- `execution_verification_supplement.json`: checks from the newly executed SVM supplement.
- `integration_checks_before_test.json`: reproduction checks before reading the saved holdout record.
- `reproduction_differences.csv`, `reproduction_diagnostics.json`: historical versus reproduced score and fitted-coefficient differences. A diagnostic mismatch is reported; it does not replace the frozen model.
- `updated_model_comparison.csv`, `updated_resource_comparison.csv`: this validation run's measurements, not the original selection evidence.

Notebook kernel access to the original integrated project, earlier English portable package and E:\CW2 is blocked during the relocation run. The fresh environment and copied package live in separate directories, with spaces and Chinese characters in the path. The original archived notebook and all manifest inputs are checked after execution.

本目录是便携入口的独立验证证据。历史数据见 `archive/` 和 `reference/`。全量执行不新增留出集预测；仅核对已有预测并重新计算指标。Windows 的本地验证不能替代 macOS / Linux 或老师电脑上的实际验证，耗时也不能跨硬件保证一致。
