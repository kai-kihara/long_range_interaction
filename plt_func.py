import matplotlib.pyplot as plt
import matplotlib


def plt_setting():
    plt.rcParams['font.family'] = 'Arial'

def ax_setting(ax:matplotlib.axes.Axes):
    ax.tick_params(left=False, bottom=False, which='minor')
    ax.tick_params(labelleft=False, labelbottom=False, which='minor')

def create_subplots(figsize:tuple=(6,4), size:tuple=(1,1), sharex:bool=True, sharey:bool=True):
    fig, axs = plt.subplots(nrows=size[0], ncols=size[1], figsize=figsize, constrained_layout=True, sharex=sharex, sharey=sharey)
    if size == (1,1):
        axs:matplotlib.axes.Axes
        ax_setting(ax=axs)
    elif size[0]==1 or size[1]==1:
        for ax in axs: ax_setting(ax=ax)
    else:
        for ax in axs.flat: ax_setting(ax=ax)
    return fig, axs

def save_fig(fig:matplotlib.figure.Figure, directory, file_name, style:str='png'):
    if style == 'png' or style == 'all':
        fig.savefig(f'image/{directory}/{file_name}.png', dpi=300)
    if style == 'svg' or style == 'all':
        fig.savefig(f'image/{directory}/{file_name}.svg', dpi=300)
    plt.close()
