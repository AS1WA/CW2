from pathlib import Path
import argparse
import asyncio
import json
import os
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent
NOTEBOOK = ROOT/'ENG5338_CW2_notebook_GROUP_5_EN_PORTABLE.ipynb'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='Check environment and bundled inputs only.')
    parser.add_argument('--verify-cache', action='store_true', help='Recompute saved holdout metrics without prediction.')
    args = parser.parse_args()
    from portable_support import check_environment, verify_inputs, check_cached_metrics
    check_environment(ROOT)
    print('Verified package inputs:', verify_inputs(ROOT), flush=True)
    if args.verify_cache:
        print(json.dumps(check_cached_metrics(ROOT), indent=2))
        return
    if args.check:
        print('Environment and package checks passed.')
        return
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:
        os.environ[key] = '1'
    for key, folder in [('JUPYTER_RUNTIME_DIR','jupyter_runtime'),('IPYTHONDIR','ipython'),('MPLCONFIGDIR','matplotlib')]:
        local = ROOT/'qa'/folder
        local.mkdir(parents=True, exist_ok=True)
        os.environ[key] = str(local)
    import nbformat
    from nbclient import NotebookClient
    from nbconvert import HTMLExporter
    from jupyter_client import AsyncKernelManager
    from jupyter_client.kernelspec import KernelSpecManager
    n = nbformat.read(NOTEBOOK, as_version=4)
    for cell in n.cells:
        if cell.cell_type == 'code':
            cell.execution_count = None
            cell.outputs = []
            cell.metadata.pop('execution', None)
    first = next(c for c in n.cells if c.cell_type == 'code')
    first_source = first.source
    blocked = json.loads(os.environ.get('CW2_BLOCK_ROOTS_JSON', '[]'))
    if blocked:
        first.source = '''import sys as _audit_sys, os as _audit_os
_blocked_roots = __ROOTS__
def _deny_original_reads(event, args):
    if event == 'open' and args and isinstance(args[0], (str, bytes)):
        name = _audit_os.path.normcase(_audit_os.path.abspath(_audit_os.fsdecode(args[0])))
        for root in _blocked_roots:
            root = _audit_os.path.normcase(_audit_os.path.abspath(root))
            if name == root or name.startswith(root + _audit_os.sep):
                raise RuntimeError('Original-project access is blocked during relocation validation.')
_audit_sys.addaudithook(_deny_original_reads)
'''.replace('__ROOTS__', repr(blocked)) + first.source
    output = ROOT/'executed'
    output.mkdir(exist_ok=True)
    started = time.perf_counter()
    def progress(cell, cell_index, **kwargs):
        print(f'Completed cell {cell_index+1}/{len(n.cells)}; {time.perf_counter()-started:.1f}s', flush=True)
        nbformat.write(n, output/'progress.ipynb')
    try:
        with tempfile.TemporaryDirectory(prefix='cw2-kernel-', dir=ROOT/'qa') as temp:
            kernels = Path(temp)/'kernels'
            spec = kernels/'cw2-portable'
            spec.mkdir(parents=True)
            (spec/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],
                'display_name':'CW2 portable','language':'python'}), encoding='utf8')
            manager = KernelSpecManager(kernel_dirs=[str(kernels)])
            km = AsyncKernelManager(kernel_name='cw2-portable', kernel_spec_manager=manager)
            client = NotebookClient(n, km=km, kernel_name='cw2-portable', timeout=3600,
                resources={'metadata':{'path':str(ROOT)}}, on_cell_executed=progress)
            client.execute(cleanup_kc=True)
    except Exception:
        first.source = first_source
        nbformat.write(n, output/'failed.ipynb')
        raise
    first.source = first_source
    codes = [c for c in n.cells if c.cell_type == 'code']
    assert [c.execution_count for c in codes] == list(range(1,len(codes)+1))
    assert not any(o.output_type == 'error' for c in codes for o in c.outputs)
    nbformat.validate(n)
    result = output/(NOTEBOOK.stem+'.executed.ipynb')
    nbformat.write(n, result)
    html, _ = HTMLExporter().from_notebook_node(n)
    result.with_suffix('.html').write_text(html, encoding='utf8')
    summary = {'fresh_kernel':True,'code_cells':len(codes),'errors':0,
        'elapsed_seconds':time.perf_counter()-started,'original_project_reads_blocked':bool(blocked),
        'package_inputs_verified_after_execution':verify_inputs(ROOT),
        'cached_holdout_metrics':check_cached_metrics(ROOT)}
    (ROOT/'qa/execution_verification.json').write_text(json.dumps(summary,indent=2), encoding='utf8')
    print(json.dumps(summary,indent=2), flush=True)
    print('Executed notebook:', result, flush=True)


if __name__ == '__main__':
    main()
