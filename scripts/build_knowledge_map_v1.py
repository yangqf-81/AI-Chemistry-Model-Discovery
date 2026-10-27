"""Build the one-page teaching map as editable SVG and a PNG preview."""
import argparse
from html import escape
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

GROUPS = [
    ('化学任务', '#EAF2FB', '#235A91', [
        '活性预测问题', '实验与标签含义', 'SMILES结构表达',
        '数据质量检查', '类别不平衡', '训练与验证划分']),
    ('分子表征', '#EAF6F1', '#25705C', [
        '原子与化学键', '分子图结构', 'GNN分子表示',
        '独立分子模型M0', '指纹与分子相似性', 'N2V参考信息']),
    ('比较与提问', '#F1EEFB', '#655099', [
        '融合模型M1', '模型预测结果', 'AP与AUROC',
        '基线对照比较', '收益与异常观察', '提出优化问题']),
    ('设计搜索', '#FFF3E6', '#9A6329', [
        '候选模型策略', '可改变的范围', '保持不变的条件',
        '评价目标设计', '资源与候选预算', '停止规则']),
    ('人机协同', '#E9F5F8', '#256E82', [
        '伐谋候选提案', '策略可用性检查', '程序训练模型',
        '指标评价与反馈', '记录候选与失败', '人工选择方案']),
    ('科学判断', '#FAEEEF', '#965760', [
        '选择后保留评价', '对照与异常分析', '结论的证据范围',
        '提出后续验证', '代码与结果版本', '报告与个人答辩']),
]


def build(font_path):
    root = Path(__file__).resolve().parents[1]
    output = root / 'assets'
    output.mkdir(exist_ok=True)
    canvas = Image.new('RGB', (1800, 1273), 'white')
    draw = ImageDraw.Draw(canvas)
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1273" '
           'viewBox="0 0 1800 1273" role="img" aria-labelledby="title desc">',
           '<title id="title">AI辅助模型开发与优化：36节点知识与能力图谱</title>',
           '<desc id="desc">从化学任务、分子表征、模型比较、搜索设计、人机协同走向科学判断。'
           '连线表示学习推进，不表示化学因果关系。</desc>',
           '<rect width="1800" height="1273" fill="white"/>']
    fonts = {}

    def font(size):
        if size not in fonts:
            fonts[size] = ImageFont.truetype(str(font_path), size)
        return fonts[size]

    def rect(x, y, w, h, fill, outline=None, radius=14):
        draw.rounded_rectangle((x, y, x+w, y+h), radius=radius,
                               fill=fill, outline=outline, width=2)
        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
                   f'fill="{fill}" stroke="{outline or fill}" stroke-width="2"/>')

    def text(x, y, content, size=24, fill='#243344'):
        bbox = draw.textbbox((0, 0), content, font=font(size))
        if bbox[2] - bbox[0] > 1704:
            raise ValueError('Text exceeds available page width')
        draw.text((x, y), content, font=font(size), fill=fill, anchor='mm')
        svg.append(f'<text x="{x}" y="{y}" text-anchor="middle" '
                   f'dominant-baseline="central" font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif" '
                   f'font-size="{size}" fill="{fill}">{escape(content)}</text>')

    def arrow(x1, y1, x2, y2, color='#B2BFCC'):
        draw.line((x1, y1, x2, y2), fill=color, width=3)
        if x1 == x2:
            points = [(x2-5, y2-8), (x2+5, y2-8), (x2, y2)]
        else:
            points = [(x2-8, y2-5), (x2-8, y2+5), (x2, y2)]
        draw.polygon(points, fill=color)
        svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                   f'stroke="{color}" stroke-width="3"/>')
        svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in points)+f'" fill="{color}"/>')

    text(900, 66, 'AI辅助模型开发与优化', 40)
    text(900, 119, '面向化学分子活性预测的项目制实践 · 知识／能力图谱', 27)
    for i, label in enumerate(['问题驱动：从模型差异中提问',
                               '人机协同：人定边界，AI提案',
                               '证据导向：用对照与验证判断']):
        rect(48+i*576, 172, 552, 58, '#F4F7FA')
        text(324+i*576, 201, label, 23)

    number = 0
    for column, (title, light, dark, nodes) in enumerate(GROUPS):
        x = 48 + column*288
        rect(x, 274, 264, 66, dark)
        text(x+132, 307, title, 27, 'white')
        if column < 5:
            arrow(x+267, 307, x+282, 307)
        for row, label in enumerate(nodes):
            number += 1
            y = 376 + row*92
            rect(x, y, 264, 68, light)
            text(x+132, y+34, f'{number:02d}  {label}', 22, dark)
            if row < 5:
                arrow(x+132, y+72, x+132, y+88)

    rect(48, 968, 1704, 94, '#F4F7FA')
    text(900, 998, '学习产出：问题说明 → 模型比较 → 搜索问题卡 → 候选记录 → 科学评价', 25)
    text(900, 1033, '反馈用于开发探索；方案选定后的保留评价不回流调参', 22, '#58697A')
    text(900, 1124, '教师拓展：ContextOff机制诊断、完整搜索审计、多seed与跨体系统计', 23, '#58697A')
    text(900, 1170, '32学时完整课程 · 以一个实际化学课题贯穿，不要求复做31体系', 22, '#58697A')
    text(900, 1214, '36个节点 · 连线表示学习推进，不表示化学因果 · 教学内容方案 v1.1', 20, '#7C8997')
    assert number == 36
    svg.append('</svg>')
    (output/'knowledge-map.svg').write_text('\n'.join(svg)+'\n', encoding='utf-8')
    canvas.save(output/'knowledge-map.png')
    print('Built one-page knowledge map: 36 nodes, 1800 x 1273')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font', default='C:/Windows/Fonts/msyh.ttc')
    build(Path(parser.parse_args().font))
