"""Build a local, fixed-version application resource package from an allowlist."""
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
import zipfile

REPO = Path(__file__).resolve().parents[1]
PROJECT = REPO.parent
DEST = PROJECT/'交付'
DEST.mkdir(exist_ok=True)
OUTPUT = DEST/'04_四川大学_待署名_AI辅助模型开发与优化.zip'

tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=REPO).decode('utf-8').split('\0')
payload = {}
for name in tracked:
    if not name or name.startswith('assets/archive/') or name in {
        'docs/knowledge-map-v1.md', 'scripts/build_knowledge_map_v1.py',
        'scripts/package_resources.py'}:
        continue
    if (REPO/name).is_file():
        payload['AI-Chemistry-Model-Discovery/'+name] = (REPO/name).read_bytes()

# Include the local technical sample and case data specifically needed to run the package.
for directory in ['data/internal', 'examples/internal_historical']:
    for path in sorted((REPO/directory).iterdir()):
        if not path.is_file():
            continue
        data = path.read_bytes()
        if path.name == 'source_manifest.json':
            info = json.loads(data.decode('utf-8'))
            for row in info['files'].values():
                row['source'] = Path(row['source']).name
            data = (json.dumps(info, ensure_ascii=False, indent=2)+'\n').encode('utf-8')
        payload['AI-Chemistry-Model-Discovery/'+path.relative_to(REPO).as_posix()] = data

for relative in [
    'outputs/baseline/metrics.json', 'outputs/baseline/predictions.csv',
    'outputs/notebook-verification.json', 'outputs/learning-notebook-verification.json']:
    payload['AI-Chemistry-Model-Discovery/'+relative] = (REPO/relative).read_bytes()
for path in sorted((REPO/'outputs').glob('0[0-4]_*.executed.ipynb')):
    payload['AI-Chemistry-Model-Discovery/outputs/'+path.name] = path.read_bytes()

payload['申报材料/教学资源信息表.md'] = (PROJECT/'申报材料/教学资源信息表_内容初稿.md').read_bytes()
payload['校企合作说明.md'] = (REPO/'docs/cooperation.md').read_bytes()
payload['资源来源说明.md'] = (REPO/'docs/resource-sources.md').read_bytes()
payload['资源目录.md'] = '''# 教学资源目录

## AI辅助模型开发与优化——面向化学分子活性预测的项目制实践

| 内容 | 文件 |
|---|---|
| 教学资源信息表 | [信息表](申报材料/教学资源信息表.md) |
| 教学首页与运行方法 | [README](AI-Chemistry-Model-Discovery/README.md) |
| 正式教学设计 | [项目教学设计](AI-Chemistry-Model-Discovery/docs/teacher-guide.md) |
| 学期实施方案 | [32学时、16次活动](AI-Chemistry-Model-Discovery/docs/course-schedule.md) |
| 知识与能力图谱 | [高清图谱](AI-Chemistry-Model-Discovery/assets/knowledge-map-v2.png)与[SVG](AI-Chemistry-Model-Discovery/assets/knowledge-map-v2.svg) |
| 学生项目任务 | [任务书](AI-Chemistry-Model-Discovery/docs/project-brief.md)与[指南](AI-Chemistry-Model-Discovery/docs/student-guide.md) |
| 教学评价 | [量规](AI-Chemistry-Model-Discovery/docs/assessment.md) |
| 校企合作 | [合作说明](校企合作说明.md) |
| 资源来源 | [来源说明](资源来源说明.md) |

资源包按GitHub仓库结构组织。解压后从README选择教学与实践入口；基础分子数据、历史案例和环境说明随包提供。
'''.encode('utf-8')

commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO).decode().strip()
payload['版本信息.json'] = (json.dumps({
    'resource': 'AI辅助模型开发与优化——面向化学分子活性预测的项目制实践',
    'version': '2026-10-27-second-phase', 'source_commit': commit,
    'course_hours': 32, 'sessions': 16,
    'organization': 'Semester-long topic group in a class with multiple research groups',
}, ensure_ascii=False, indent=2)+'\n').encode('utf-8')
stream = io.StringIO(newline='')
writer = csv.writer(stream)
writer.writerow(['path', 'bytes', 'sha256'])
for name, data in sorted(payload.items()):
    writer.writerow([name, len(data), hashlib.sha256(data).hexdigest()])
payload['文件清单.csv'] = ('\ufeff'+stream.getvalue()).encode('utf-8')

with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as archive:
    for name, data in sorted(payload.items()):
        archive.writestr(name, data)
with zipfile.ZipFile(OUTPUT) as archive:
    assert archive.testzip() is None
    for name, data in payload.items():
        assert archive.read(name) == data
    assert not any('/.git/' in n or '/.venv/' in n or '/kernels/' in n for n in archive.namelist())
digest = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
(DEST/(OUTPUT.name+'.sha256')).write_text(digest+'  '+OUTPUT.name+'\n', encoding='utf-8')
print(json.dumps({'path': str(OUTPUT), 'files': len(payload), 'sha256': digest,
                  'source_commit': commit, 'crc_and_member_bytes': 'PASS'}, ensure_ascii=False, indent=2))
