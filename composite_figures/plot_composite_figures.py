# -*- coding: utf-8 -*-
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Patch
BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":9, "axes.linewidth":1.0, "xtick.direction":"out", "ytick.direction":"out", "pdf.fonttype":42, "ps.fonttype":42})
COLORS={"blue":"#1f5a99","orange":"#d9822b","green":"#3b8a5a","purple":"#7f5aa6","red":"#b73a4a","gray":"#5b6670","dark":"#111827","lightgray":"#e5e7eb"}
def clean(ax, axis='y'):
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    if axis: ax.grid(axis=axis, color='#e5e7eb', linewidth=0.6, zorder=0)
def load(rel): return pd.read_csv(ROOT/rel/'data.csv')
def save(fig, name):
    fig.tight_layout(pad=0.8)
    fig.savefig(BASE/f'{name}.png', dpi=600, bbox_inches='tight')
    fig.savefig(BASE/f'{name}.pdf', bbox_inches='tight')
    print('saved', BASE/f'{name}.png')

def figure1():
    df=load('Figure_01_workflow')
    fig,ax=plt.subplots(figsize=(8.2,3.6),dpi=300); ax.set_axis_off()
    for _,r in df.iterrows():
        x,y,w,h=r['x'],r['y'],r['w'],r['h']; col=COLORS[r['color']]
        box=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.015,rounding_size=0.018',linewidth=2,edgecolor=col,facecolor='white'); ax.add_patch(box)
        ax.text(x+w/2,y+h*.66,r['title'],ha='center',va='center',fontsize=13,fontweight='bold',color=col)
        ax.text(x+w/2,y+h*.35,r['subtitle'],ha='center',va='center',fontsize=10.5,color=COLORS['dark'])
    def arrow(p1,p2): ax.add_patch(FancyArrowPatch(p1,p2,arrowstyle='-|>',mutation_scale=16,linewidth=1.4,color=COLORS['gray']))
    arrow((.33,.73),(.38,.73)); arrow((.66,.73),(.71,.73)); arrow((.85,.62),(.85,.44)); arrow((.71,.33),(.66,.33)); arrow((.38,.33),(.33,.33))
    ax.text(.05,.05,'Trace-water screening workflow for silicone oil in high-voltage cable terminals',fontsize=12.5,color=COLORS['dark'])
    ax.set_xlim(0,1); ax.set_ylim(0,1); save(fig,'Figure_01_workflow')

def figure2():
    fig=plt.figure(figsize=(7.2,5.2),dpi=300)
    gs=fig.add_gridspec(2,3,wspace=.42,hspace=.52)
    axs=[fig.add_subplot(gs[0,0]),fig.add_subplot(gs[0,1]),fig.add_subplot(gs[0,2]),fig.add_subplot(gs[1,0]),fig.add_subplot(gs[1,1])]
    style={75:'-',84:'--',91:'-.',99:':',113:'--'}; col={75:COLORS['blue'],84:COLORS['orange'],91:COLORS['green'],99:COLORS['purple'],113:COLORS['red']}
    df=load('Figure_02/fig2a_time_domain')
    for k,g in df.groupby('kf_mgkg'): axs[0].plot(g.time_ps,g.amplitude_au,style[int(k)],lw=1.0,color=col[int(k)],label=f'{int(k)} mg kg$^{{-1}}$')
    axs[0].set(xlabel='Time (ps)',ylabel='Amplitude (a.u.)',xlim=(-5,120),ylim=(-1100,2050)); clean(axs[0])
    df=load('Figure_02/fig2b_frequency_domain')
    for k,g in df.groupby('kf_mgkg'): axs[1].plot(g.frequency_thz,g.amplitude_db,style[int(k)],lw=1.0,color=col[int(k)])
    axs[1].set(xlabel='Frequency (THz)',ylabel='Amplitude (dB)',xlim=(0,3),ylim=(-205,10)); clean(axs[1])
    df=load('Figure_02/fig2c_dielectric_spectra')
    for k,g in df.groupby('kf_mgkg'): axs[2].plot(g.frequency_thz,g.eps_real,style[int(k)],lw=1.0,color=col[int(k)])
    axs[2].set(xlabel='Frequency (THz)',ylabel=r"Dielectric constant, $\epsilon'$",xlim=(.5,2.0),ylim=(.55,2.45)); clean(axs[2])
    df=load('Figure_02/fig2d_sensitive_frequency_fit'); x=df.kf_mgkg.to_numpy(); y=df.eps_real_1p9418.to_numpy(); coef=np.polyfit(x,y,1); xx=np.linspace(72,116,100); axs[3].scatter(x,y,s=24,color=COLORS['blue'],edgecolor='white',linewidth=.4,zorder=3); axs[3].plot(xx,np.polyval(coef,xx),color=COLORS['red'],lw=1.1); r2=1-((y-np.polyval(coef,x))**2).sum()/((y-y.mean())**2).sum(); axs[3].text(75,1.47,'1.9418 THz\n$R^2$ = %.3f'%r2,fontsize=8); axs[3].set(xlabel=r'KF moisture (mg kg$^{-1}$)',ylabel=r"Dielectric constant, $\epsilon'$",xlim=(73,115),ylim=(1.03,1.52)); clean(axs[3])
    df=load('Figure_02/fig2e_sample_unit_distribution')
    df['cell_thickness']=1.20
    axs[4].scatter(df.kf_mgkg,df.eps_real_1p94_mean,s=24,color=COLORS['blue'],edgecolor='white',linewidth=.4,alpha=.92,zorder=3)
    summary=df.groupby('kf_mgkg').eps_real_1p94_mean.agg(['mean','std']).reset_index()
    axs[4].errorbar(summary.kf_mgkg,summary['mean'],yerr=summary['std'],fmt='o',ms=4.2,color=COLORS['orange'],ecolor=COLORS['gray'],elinewidth=1.0,capsize=2.0,label='Gradient mean ± SD',zorder=4)
    axs[4].set(xlabel=r'KF moisture (mg kg$^{-1}$)',ylabel=r"Sampling-unit $\epsilon'$ at 1.94 THz",xlim=(70,118),ylim=(1.15,3.05)); clean(axs[4])
    for label,ax in zip('abcde',axs): ax.text(-.16,1.08,label,transform=ax.transAxes,fontweight='bold',fontsize=11,va='top')
    fig.legend(*axs[0].get_legend_handles_labels(), loc='upper center', ncol=5, frameon=False, bbox_to_anchor=(0.5,1.04), fontsize=8)
    save(fig,'Figure_02_spectral_response')

