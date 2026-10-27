"""Execute the four staged learning notebooks in project-local Jupyter kernels."""
import json
from pathlib import Path
import sys

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager

root = Path(__file__).resolve().parents[1]
kernel_root = root/'outputs/kernels'
kernel = kernel_root/'chem-practice'
kernel.mkdir(parents=True, exist_ok=True)
(kernel/'kernel.json').write_text(json.dumps({
    'argv': [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
    'display_name': 'Chemistry practice', 'language': 'python',
}), encoding='utf-8')
results = []
for source in sorted((root/'notebooks').glob('0[1-4]_*.ipynb')):
    notebook = nbformat.read(source, as_version=4)
    nbformat.validate(notebook)
    manager = KernelManager(kernel_name='chem-practice',
                            kernel_spec_manager=KernelSpecManager(kernel_dirs=[str(kernel_root)]))
    NotebookClient(notebook, km=manager, timeout=120,
                   resources={'metadata': {'path': str(root)}}).execute()
    cells = [c for c in notebook.cells if c.cell_type == 'code']
    assert all(c.execution_count is not None for c in cells)
    assert not any(o.output_type == 'error' for c in cells for o in c.outputs)
    nbformat.write(notebook, root/'outputs'/source.name.replace('.ipynb', '.executed.ipynb'))
    record = {'notebook': source.name, 'code_cells': len(cells), 'status': 'PASS'}
    results.append(record)
    print(json.dumps(record, ensure_ascii=False), flush=True)
assert len(results) == 4
(root/'outputs/learning-notebook-verification.json').write_text(
    json.dumps({'execution': 'Real Jupyter kernels; no online Famou call or new GNN training',
                'notebooks': results}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
