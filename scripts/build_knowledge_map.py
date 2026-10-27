"""Build the v2 relation-aware, 36-node teaching map; v1 is archived."""
import argparse
from html import escape
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GROUPS = [
 ('化学问题与数据','#EDF3FB','#285A8A',[
  '真实课题与自主选题','活性标签与实验含义','分子结构与SMILES',
  '质量与类别比例','训练与验证划分','数据泄漏控制']),
 ('分子表示与融合','#EBF6F1','#286A56',[
  '分子图：原子与键','GNN独立表示（M0）','分子指纹与相似性',
  '化学空间训练参考图','N2V关系表示','融合模型（M1）']),
 ('比较与问题修订','#F1EEFA','#675394',[
  '模型预测输出','AP与AUROC指标','M0/M1同划分比较',
  '差异与异常观察','提出优化假设','依据证据修订问题']),
 ('学生自主设计搜索','#FFF3E5','#9A642C',[
  '设计候选策略空间','设定优化目标','明确保持不变的条件',
  '制定评价规则','安排资源与候选预算','规定停止条件']),
 ('人机协同迭代','#E9F5F8','#276E80',[
  'AI提出候选策略','策略合法性检查','可信程序执行训练',
  '开发评价与反馈','候选及失败记录','比较选择与方案冻结']),
 ('保留评价与科学判断','#FAEFF0','#945660',[
  '冻结后保留评价','对照与异常解释','结论及证据范围',
  '未来检验问题','学期研究过程档案','项目报告与个人答辩']),
]
BLUE='#3D76AD'; ORANGE='#CC7B22'; GREY='#8495A5'; GREEN='#35725C'

