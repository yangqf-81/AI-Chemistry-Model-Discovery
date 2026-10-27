"""Execute the foundation notebook in a real, project-local Jupyter kernel."""
import json
from pathlib import Path
import sys

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager

root = Path(__file__).resolve().parents[1]
source = root / 'notebooks/00_分子预测基础实验.ipynb'
kernel_root = root / 'outputs/kernels'
kernel = kernel_root / 'chem-practice'
kernel.mkdir(parents=True, exist_ok=True)
(kernel / 'kernel.json').write_text(json.dumps({
    'argv': [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
    'display_name': 'Project chemistry practice', 'language': 'python',
}), encoding='utf-8')
notebook = nbformat.read(source, as_version=4)
for index, cell in enumerate(notebook.cells):
    cell['id'] = f'foundation-{index + 1}'
nbformat.validate(notebook)
manager = KernelManager(
    kernel_name='chem-practice',
    kernel_spec_manager=KernelSpecManager(kernel_dirs=[str(kernel_root)]))
client = NotebookClient(notebook, km=manager, timeout=120,
                        resources={'metadata': {'path': str(root)}})
client.execute()
cells = [cell for cell in notebook.cells if cell.cell_type == 'code']
assert all(cell.execution_count is not None for cell in cells)
assert not any(output.output_type == 'error' for cell in cells for output in cell.outputs)
executed = root / 'outputs/00_分子预测基础实验.executed.ipynb'
nbformat.write(notebook, executed)
summary = {'status': 'PASS', 'code_cells': len(cells),
           'execution': 'Real Jupyter kernel via nbclient; not text-only cell simulation',
           'executed_notebook': executed.name}
(root / 'outputs/notebook-verification.json').write_text(
    json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))