def figure3():
    fig,axs=plt.subplots(2,2,figsize=(7.0,5.2),dpi=300)
    ax=axs[0,0]; df=load('Figure_03/fig3a_pca_band_screening').iloc[::-1]; ax.barh(df.candidate_band,df.composite_score,color=COLORS['blue']); ax.set(xlabel='Composite score',ylabel='Candidate band',xlim=(0,.9)); clean(ax,'x')
    ax=axs[0,1]; df=load('Figure_03/fig3b_xgboost_mapping'); pal={75:COLORS['blue'],84:COLORS['orange'],91:'#55aa5a',99:'#9b7ac9',113:'#e84a5f'}
    for k,g in df.groupby('kf_mgkg'): ax.scatter(g.kf_mgkg,g.mapped_moisture_mgkg,s=18,color=pal[int(k)],alpha=.85,edgecolor='white',linewidth=.2)
    ax.plot([70,117],[70,117],ls='--',color=COLORS['gray'],lw=1); ax.text(72.5,114,'$R^2$=0.772\nRMSE=5.18',fontsize=8); ax.set(xlabel=r'KF moisture (mg kg$^{-1}$)',ylabel=r'Mapped moisture (mg kg$^{-1}$)',xlim=(70,117),ylim=(69,117)); clean(ax)
    ax=axs[1,0]; df=load('Figure_03/fig3c_residual_distribution'); ax.hist(df.residual_mgkg,bins=np.arange(-40,22,5),color=COLORS['blue'],edgecolor='white',linewidth=.4); ax.axvline(df.residual_mgkg.mean(),color=COLORS['orange'],lw=1.2,ls='--'); ax.axvline(0,color=COLORS['gray'],lw=1,ls='--'); ax.text(-35,88,'mean=%.2f'%df.residual_mgkg.mean(),fontsize=8); ax.set(xlabel=r'Residual (mapped - KF, mg kg$^{-1}$)',ylabel='Scan count',xlim=(-40,20)); clean(ax)
    ax=axs[1,1]; df=load('Figure_03/fig3d_feature_importance').iloc[::-1]; ax.barh(df.feature,df.importance,color=COLORS['green']); ax.set(xlabel='XGBoost feature importance',xlim=(0,.27)); clean(ax,'x')
    for label,ax in zip('abcd',axs.ravel()): ax.text(-.12,1.06,label,transform=ax.transAxes,fontweight='bold',fontsize=11,va='top')
    save(fig,'Figure_03_response_mapping')

