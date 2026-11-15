# 数据来源 / Dataset provenance

The underlying dataset is **Steel Plates Faults**, by M. Buscema, S. Terzi and W. Tastle (2010), UCI Machine Learning Repository. The official record describes 1,941 instances, 27 features and seven defect types.

- Dataset record: [UCI Steel Plates Faults](https://archive.ics.uci.edu/dataset/198/steel+plates+faults)
- Citation / DOI: [10.24432/C5J88N](https://doi.org/10.24432/C5J88N)
- Dataset licence: [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)

`steel-plates-faults.csv` is the existing CSV used by the supplied coursework notebook. It is copied byte-for-byte from that project, not freshly downloaded or relabelled. It has one `fault_type` target column; UCI's original distribution uses a different file layout. This packaging step does not independently reconstruct the earlier CSV conversion. All class codes, row order and values are retained.

本仓库保留课程项目现有 CSV 的原始字节，不重新下载、排序或改写类别。它与 UCI 原始文件的存储格式不同；本次打包未重新审计更早的 CSV 转换过程。

SHA-256:

```text
9e9bfebd2ea8bf84f5264325fadace2194387991183cb20d52075ef72e2c858e
```

Reproduction reads this local file and does not require a dataset service or network download. Internet access is needed only to install Python dependencies.
