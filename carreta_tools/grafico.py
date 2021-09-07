import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


def getImage(path, zoom):
    return OffsetImage(plt.imread(path), zoom=zoom)


def get_image_path(hero):
    img_prefix = 'carreta_tools/static/images/minimap_icon/'
    img_suffix = '_minimap_icon.png'
    img_paths = [img_prefix + element.replace(' ', '_') + img_suffix for element in hero]
    return img_paths


def generate_graph(hero, matches, winrate, pos):
    plt.style.use('seaborn')

    fig, ax = plt.subplots()
    ax.scatter(winrate, matches)

    for x, y, path in zip(winrate, matches, get_image_path(hero)):
        zoom = x/55
        ab = AnnotationBbox(getImage(path, zoom), (x, y), frameon=False)
        ax.add_artist(ab)

        plt.xlabel('Winrate')
        plt.ylabel('Matches')

        plt.xlim(min(winrate)-10, max(winrate)+10)
        plt.ylim(0, max(matches)+10)

        plt.axhline(y=100, color='red', linestyle='-')
        plt.axvline(x=50, color='red', linestyle='-')
        plt.grid(which='major', axis='both', color='gray')

    plt.savefig(f'carreta_tools/static/graph_{pos}.jpg')
