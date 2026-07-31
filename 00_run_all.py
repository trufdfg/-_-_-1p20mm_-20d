# -*- coding: utf-8 -*-
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
scripts = sorted([p for p in ROOT.rglob('plot.py')])
print('将运行子图脚本数量：', len(scripts))
for p in scripts:
    print('\n运行：', p.relative_to(ROOT))
    subprocess.run([sys.executable, str(p)], check=True)

composite = ROOT / 'composite_figures' / 'plot_composite_figures.py'
print('\n运行整图合成脚本：', composite.relative_to(ROOT))
subprocess.run([sys.executable, str(composite)], check=True)
print('\n全部图片复现完成。Fig.1-Fig.5整图由composite_figures合成，Fig.6由Figure_06_20d_unlabeled_trend/plot.py直接输出。')