def figure4():
    fig,axs=plt.subplots(2,2,figsize=(7.0,5.2),dpi=300)
    df=load('Figure_04/fig4a_field_mapping'); colors={'North':COLORS['blue'],'South':COLORS['orange']}; ax=axs[0,0]
    for side,g in df.groupby('side'):
        ax.errorbar(g.kf_mgkg,g.mapped_mgkg,yerr=g.mapped_sd,fmt='o',ms=5,color=colors[side],ecolor='#dbe2ea',elinewidth=1,capsize=0,label=side)
        for _,r in g.iterrows(): ax.text(r.kf_mgkg+.08,r.mapped_mgkg+.05,r['sample'],fontsize=8)
    ax.plot([77.5,87],[77.5,87],ls='--',color=COLORS['gray']); ax.set(xlabel=r'KF moisture (mg kg$^{-1}$)',ylabel=r'Mapped moisture (mg kg$^{-1}$)',xlim=(77.6,86.9),ylim=(77.6,86.9)); ax.legend(frameon=False,loc='upper left'); clean(ax)
    ax=axs[0,1]; df['mean_pair']=(df.kf_mgkg+df.mapped_mgkg)/2; bias=df.error_mgkg.mean(); sd=df.error_mgkg.std(ddof=1)
    for side,g in df.groupby('side'): ax.scatter(g.mean_pair,g.error_mgkg,s=28,color=colors[side],edgecolor='white',linewidth=.4)
    ax.axhline(bias,color=COLORS['dark']); ax.axhline(bias+1.96*sd,color=COLORS['gray'],ls='--'); ax.axhline(bias-1.96*sd,color=COLORS['gray'],ls='--'); ax.text(df.mean_pair.min()+.05,bias+1.96*sd-.25,'bias=%.2f'%bias,fontsize=8); ax.set(xlabel=r'Mean of KF and mapped value (mg kg$^{-1}$)',ylabel=r'Mapped - KF (mg kg$^{-1}$)',ylim=(-2.1,7.2)); clean(ax)
    ax=axs[1,0]; ax.bar(df['sample'],df.abs_error_mgkg,color=COLORS['orange'],edgecolor=COLORS['dark'],linewidth=.6,hatch='//'); m=df.abs_error_mgkg.mean(); ax.axhline(m,color=COLORS['gray'],ls='--'); ax.text(-.4,m+.08,'mean',fontsize=8,color=COLORS['gray']); ax.set(ylabel=r'Absolute error (mg kg$^{-1}$)',ylim=(0,6.5)); clean(ax)
    ax=axs[1,1]; order=['North','South']; means=df.groupby('side').relative_error_percent.mean().reindex(order); ax.bar(order,means,color=[COLORS['blue'],COLORS['orange']],edgecolor=COLORS['dark'],linewidth=.6)
    for i,side in enumerate(order):
        vals=df[df.side==side].relative_error_percent; ax.scatter(np.full(len(vals),i)+np.linspace(-.08,.08,len(vals)),vals,s=24,facecolor='white',edgecolor=COLORS['dark'],linewidth=.6)
    ax.set(ylabel='Relative error (%)',ylim=(0,8.2)); clean(ax)
    for label,ax in zip('abcd',axs.ravel()): ax.text(-.12,1.06,label,transform=ax.transAxes,fontweight='bold',fontsize=11,va='top')
    save(fig,'Figure_04_field_applicability')

def figure5():
    fig,axs=plt.subplots(2,2,figsize=(7.0,5.2),dpi=300)
    df=load('Figure_05/fig5a_data_structure'); ax=axs[0,0]; ax2=ax.twinx(); ax.bar(df.kf_mgkg.astype(str),df.sampling_units,color=COLORS['blue'],width=.62); ax2.plot(df.kf_mgkg.astype(str),df.scan_records,color=COLORS['orange'],marker='o',lw=1.2); ax.set(xlabel=r'KF moisture (mg kg$^{-1}$)',ylabel='Sampling units (n)',ylim=(0,7.4)); ax2.set(ylabel='Scan records (n)',ylim=(0,230)); clean(ax); ax2.spines['top'].set_visible(False)
    df=load('Figure_05/fig5b_within_level_cv'); ax=axs[0,1]; ax.bar(df.kf_mgkg.astype(str),df.within_level_cv_percent,color=COLORS['purple'],edgecolor=COLORS['dark'],linewidth=.5); ax.set(xlabel=r'KF moisture (mg kg$^{-1}$)',ylabel='Within-level CV (%)',ylim=(0,37)); clean(ax)
    df=load('Figure_05/fig5c_holdout_rmse'); ax=axs[1,0]; ax.bar(df.held_out_kf_mgkg.astype(str),df.holdout_rmse_mgkg,color=df['type'].map({'Endpoint':COLORS['red'],'Interior':COLORS['green']}),edgecolor=COLORS['dark'],linewidth=.6); ax.legend(handles=[Patch(facecolor=COLORS['red'],edgecolor=COLORS['dark'],label='Endpoint'),Patch(facecolor=COLORS['green'],edgecolor=COLORS['dark'],label='Interior')],frameon=False,fontsize=8); ax.set(xlabel=r'Held-out KF moisture (mg kg$^{-1}$)',ylabel=r'Holdout RMSE (mg kg$^{-1}$)',ylim=(0,31.5)); clean(ax)
    df=load('Figure_05/fig5d_field_relative_error'); ax=axs[1,1]; ax.bar(df['sample'],df.relative_error_percent,color=COLORS['orange'],edgecolor=COLORS['dark'],linewidth=.6,hatch='//'); m=df.relative_error_percent.mean(); ax.axhline(m,color=COLORS['gray'],ls='--'); ax.text(-.4,m+.08,'mean',fontsize=8,color=COLORS['gray']); ax.set(xlabel='Field-aged samples',ylabel='Field relative error (%)',ylim=(0,6.9)); clean(ax)
    for label,ax in zip('abcd',axs.ravel()): ax.text(-.12,1.06,label,transform=ax.transAxes,fontweight='bold',fontsize=11,va='top')
    save(fig,'Figure_05_measurement_boundary')

if __name__ == '__main__':
    figure1(); figure2(); figure3(); figure4(); figure5(); plt.show()
