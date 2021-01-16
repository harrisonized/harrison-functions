import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from wordcloud import WordCloud, STOPWORDS


# Functions included in this file:
# # plot_empty
# # plot_heatmap
# # plot_corr
# # plot_barh
# # plot_single_scatter
# # plot_histogram
# # plot_qq
# # plot_wordcloud


def plot_empty(xlabel=None, ylabel=None,
               title=None,
               figsize=(8, 5)):
    """Convenience function
    """
    fig = plt.figure(figsize=figsize, dpi=80)

    ax = fig.gca()
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=16)

    return fig, ax


def plot_heatmap(df, xlabel=None, ylabel=None, title=None,
                 xticklabels=None, yticklabels=None,
                 color='coolwarm', annot=False, fmt=None,
                 order=None, figsize=(8, 5), dpi=240):
    """Heatmap is the same dimensions as input table
    """
    fig = plt.figure(figsize=figsize, dpi=dpi)

    if order:
        df = df[order]

    # annotations
    if fmt:
        sns.heatmap(df, cmap=color, annot=annot, fmt=fmt)
    else:
        sns.heatmap(df, cmap=color, annot=annot)

    ax = fig.gca()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if xticklabels:
        ax.set_xticklabels(xticklabels)
    if yticklabels:
        ax.set_yticklabels(yticklabels)
    ax.set_title(title)
    return fig, ax


def plot_corr(df, title, order=None, figsize=(8, 5)):
    """
    """
    fig = plt.figure(figsize=figsize)

    if order:
        df = df[order]
    sns.heatmap(df.corr(), cmap='coolwarm', annot=True)

    ax = fig.gca()
    ax.set_title(title, fontsize=18)
    return fig


def plot_barh(df, x, y, xerr=None, color='#8d1a93',
              xlabel=None, yticklabels=None, title=None,
              figsize=(8, 5)):
    """
    """
    fig, ax = plt.subplots(figsize=figsize)

    if xerr:
        ax.barh(df[y], df[x], xerr=df[xerr], align='center', color=color, capsize=3)
    else:
        ax.barh(df[y], df[x], align='center', color=color, capsize=3)

    ax.set_yticks(df[y])
    if yticklabels:
        ax.set_yticklabels(yticklabels, fontsize=12)
    else:
        ax.set_yticklabels(df[y], fontsize=12)

    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_title(title, fontsize=16)

    return fig, ax


def plot_single_scatter(df, x, y,
                        xlabel=None, ylabel=None,
                        title=None,
                        color=None,
                        figsize=(8, 5)
                        ):
    """
    """
    fig = plt.figure(figsize=figsize)
    plt.scatter(df[x], df[y], color=color)

    if xlabel is None:
        xlabel = x
    if ylabel is None:
        ylabel = y

    ax = fig.gca()
    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.set_title(title, fontsize=18)

    return fig


def plot_histogram(df, x, bins, xlabel=None, ylabel=None, title=None, figsize=(8, 5)):
    """
    """
    fig = plt.figure(figsize=figsize)

    ax = fig.gca()
    ax.hist(df[x], bins=bins, color='#8d1a93')

    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.set_title(title, fontsize=18)

    return fig


def plot_qq(vals, xlabel, ylabel, title):
    """vals should be a list of residuals
    """
    fig = sm.qqplot(vals, line='s', color='#1f77b4')

    plt.xlabel(xlabel, fontsize=16)
    plt.ylabel(ylabel, fontsize=16)
    plt.title(title, fontsize=18)

    return fig


def plot_wordcloud(topics, stopwords=STOPWORDS, figsize=(10, 4)):
    """Convenience wrapper
    """
    wordcloud = WordCloud(stopwords=stopwords,
                          background_color='white',
                          width=figsize[0] * 100, height=figsize[1] * 100).generate(topics)

    fig = plt.figure(figsize=figsize)
    plt.imshow(wordcloud)
    plt.axis('off')

    return fig
