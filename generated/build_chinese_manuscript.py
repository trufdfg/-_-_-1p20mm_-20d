# -*- coding: utf-8 -*-
from pathlib import Path
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.style import WD_STYLE_TYPE

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / '高压电缆终端硅油含水相关太赫兹介电响应与KF前快速筛查边界_中文SCI修改稿.docx'


def set_cell_text(cell, text, bold=False, size=9):
    cell.text = ''
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(str(text))
    r.bold = bold
    r.font.name = 'Times New Roman'
    r._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    r.font.size = Pt(size)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def set_repeat_table_header(row):
    trPr = row._tr.get_or_add_trPr()
    tblHeader = OxmlElement('w:tblHeader')
    tblHeader.set(qn('w:val'), 'true')
    trPr.append(tblHeader)


def set_table_borders(table, top=True, bottom=True, header_bottom=True):
    tblPr = table._tbl.tblPr
    borders = tblPr.first_child_found_in('w:tblBorders')
    if borders is None:
        borders = OxmlElement('w:tblBorders')
        tblPr.append(borders)
    for edge in ('left', 'right', 'insideH', 'insideV'):
        tag = 'w:' + edge
        el = borders.find(qn(tag))
        if el is None:
            el = OxmlElement(tag)
            borders.append(el)
        el.set(qn('w:val'), 'nil')
    for edge, enabled in (('top', top), ('bottom', bottom)):
        tag = 'w:' + edge
        el = borders.find(qn(tag))
        if el is None:
            el = OxmlElement(tag)
            borders.append(el)
        el.set(qn('w:val'), 'single' if enabled else 'nil')
        if enabled:
            el.set(qn('w:sz'), '12')
            el.set(qn('w:color'), '000000')
    if header_bottom and table.rows:
        tcPr_list = [c._tc.get_or_add_tcPr() for c in table.rows[0].cells]
        for tcPr in tcPr_list:
            tcBorders = tcPr.first_child_found_in('w:tcBorders')
            if tcBorders is None:
                tcBorders = OxmlElement('w:tcBorders')
                tcPr.append(tcBorders)
            bottom_el = OxmlElement('w:bottom')
            bottom_el.set(qn('w:val'), 'single')
            bottom_el.set(qn('w:sz'), '8')
            bottom_el.set(qn('w:color'), '000000')
            tcBorders.append(bottom_el)


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = 'PAGE'
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)


def add_line_numbering(section):
    sectPr = section._sectPr
    ln = sectPr.find(qn('w:lnNumType'))
    if ln is None:
        ln = OxmlElement('w:lnNumType')
        sectPr.append(ln)
    ln.set(qn('w:countBy'), '1')
    ln.set(qn('w:start'), '1')
    ln.set(qn('w:restart'), 'continuous')
    ln.set(qn('w:distance'), '360')


def set_run_font(run, east='宋体', latin='Times New Roman', size=10.5, bold=None, italic=None):
    run.font.name = latin
    run._element.rPr.rFonts.set(qn('w:eastAsia'), east)
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic


