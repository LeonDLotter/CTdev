import ptitprince as pt
import seaborn as sns


def plot_raincloud(data, ax, x, y, x_mean=None, y_mean=None, 
                   title="", xlab="", ylab="", 
                   colors=None, 
                   violin_scale="width", 
                   violinbox_lw=1, violin_w=1,
                   scatter_a=0.075, scatter_s=1, scatter_lw=0.1,
                   mean_s=10):
    violin_kwargs = dict(
        zorder=1,
        linewidth=violinbox_lw,
        palette=colors,
        cut=0,
        scale=violin_scale,
        width=violin_w,
        bw="scott",
        inner=None,
    )
    scatter_kwargs = dict(
        zorder=1,
        linewidth=scatter_lw,
        alpha=scatter_a,
        palette=colors,
        s=scatter_s,
        edgecolor="k",
    )
    box_kwargs = dict(
        zorder=2,
        linewidth=violinbox_lw,
        palette=colors,
        width=0.175,
        showfliers=False,
        showcaps=False,
    )
    mean_kwargs = dict(
        zorder=3,
        s=mean_s,
        color="white",
        edgecolor="0.3",
        linewidth=0.5,
    )
    pt.half_violinplot(data=data, x=x, y=y, ax=ax, **violin_kwargs)
    sns.stripplot(data=data, x=x, y=y, ax=ax, **scatter_kwargs)
    sns.boxplot(data=data, x=x, y=y, ax=ax, **box_kwargs)
    if (x_mean is not None) & (y_mean is not None):
        sns.scatterplot(x=x_mean , y=y_mean, ax=ax, **mean_kwargs)
    
    ax.set_title(title)
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)