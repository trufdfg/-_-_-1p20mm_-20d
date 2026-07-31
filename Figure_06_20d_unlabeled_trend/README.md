# Figure 06 20 d无KF标签样品趋势观察

本文件夹用于复现论文新增图6。原始记录中曾出现1.13 mm液池厚度标签，经实验记录复核后确认为记录误写，所有取样单元的有效液池厚度统一校正为1.20 mm。因此，图6不再按厚度分层显示，也不将厚度作为模型或PCA解释变量。

## 文件说明

- `data_spectra_1p20mm_day_mean.csv`：统一1.20 mm液池条件下3、10、15、20、30 d样品的日均ε′谱，用于图6a。20 d无KF标签，仅作趋势观察。
- `data_unit_feature_1p9418.csv`：所有29个取样单元在1.9418 THz处的ε′均值、扫描数、统一液池厚度标签和KF标签状态，用于图6b。
- `data_pca_unit_scores.csv`：基于0.5–2.0 THz取样单元平均ε′谱获得的PCA得分，用于图6c。
- `data_pca_variance.csv`：PCA解释方差比例。
- `plot.py`：复现图6的Python脚本。

## 运行方式

```bash
python plot.py
```

运行后将生成：

- `Figure_06_20d_unlabeled_trend.png`
- `Figure_06_20d_unlabeled_trend.pdf`

## 解释边界

20 d样品有THz-TDS扫描记录，但缺少KF参考值。因此它只用于无标签趋势观察，不参与监督训练、测试、R²/RMSE/MAE误差计算或水分梯度留一验证。