def build(font_path):
 root=Path(__file__).resolve().parents[1]; out=root/'assets'; out.mkdir(exist_ok=True)
 S=1.5; im=Image.new('RGB',(3600,2550),'white'); draw=ImageDraw.Draw(im)
 svg=['<svg xmlns="http://www.w3.org/2000/svg" width="2400" height="1700" viewBox="0 0 2400 1700" role="img" aria-labelledby="title desc">',
 '<title id="title">36节点知识与能力图谱v2：分组课题学期实践</title>',
 '<desc id="desc">六模块36节点；区分知识依赖、教学推进、开发反馈和能力递进。开发反馈回到候选提案，方案冻结后的最终保留评价不回流调参。</desc>',
 '<rect width="2400" height="1700" fill="white"/>']; fonts={}; positions={}; nodes=[]; edges=[]
 def f(size):
  if size not in fonts: fonts[size]=ImageFont.truetype(str(font_path),round(size*S))
  return fonts[size]
 def rect(x,y,w,h,fill,outline=None,r=14):
  draw.rounded_rectangle(tuple(round(t*S) for t in (x,y,x+w,y+h)),radius=round(r*S),fill=fill,outline=outline,width=2)
  svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{outline or fill}"/>')
 def text(x,y,t,size=25,color='#273746'):
  draw.text((round(x*S),round(y*S)),t,font=f(size),fill=color,anchor='mm')
  svg.append(f'<text x="{x}" y="{y}" font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif" font-size="{size}" fill="{color}" text-anchor="middle" dominant-baseline="central">{escape(t)}</text>')
 def line(points,color=GREY,width=3,dash=False,arrow=False):
  for (x1,y1),(x2,y2) in zip(points,points[1:]):
   if dash:
    length=math.hypot(x2-x1,y2-y1); steps=max(1,int(length/12))
    for k in range(0,steps,2):
     a=k/steps; b=min(k+1,steps)/steps
     draw.line(tuple(round(v*S) for v in (x1+(x2-x1)*a,y1+(y2-y1)*a,x1+(x2-x1)*b,y1+(y2-y1)*b)),fill=color,width=round(width*S))
   else: draw.line(tuple(round(v*S) for v in (x1,y1,x2,y2)),fill=color,width=round(width*S))
  pts=' '.join(f'{x},{y}' for x,y in points)
  svg.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="7 6"' if dash else '')+'/>')
  if arrow:
   x1,y1=points[-2]; x,y=points[-1]; angle=math.atan2(y-y1,x-x1)
   p=[(x,y),(x-11*math.cos(angle)+5*math.sin(angle),y-11*math.sin(angle)-5*math.cos(angle)),(x-11*math.cos(angle)-5*math.sin(angle),y-11*math.sin(angle)+5*math.cos(angle))]
   draw.polygon([(round(a*S),round(b*S)) for a,b in p],fill=color)
   svg.append('<polygon points="'+' '.join(f'{a},{b}' for a,b in p)+f'" fill="{color}"/>')
 text(1200,70,'AI辅助模型开发与优化',43)
 text(1200,127,'知识与能力图谱 · 学期制课题小组实践 · 32学时',29)
 text(1200,183,'以分子活性预测为课题，从模型比较走向AI辅助模型开发',24,'#637587')
 for x,color,label,dashed in [(75,BLUE,'知识依赖',True),(650,GREY,'教学推进',False),(1225,ORANGE,'开发反馈回路',False),(1800,GREEN,'能力递进',False)]:
  line([(x,247),(x+80,247)],color,4,dashed,True); text(x+230,247,label,24,color)
 for col,(title,light,dark,labels) in enumerate(GROUPS):
  x=60+380*col
  rect(x,320,360,70,dark); text(x+180,355,title,27,'white')
  if col<5: line([(x+363,355),(x+377,355)],GREY,3,False,True)
  for row,label in enumerate(labels):
   n=col*6+row+1; y=428+104*row
   rect(x+18,y,324,76,light); text(x+180,y+38,f'{n:02d}  {label}',22,dark)
   positions[n]=(x+18,y,324,76); nodes.append({'id':n,'module':col+1,'label':label})
 def dep(a,b,points=None):
  x,y,w,h=positions[a]; xx,yy,ww,hh=positions[b]
  line(points or [(x+w/2,y+h+2),(xx+ww/2,yy-3)],BLUE,2,True,True)
  edges.append({'from':a,'to':b,'relation':'knowledge_dependency'})
 dep(7,8); dep(9,10); dep(10,11); dep(11,12)
 x,y,w,h=positions[8]; xx,yy,ww,hh=positions[12]
 dep(8,12,[(x,y+h/2),(x-12,y+h/2),(x-12,yy+hh/2),(xx-1,yy+hh/2)])
 x,y,w,h=positions[12]; xx,yy,ww,hh=positions[13]
 dep(12,13,[(x+w,y+h/2),(x+w+29,y+h/2),(x+w+29,yy+hh/2),(xx-2,yy+hh/2)])
 dep(13,14); dep(14,15)
 x,y,w,h=positions[15]; xx,yy,ww,hh=positions[17]
 dep(15,17,[(x,y+h/2),(x-12,y+h/2),(x-12,yy+hh/2),(xx-1,yy+hh/2)])
 dep(17,18)
 for a,b in [(25,26),(26,27),(27,28)]:
  x,y,w,h=positions[a]; xx,yy,ww,hh=positions[b]
  line([(x+w/2,y+h+2),(xx+ww/2,yy-3)],ORANGE,3,False,True)
  edges.append({'from':a,'to':b,'relation':'development_process'})
 x,y,w,h=positions[28]; xx,yy,ww,hh=positions[25]
 line([(x+w,y+h/2),(x+w+12,y+h/2),(x+w+12,yy+hh/2),(xx+ww+1,yy+hh/2)],ORANGE,4,False,True)
 edges.append({'from':28,'to':25,'relation':'development_feedback'})
 text(1765,1122,'开发反馈可进入下一轮提案',21,ORANGE)
 # Selected/frozen policy leads only to held-out evaluation; there is no reverse edge.
 x,y,w,h=positions[30]; xx,yy,ww,hh=positions[31]
 line([(x+w/2,y+h+2),(x+w/2,1090),(x+w+29,1090),(x+w+29,yy+hh/2),(xx-2,yy+hh/2)],GREEN,4,False,True)
 edges.append({'from':30,'to':31,'relation':'freeze_then_holdout'})
 rect(1980,1063,320,51,'#FBE5E7'); text(2140,1088,'冻结后开展保留评价',22,'#A63D47')
 for a,b in [(15,18),(18,19),(19,25),(28,29),(29,30),(31,32),(32,33),(33,34),(33,36)]:
  edges.append({'from':a,'to':b,'relation':'teaching_process'})
 for a in [1,18,24,29,31,33]: edges.append({'from':a,'to':35,'relation':'process_evidence'})
 outcomes=['课题说明／表示图','基础模型／表示说明','比较表／问题修订','搜索问题卡与回应','候选档案／冻结记录','学期档案／评价报告']
 capabilities=['理解并界定问题','解释信息与模型','比较并提出假设','自主设计开发任务','协同探索与修订','依证据判断与表达']
 text(1200,1158,'阶段成果与教师反馈：提交 → 反馈 → 学生回应／修订',25)
 for col,label in enumerate(outcomes):
  x=60+380*col; rect(x,1200,360,68,'#F3F6F9'); text(x+180,1234,label,23)
 text(1200,1320,'能力递进（由相应模块与阶段产出支撑）',25,GREEN)
 for col,label in enumerate(capabilities):
  x=60+380*col; y=1420-col*10
  rect(x,y,360,60,'#EDF6F0'); text(x+180,y+30,label,23,GREEN)
  if col<5: line([(x+361,y+30),(x+378,y+20)],GREEN,3,False,True)
 text(1200,1530,'全过程档案（节点35）：最初问题 → 初始模型 → 策略修订 → 自动探索 → 验证与判断变化',24)
 text(1200,1592,'开发评价支持策略迭代，冻结后的保留评价用于检验研究结论',23,'#637587')
 text(1200,1642,'四川大学《化学人工智能实践》 · 化学分子活性预测项目',21,'#718294')
 assert len(nodes)==36
 model={'version':'v2','scope':'One topic group, semester-long 32 teaching hours; not a uniform whole-class assignment','nodes':nodes,'edges':edges,
 'outcomes':dict(enumerate(outcomes,1)),'capabilities':dict(enumerate(capabilities,1)),
 'forbidden_feedback':'Held-out evaluation (31) must not feed the current search (19-30).'}
 (out/'knowledge-map-v2.json').write_text(json.dumps(model,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 svg.append('</svg>'); (out/'knowledge-map.svg').write_text('\n'.join(svg)+'\n',encoding='utf-8'); im.save(out/'knowledge-map.png')
 (out/'knowledge-map-v2.svg').write_bytes((out/'knowledge-map.svg').read_bytes()); (out/'knowledge-map-v2.png').write_bytes((out/'knowledge-map.png').read_bytes())
 print('Built v2: 36 nodes; typed relations; 3600x2550 PNG and editable SVG/JSON')

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--font',default='C:/Windows/Fonts/msyh.ttc')
 build(Path(parser.parse_args().font))
