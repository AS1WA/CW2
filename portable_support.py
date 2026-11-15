"""Environment and immutable input checks for the portable project."""
from pathlib import Path, PurePosixPath
import hashlib
import importlib.metadata
import json
import sys


def verify_inputs(root):
    root = Path(root).resolve()
    manifest = json.loads((root/'input_manifest.json').read_text(encoding='utf8'))
    for relative, expected in manifest['files'].items():
        rel = PurePosixPath(relative)
        if rel.is_absolute() or '..' in rel.parts:
            raise ValueError('Invalid input path: '+relative)
        path = root.joinpath(*rel.parts).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise FileNotFoundError('Missing package input: '+relative)
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError('Changed package input: '+relative)
    return len(manifest['files'])


def check_environment(root):
    root = Path(root)
    expected = json.loads((root/'runtime_versions.json').read_text(encoding='utf8'))
    problems = []
    if sys.version_info[:2] != (3, 11):
        problems.append('Use Python 3.11; found '+sys.version.split()[0])
    for package, version in expected.items():
        try:
            actual = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            actual = 'not installed'
        if actual != version:
            problems.append(f'{package}: expected {version}, found {actual}')
    if problems:
        raise RuntimeError('\n'.join(problems)+'\nInstall requirements.txt in a Python 3.11 environment.')
    return expected


def check_cached_metrics(root):
    import numpy as np
    import pandas as pd
    from sklearn.metrics import accuracy_score, f1_score
    root = Path(root)
    verify_inputs(root)
    saved = json.loads((root/'final_test/test_metrics.json').read_text())
    prediction = pd.read_csv(root/'final_test/test_predictions.csv')
    accuracy = accuracy_score(prediction.truth, prediction.prediction)
    f1 = f1_score(prediction.truth, prediction.prediction, average='macro')
    np.testing.assert_allclose([accuracy, f1], [saved['test_accuracy'], saved['test_macro_f1']], atol=1e-14, rtol=0)
    assert len(prediction) == 389 and prediction.row_id.is_unique
    pastry = prediction[prediction.truth == 'pastry']
    assert len(pastry) == 32 and (pastry.prediction == 'pastry').sum() == 18
    assert saved['test_evaluation_count'] == 1 and saved['test_recall_constraint_pass'] is False
    return {'accuracy': accuracy, 'macro_f1': f1, 'pastry_recall': 18/32,
            'prediction_calls': 0, 'all_class_recall_target_met': False}