def add_body(doc, text, first_indent=True, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.line_spacing = 1.35
    pf.space_after = Pt(2)
    pf.space_before = Pt(0)
    if first_indent:
        pf.first_line_indent = Cm(0.74)
    r = p.add_run(text)
    set_run_font(r)
    return p


def add_heading(doc, text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(8 if level == 1 else 5)
    p.paragraph_format.space_after = Pt(3)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text)
    set_run_font(r, east='黑体', size=12 if level == 1 else 11, bold=True)
    return p


def add_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(5)
    r = p.add_run(text)
    set_run_font(r, size=9)
    return p


def add_figure(doc, rel_path, caption, width_cm=15.8):
    path = ROOT / rel_path
    if not path.exists():
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(f'[图文件未生成：{rel_path}]')
        set_run_font(r, size=9)
    else:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.keep_with_next = True
        p.add_run().add_picture(str(path), width=Cm(width_cm))
    add_caption(doc, caption)


def add_table_title(doc, title):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(title)
    set_run_font(r, size=9.5)


def add_reference(doc, idx, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.74)
    p.paragraph_format.first_line_indent = Cm(-0.74)
    p.paragraph_format.line_spacing = 1.1
    p.paragraph_format.space_after = Pt(1)
    r = p.add_run(f'[{idx}] {text}')
    set_run_font(r, size=8.5)


doc = Document()
sec = doc.sections[0]
sec.page_width = Cm(21.0)
sec.page_height = Cm(29.7)
sec.top_margin = Cm(2.2)
sec.bottom_margin = Cm(2.0)
sec.left_margin = Cm(2.5)
sec.right_margin = Cm(2.2)
sec.header_distance = Cm(1.0)
sec.footer_distance = Cm(1.0)
add_line_numbering(sec)
add_page_number(sec.footer.paragraphs[0])

styles = doc.styles
normal = styles['Normal']
normal.font.name = 'Times New Roman'
normal._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
normal.font.size = Pt(10.5)
normal.paragraph_format.line_spacing = 1.35

# Metadata
doc.core_properties.title = '高压电缆终端硅油含水相关太赫兹介电响应的样品间稳定性与KF前快速筛查边界'
doc.core_properties.subject = '中文SCI修改稿'
doc.core_properties.comments = '依据1.20 mm复现包、硕士论文和小论文手稿重构；删除无可追溯依据的R²=0.718。'

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(8)
r = p.add_run('高压电缆终端硅油含水相关太赫兹介电响应的\n样品间稳定性与KF前快速筛查边界')
set_run_font(r, east='黑体', size=16, bold=True)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('作者1，作者2，作者3*')
set_run_font(r, size=11)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('（1. 单位名称，城市 邮编；2. 单位名称，城市 邮编）')
set_run_font(r, size=9.5)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('*通信作者：________；Email：________')
set_run_font(r, size=9)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('基金项目：________')
set_run_font(r, size=9)

add_heading(doc, '摘  要', 1)
abstract = (
    '高压电缆充油终端硅油中的水分会改变液体绝缘介质的极化与损耗。卡尔·费休（Karl Fischer，KF）滴定是油中水分的参照测量方法，'
    '但其试剂消耗、取样控制和操作流程不利于大批量样品的首轮分流。本文将太赫兹时域光谱（THz–TDS）定位为KF确认前的辅助筛查工具，'
    '重点评价含水相关介电响应在独立制备样品之间的稳定性及不同验证层级下的模型适用边界。参考绝缘硅油自然吸湿方法制备样品，'
    '获得75、84、91、99和113 mg·kg⁻¹五个KF标定水平。23个独立制备油样共形成779条有标签技术重复谱，另有6个20 d无KF样品（187条谱）仅用于无监督趋势观察；'
    '全部透射测量均采用1.20 mm有效光程。梯度平均谱显示，水分增加伴随脉冲衰减、传播延迟和介电常数实部ε′的整体变化；五个梯度均值在1.9418 THz处的线性拟合R²约为0.867，'
    '但独立样品层面的分布重叠明显。五个KF水平的样品内/样品间综合变异系数为16.3%–33.7%。XGBoost在谱级探索性映射中得到R²=0.772、RMSE=5.18 mg·kg⁻¹；'
    '当完整留出一个KF水平时，各水平RMSE为8.4–30.0 mg·kg⁻¹，其中两个端点水平分别为30.0和27.0 mg·kg⁻¹，明显高于多数内部水平。'
    '六组未参与建模的在役油样KF值集中于79.10–80.43 mg·kg⁻¹，平均绝对误差为2.52 mg·kg⁻¹、平均相对误差为3.16%，但均呈非负偏差且样本范围狭窄。'
    '结果表明，THz介电谱能够提供低含水硅油的状态相关信号，但高谱级性能不能直接等同于跨样品或跨含水水平的通用定量能力。'
    '现阶段该方法更适合在同油种、同仪器和局部校准条件下开展排序、趋势比较和异常分流；接近行动界限、超出校准域、重复性不足或谱形异常的样品仍应转入KF确认。'
)
add_body(doc, abstract, first_indent=False)

p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(6)
r1 = p.add_run('关键词：')
set_run_font(r1, east='黑体', size=10, bold=True)
r2 = p.add_run('太赫兹时域光谱；绝缘硅油；含水状态；独立样品；数据泄漏；快速筛查；卡尔·费休')
set_run_font(r2, size=10)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Inter-sample stability of water-related terahertz dielectric responses in cable-terminal silicone oil and the boundary of pre-KF screening')
set_run_font(r, size=12, bold=True)

add_heading(doc, '1 引言', 1)
add_body(doc, '高压电缆充油终端具有复杂的电场界面和多材料绝缘结构，硅油承担外绝缘、散热与缓冲等功能。潮气进入终端后，水分可在液体与固体绝缘之间迁移，并通过提高介质极化和损耗、降低绝缘裕度等途径影响运行可靠性。因此，油中水分是终端状态评价中需要优先关注的变量之一[1–3]。')
add_body(doc, 'KF滴定能够直接给出水分参考值，适用于定量确认和争议样品仲裁。与此同时，KF分析依赖化学试剂、规范取样和操作时间。红外光谱、介电响应、超声及在线湿度传感等技术可提高检测效率，但其输出往往受到油种、温度、老化产物和校准转移的影响[4–8]。因此，更合理的工程路线并非简单以快速方法替代KF，而是利用快速方法完成首轮分流，再将临界、异常和不确定样品送入参照测量。')
add_body(doc, 'THz–TDS同时记录透射电场的幅度和相位，可获得折射率、吸收及复介电常数等信息。水分子的偶极取向和氢键网络集体运动在太赫兹频段产生宽带响应；合成油—水体系、变压器油、天然酯绝缘油和油纸绝缘研究均表明，含水变化能够引起THz传播延迟、吸收和介电参数变化[9–16]。对于绝缘硅油，已有极化—去极化电流研究证明自然吸湿会改变其介电响应，但针对高压电缆终端硅油的THz样品间稳定性仍缺乏充分讨论[17]。')
add_body(doc, '光谱建模中的另一个关键问题是实验单元定义。同一油样的多次扫描属于技术重复，彼此共享制备状态、装样条件和仪器背景。若将这些扫描随机分配至训练集和测试集，模型可能识别样品或测量批次的“指纹”，从而获得高于未知独立样品的表观性能。相关机器学习研究已指出，重复个体、重复测量或跨训练—测试预处理会造成信息泄漏和性能膨胀[18–20]。因此，光谱模型的证据强度必须与数据划分层级相匹配。')
add_body(doc, '基于上述认识，本文不以获得最高谱级R²为主要目标，而是回答三个问题：（1）75–113 mg·kg⁻¹范围内是否存在具有物理一致性的含水相关THz响应；（2）该响应在独立制备样品之间是否稳定；（3）谱级映射、完整含水水平留出和在役样品评价分别能够支持何种程度的筛查结论。由此建立“THz快速排序与异常分流—KF确认”的两阶段应用框架。')

add_figure(doc, 'composite_figures/Figure_01_workflow.png', '图1  THz–TDS预筛查与KF确认的两阶段研究流程。THz结果用于校准域内的排序、趋势比较和异常分流；临界、域外或不确定样品进入KF确认。')

add_heading(doc, '2 材料与方法', 1)
add_heading(doc, '2.1 预期用途与证据层级', 2)
add_body(doc, '本研究预先将THz–TDS定义为KF确认前的辅助筛查，而非KF替代方法。实验室样品用于建立介电响应、评价独立样品离散性并进行探索性映射；完整KF水平留出用于检验未见含水状态下的稳健性；在役油样仅用于观察同油种、窄区间内的局部适用性和基质偏移。所有指标均按照其评价层级解释，技术重复数量不等同于独立样品数量。')

add_heading(doc, '2.2 硅油样品制备与KF参照测量', 2)
add_body(doc, '样品制备参考王飞风等提出的绝缘硅油自然吸湿方法，并对真空干燥时间和吸湿温度作实验条件调整[17]。绝缘硅油首先在70 ℃、133 Pa条件下真空干燥96 h，以降低初始水分差异；随后置于25 ℃、80%相对湿度环境中自然吸湿，并在0、3、10、15和30 d取样。依据GB/T 7600—2014采用KF库仑法测定水分，得到75、84、91、99和113 mg·kg⁻¹五个有标签水平。20 d样品缺少KF结果，仅作为无监督趋势样品，不参与监督训练、特征选择、参数优化或误差计算。')
add_body(doc, '每个Excel工作簿对应一个独立制备油样，工作簿内多条光谱为该油样的技术重复。五个有标签水平分别包含2、7、4、7和3个独立样品，对应19、212、177、211和160条有效扫描，总计23个独立样品、779条有标签扫描。20 d无标签组包含6个独立样品、187条扫描。')

add_table_title(doc, '表1  有标签数据的独立样品与技术重复结构')
table = doc.add_table(rows=1, cols=4)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ['KF水分/(mg·kg⁻¹)', '吸湿时间/d', '独立样品数', '有效扫描数']
for i,h in enumerate(headers): set_cell_text(table.rows[0].cells[i], h, bold=True)
for row in [(75,0,2,19),(84,3,7,212),(91,10,4,177),(99,15,7,211),(113,30,3,160),('合计','—',23,779)]:
    cells = table.add_row().cells
    for i,v in enumerate(row): set_cell_text(cells[i], v)
set_repeat_table_header(table.rows[0]); set_table_borders(table)

add_heading(doc, '2.3 THz–TDS测量与1.20 mm液体样品池', 2)
add_body(doc, '透射测量采用QT–TO 1000太赫兹时域光谱系统。仪器预热60 min，密封测试空间相对湿度控制在35%以下；扫描频率25 Hz、时窗120 ps、采集点数12 000，并叠加100次。单条谱的仪器采集时间约30 s，该时间不包括取样、装样、清洗和KF测量。')
add_body(doc, '液体样品池由不锈钢基座、定位结构和聚乙烯窗口组成，间隔结构将有效光程固定为1.20 mm。原始反演程序始终采用1.20 mm；此前稿件中的5 mm属于文字记录错误，不涉及介电参数重新反演。样品池位置和方向通过机械定位保持一致，装样后检查气泡并密闭；空池参考和样品信号采用相同采集设置。')

add_heading(doc, '2.4 光学与介电参数反演', 2)
add_body(doc, '对时域信号采用统一脉冲窗口并进行快速傅里叶变换，得到参考复电场Eᵣ(ω)和样品复电场Eₛ(ω)。复传递函数H(ω)=Eₛ(ω)/Eᵣ(ω)同时保留幅度比和相位差。结合相同聚乙烯窗口的透射模型反演复折射率ñ=n+iκ，并计算吸收系数α=2ωκ/c及复介电常数ε*=ñ²，其中ε′=n²−κ²、ε″=2nκ。全部样品使用相同的d=1.20 mm和相位处理参数。')
add_body(doc, '本文以介电常数实部ε′作为主要分析变量，并利用时域峰值、频域幅值、折射率和吸收变化检验响应方向的一致性。不能反演、含非有限值或重复记录的数据在分析前剔除。')

add_heading(doc, '2.5 频段、样品间稳定性与模型评价', 2)
add_body(doc, '基于标准化ε′谱比较候选连续频段，0.5–2.0 THz被定义为信息相对集中且相位反演较稳定的解释性核心窗口，而不预设其为所有算法的唯一最优输入。1.9418 THz仅作为候选响应位置：五个KF梯度均值用于显示物理趋势，独立样品均值及其离散性用于评价该位置的样品间稳定性。')
add_body(doc, '样品间稳定性通过各KF水平独立样品特征的变异系数（CV）描述。探索性XGBoost映射使用复现包中既定的原始谱、导数及分段统计特征，现场样品不参与特征选择或调参。谱级映射用于衡量在现有样品域内的可学习性；完整KF水平留出则每次以其余四个水平训练，并将被留出的全部水平作为未见数据，以评价插值/端点外推边界。由于原稿中R²=0.718、RMSE=5.41 mg·kg⁻¹和MAE=3.67 mg·kg⁻¹缺乏可追溯计算文件，本文不再采用这些汇总指标，而直接报告复现包能够核验的谱级结果和各留出水平RMSE。')

add_heading(doc, '2.6 在役样品与统计解释', 2)
add_body(doc, '六组110 kV电缆终端在役硅油来自同一工程场景，KF水分为79.10–80.43 mg·kg⁻¹。每组进行30次重复扫描，南C为34次。现场样品不参与训练、频段选择或参数优化；评价指标为映射均值、绝对误差、相对误差和重复扫描标准差。由于现场KF范围过窄，不使用R²评价。')

add_heading(doc, '3 结果', 1)
add_heading(doc, '3.1 含水相关THz传播和介电响应', 2)
add_body(doc, '随KF标定水分由75 mg·kg⁻¹增加至113 mg·kg⁻¹，梯度平均谱总体表现为透射主脉冲幅值降低、到达时间后移以及主要能量频段幅值衰减。幅度和相位方向的一致变化说明，样品状态差异不仅体现为单一幅度漂移，还伴随传播相速度和能量耗散的改变。')
add_body(doc, '0.5–2.0 THz范围内的ε′平均谱呈弱频散背景，不同KF水平的平均曲线存在整体位移。1.9418 THz处五个梯度平均值的线性拟合R²约为0.867。该关系仅由五个梯度均值支撑，会压缩同一水平内的样品离散性，因此只能作为“存在可测含水相关介电响应”的物理证据，不能作为通用单频校准方程。')
add_figure(doc, 'composite_figures/Figure_02_spectral_response.png', '图2  低含水硅油的THz传播、介电响应及独立样品分布。a，时域透射波形；b，频域幅值谱；c，介电常数实部ε′；d，1.9418 THz处五个梯度均值关系；e，独立制备样品在1.94 THz处的均值及梯度汇总。')

add_heading(doc, '3.2 独立样品离散性限制单频解释', 2)
add_body(doc, '在独立样品层面，1.94 THz处的ε′分布出现明显重叠。同一KF水平内既存在重复扫描较稳定的样品，也存在均值偏移或扫描标准差较大的样品。例如，84 mg·kg⁻¹水平的独立样品均值跨越约1.27–2.93，99 mg·kg⁻¹水平跨越约1.28–2.80。五个KF水平的综合CV分别为16.3%、21.1%、19.6%、16.8%和33.7%，其中113 mg·kg⁻¹端点的离散性最高。')
add_body(doc, '该结果表明，梯度平均谱中的单调趋势与独立样品层面的稳定校准并非同一证据。自然吸湿过程、样品制备差异、装样状态、参考信号及系统漂移均可能与水分共同影响介电特征。因此，本文采用“含水相关响应”而不是“水分特异峰”的表述。')

add_heading(doc, '3.3 谱级可学习性不能替代完整水平验证', 2)
add_body(doc, '复现包中的XGBoost谱级映射包含158条测试记录，得到R²=0.772、RMSE=5.18 mg·kg⁻¹。多数记录分布于理想一致线附近，但残差分布存在长尾，说明少数样品或扫描状态可产生明显偏差。该结果证明多频介电信息在当前数据域内可被模型利用，但不等同于对新含水水平或新来源样品的独立泛化能力。')
add_body(doc, '完整KF水平留出后，75、84、91、99和113 mg·kg⁻¹的RMSE分别为30.0、16.2、8.4、9.3和27.0 mg·kg⁻¹。三个内部水平的平均RMSE为11.3 mg·kg⁻¹，而两个端点水平平均为28.5 mg·kg⁻¹。端点误差显著增大，说明当前模型更接近受限校准域内的局部映射器，对未见端点状态缺乏可靠外推能力。')
add_figure(doc, 'composite_figures/Figure_03_response_mapping.png', '图3  多频介电信息的探索性映射。a，候选频段综合得分；b，XGBoost谱级映射；c，残差分布；d，主要特征的重要性。谱级结果用于说明可学习性，不作为跨样品通用定量证据。')

add_heading(doc, '3.4 在役油样表现出局部可用性与一致正偏差', 2)
add_body(doc, '六组在役油样的KF值集中在79.10–80.43 mg·kg⁻¹，THz映射均值为79.37–85.38 mg·kg⁻¹。平均绝对误差为2.52 mg·kg⁻¹，平均相对误差为3.16%，各样品相对误差均低于7%；重复扫描标准差为1.96–4.21 mg·kg⁻¹。')
add_body(doc, '六组样品的映射值均不低于KF参考值，且南B、南C偏差较大。该一致正偏差更适合解释为实验室自然吸湿硅油与长期服役硅油之间的基质偏移，而不能据此宣称模型已经区分水分与老化产物。现场样品来自同一场景且KF范围狭窄，只支持局部插值和偏差观察。')
add_figure(doc, 'composite_figures/Figure_04_field_applicability.png', '图4  六组在役硅油的局部适用性。a，KF参考值与THz映射均值；b，Bland–Altman偏差；c，绝对误差；d，南北侧样品相对误差。误差线为重复扫描标准差。')

add_table_title(doc, '表2  六组在役终端硅油的局部适用性结果')
table = doc.add_table(rows=1, cols=7)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ['样品','KF/(mg·kg⁻¹)','THz映射/(mg·kg⁻¹)','绝对误差/(mg·kg⁻¹)','相对误差/%','扫描数','扫描SD/(mg·kg⁻¹)']
for i,h in enumerate(headers): set_cell_text(table.rows[0].cells[i], h, bold=True, size=8)
field_rows = [
    ('北A',80.03,80.15,0.12,0.15,30,3.16),('北B',80.43,82.28,1.85,2.30,30,3.21),('北C',79.10,79.37,0.27,0.34,30,2.63),
    ('南A',79.50,82.64,3.14,3.95,30,4.21),('南B',80.10,84.71,4.61,5.75,30,2.33),('南C',80.23,85.38,5.15,6.42,34,1.96),
    ('平均',79.90,82.42,2.52,3.16,'—',2.92)
]
for row in field_rows:
    cells = table.add_row().cells
    for i,v in enumerate(row): set_cell_text(cells[i], v, size=8)
set_repeat_table_header(table.rows[0]); set_table_borders(table)

add_heading(doc, '3.5 无KF的20 d样品只能用于趋势观察', 2)
add_body(doc, '20 d组的6个独立样品在1.9418 THz处均值约为1.35–2.63，其分布覆盖已标定样品的较宽范围，并未形成可直接赋予单一KF标签的紧密簇。该组在平均谱和PCA投影中的位置可以用于观察自然吸湿过程的连续性，但由于缺少参照值，任何监督预测或误差评价都会引入未经验证的伪标签。因此，20 d数据不进入模型训练、调参和性能计算。')
add_figure(doc, 'Figure_06_20d_unlabeled_trend/Figure_06_20d_unlabeled_trend.png', '图5  20 d无KF样品的无监督趋势。a，统一1.20 mm光程下不同吸湿时间的平均ε′谱；b，1.9418 THz独立样品分布；c，独立样品PCA投影。20 d样品以空心菱形表示。')

add_heading(doc, '3.6 证据边界和KF转检规则', 2)
add_body(doc, '数据层级对模型解释具有决定性影响。谱级映射回答“现有样品域内的光谱信息是否可被学习”；独立样品离散性回答“同一KF状态能否稳定复现”；完整水平留出回答“未见含水状态能否被可靠映射”；在役样品回答“实验室模型在相近工程基质中是否存在系统偏差”。四类证据不能相互替代。')
add_figure(doc, 'composite_figures/Figure_05_measurement_boundary.png', '图6  数据结构与测量边界。a，各KF水平的独立样品数和扫描记录数；b，水平内CV；c，完整KF水平留出RMSE；d，在役样品相对误差。')
add_body(doc, 'THz输出建议同时包括映射值、重复扫描离散度、校准域内/域外标记以及KF转检建议。以下情况应直接触发KF确认：结果接近设备行动界限；预测或特征向量超出训练域；重复扫描离散度异常；谱形、基线或相位行为与校准样品不一致；以及THz结果与历史趋势、外观或其他诊断量冲突。当前数据不足以建立通用二分类阈值，也不能计算可靠的灵敏度、特异度或阴性预测值。')

add_heading(doc, '4 讨论', 1)
add_heading(doc, '4.1 含水相关响应具有物理一致性，但不具水分专一性', 2)
add_body(doc, '水具有较大的偶极矩，其取向弛豫及氢键网络集体运动可在太赫兹频段贡献宽带介电响应[9,10,21]。在弱极性硅油背景中，水分状态变化可能同时影响透射幅度、相位和ε′，这解释了平均谱中衰减、延迟和介电基线变化的协同方向。然而，服役硅油中的酸、醇、醛等极性老化产物以及水分存在形态也会改变介电行为，因此本研究不能将1.9418 THz解释为水分专一吸收峰。')

add_heading(doc, '4.2 独立样品是模型评价的基本实验单元', 2)
add_body(doc, '每个工作簿对应一个独立制备油样，同一工作簿内扫描共享同一物理样品。随机拆分技术重复会降低训练集和测试集之间的真实差异，使模型有机会学习样品特异性或测量状态。数据泄漏研究表明，重复对象或不恰当的预处理可显著提高表观预测性能[18–20]。因此，本研究将谱级结果降为探索性证据，并用独立样品离散性和完整水平留出约束结论。')
add_body(doc, '本数据中，五个KF水平的独立样品数不均衡，最低仅2个，且端点覆盖不足。完整水平留出时端点RMSE达到27–30 mg·kg⁻¹，说明模型主要依赖校准域内的插值信息。对这类小样本、高维、重复谱数据，继续增加同一样品的扫描次数不能替代新增独立制备样品。')

add_heading(doc, '4.3 快速筛查应强调不确定性和转检机制', 2)
add_body(doc, '筛查工具的目标不是在所有情况下给出最终定量结论，而是快速识别优先级和不确定样品。在同油种、同仪器、同样品池和相近环境条件下，可利用THz介电谱进行批量排序和趋势比较；当结果接近运维界限或出现域外特征时，再由KF确认。这种流程利用了THz无需滴定试剂、可连续重复测量和同时提供幅相信息的优势，同时保留KF在定量确认中的参照地位。')
add_body(doc, '在役样品的平均误差较小，但其KF范围仅1.33 mg·kg⁻¹且全部来源于同一工程场景，不能证明模型适用于不同油批、不同老化程度或不同设备。正偏差可能提高KF转检率，也可能造成不必要复核；在缺少行动界限附近阳性/阴性样品时，不能将其解释为已证实的安全优势。')

add_heading(doc, '4.4 研究局限', 2)
add_body(doc, '本研究存在以下局限：（1）仅有五个KF标定水平，端点及阈值附近独立样品不足；（2）自然吸湿时间与KF水分高度相关，不能完全排除随时间共同变化的因素；（3）样品间CV较高，尚未通过跨日期、跨操作员和样品池更换验证再现性；（4）现场样品来源单一、含水范围狭窄；（5）现有复现包主要支持图表和既定映射结果，未保留原稿R²=0.718的完整计算链，因此本文删除该指标。上述限制决定了当前结论应停留在筛查可行性与适用边界，而非通用定量方法。')

add_heading(doc, '5 结论', 1)
add_body(doc, '（1）在统一1.20 mm液体样品池和受控测试条件下，不同KF标定状态的硅油在THz脉冲幅值、传播延迟和介电谱中表现出方向一致的状态相关变化，说明THz–TDS能够感知低含水硅油的介电状态差异。')
add_body(doc, '（2）五个梯度平均值在1.9418 THz处呈较高线性关系，但独立制备样品存在明显重叠，水平内CV为16.3%–33.7%。因此，梯度均值关系不能直接转化为稳定的单频定量方程。')
add_body(doc, '（3）XGBoost谱级映射得到R²=0.772、RMSE=5.18 mg·kg⁻¹；完整KF水平留出RMSE为8.4–30.0 mg·kg⁻¹，端点误差明显增大。高谱级性能不能等同于跨样品和跨含水水平的通用泛化能力。')
add_body(doc, '（4）六组在役油样表现出局部可用性和一致正偏差，但样本范围不足以支持广泛工程验证。当前方法适合作为同域、局部校准条件下的KF前排序、趋势比较与异常分流工具，不能替代KF作最终定量判定。')

add_heading(doc, '作者贡献', 1)
add_body(doc, '概念设计：________；实验实施：________；数据分析：________；软件与可视化：________；论文初稿：________；审阅与修改：________；项目管理：________。', first_indent=False)
add_heading(doc, '利益冲突', 1)
add_body(doc, '作者声明不存在利益冲突。/（请作者根据实际情况修改）', first_indent=False)
add_heading(doc, '数据与代码可用性', 1)
add_body(doc, '用于生成图1—图6的数据和绘图代码已公开存储于GitHub仓库：https://github.com/trufdfg/-_-_-1p20mm_-20d。原始仪器数据的开放范围由作者和所属单位根据数据管理要求确定。', first_indent=False)
add_heading(doc, '致谢', 1)
add_body(doc, '________。', first_indent=False)

add_heading(doc, '参考文献', 1)
refs = [
'Virtanen S, Callender G, Andritsch T. Characterization of silicone oil used in HV cable sealing ends. Proceedings of the Nordic Insulation Symposium, 2019, 26: 28–31.',
'Bergin E. Guidelines for maintaining the integrity of extruded cable accessories. In: Accessories for HV and EHV Extruded Cables. Springer, 2021: 257–315.',
'Ghani A B A, et al. Diagnostic criteria based on the correlation of DGA, moisture contents with PD and tan δ in MV oil-filled underground cable. IEEE International Conference on Dielectric Liquids, 2011: 1–4.',
'Zhao D, Zhu B, Li L, et al. A review of methods for measuring oil moisture. Measurement, 2023, 217: 113119. DOI: 10.1016/j.measurement.2023.113119.',
'全国电气化学标准化技术委员会. GB/T 7600—2014 运行中变压器油和汽轮机油水分含量测定法（库仑法）. 北京: 中国标准出版社, 2014.',
'Hadjadj Y, Fofana I, Van De Voort F R, Bussieres D. Potential of determining moisture content in mineral insulating oil by Fourier transform infrared spectroscopy. IEEE Electrical Insulation Magazine, 2016, 32: 34–39.',
'Kondalkar V V, Ryu G, Lee Y, Lee K. Development of a highly sensitive and stable humidity sensor for real-time monitoring of dissolved moisture in transformer-insulating oil. Sensors and Actuators B: Chemical, 2019, 286: 377–385. DOI: 10.1016/j.snb.2019.01.162.',
'Sangineni R, Nayak S K, Becerra M. A non-intrusive and non-destructive technique for condition assessment of transformer liquid insulation. IEEE Transactions on Dielectrics and Electrical Insulation, 2022, 29: 693–700.',
'Gorenflo S, Tauer U, Hinkov I, et al. Dielectric properties of oil–water complexes using terahertz transmission spectroscopy. Chemical Physics Letters, 2006, 421: 494–498. DOI: 10.1016/j.cplett.2006.01.108.',
'Fu X, et al. Applications of terahertz spectroscopy in the detection and recognition of substances. Frontiers in Physics, 2022, 10: 869537.',
'蒋强, 王玥, 文哲, 等. 太赫兹时域光谱技术的变压器油低水含量检测. 光谱学与光谱分析, 2018, 38: 1049–1052.',
'Luo G, Chen Q, He Y, et al. Detection of moisture content in insulating oil based on terahertz technology. IEEE International Conference on High Voltage Engineering and Applications, 2022: 1–4.',
'Wang T, Yin J, Cheng L, et al. A novel method to measure moisture content in transformer oil based on terahertz technology. IEEE International Conference on High Voltage Engineering and Application, 2020: 1–4.',
'Wang H, Yin J, Cheng L, et al. A non-destructive testing method for moisture content of oil-paper insulation based on terahertz dielectric response. IEEE Conference on Electrical Insulation and Dielectric Phenomena, 2019: 741–744.',
'成立, 夏彦卫, 高树国, 等. 太赫兹时域光谱技术在绝缘纸板微水含量检测中的应用分析. 智慧电力, 2020, 48: 104–109.',
'Wang L, Qi Z, Li Z, Guo L. THz optical parameters of FR3 natural ester insulating oil after thermal aging. Optik, 2021, 239: 166873. DOI: 10.1016/j.ijleo.2021.166873.',
'王飞风, 郭金明, 田树军, 卓浩泽. 微水含量及老化状态对绝缘硅油介电特性的影响. 中国电力, 2022, 55(3): 48–56. DOI: 10.11930/j.issn.1004-9649.202109137.',
'Kapoor S, Narayanan A. Leakage and the reproducibility crisis in machine-learning-based science. Patterns, 2023, 4: 100804.',
'Bernett J, Blumenthal D B, Grimm D G, et al. Guiding questions to avoid data leakage in biological machine learning applications. Nature Methods, 2024, 21: 1444–1453. DOI: 10.1038/s41592-024-02362-y.',
'Spisak T, et al. Data leakage inflates prediction performance in connectome-based machine learning models. Nature Communications, 2024, 15: 1829. DOI: 10.1038/s41467-024-46150-w.',
'Chen T, Guestrin C. XGBoost: A scalable tree boosting system. Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 2016: 785–794.',
'Jolliffe I T, Cadima J. Principal component analysis: a review and recent developments. Philosophical Transactions of the Royal Society A, 2016, 374: 20150202.',
'Wang J, Wang H, Cheng L, et al. Terahertz relaxation polarization modeling of micro-water inside nano-modified dielectrics and imaging distribution of free/bound water. Polymer Testing, 2023, 122: 108031.',
'Zhang W, et al. Aging behaviors of insulating silicone oil for cable terminals based on chromatographic and spectroscopic analysis. PLOS ONE, 2025, 20: e0334552.',
'Neimanis R, Eriksson R, Papazyan R. Diagnosis of moisture in oil/paper distribution cables—Part II: Water penetration in cable insulation. IEEE Transactions on Power Delivery, 2004, 19: 15–20.',
'Joeres R, Blumenthal D B, Kalinina O V. Data splitting to avoid information leakage with DataSAIL. Nature Communications, 2025, 16: 3337. DOI: 10.1038/s41467-025-58606-8.'
]
for i,ref in enumerate(refs,1): add_reference(doc,i,ref)

# Final paragraph style cleanup
for p in doc.paragraphs:
    for run in p.runs:
        if run.font.size is None:
            set_run_font(run)

# Disable widow control only for captions; keep paragraphs together where possible
for p in doc.paragraphs:
    pPr = p._p.get_or_add_pPr()
    widow = OxmlElement('w:widowControl')
    widow.set(qn('w:val'), '1')
    pPr.append(widow)

doc.save(OUT)
print(OUT)
