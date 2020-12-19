import os
import urllib.request
from cairosvg import svg2png
import img2pdf
import glob

class Downloader():
    def __init__(self):
        pass

    def download(self, scores, save, saveImages=False, savePdf=False):
        for score in scores:
            filesToPdf = []


            for ix, page in enumerate(score["pages"]):
                if "svg" in page:
                    fmt = "svg"
                else:
                    fmt = "png"

                if ix < 10:
                    ix = f'0{ix}'

                savepath = os.path.join(save, f'{score["title"]}_{ix}.{fmt}')

                urllib.request.urlretrieve(page, savepath)
                addToPdfPath = savepath

                if fmt == "svg":
                    svg2png(url=savepath, write_to=savepath.replace("svg", "png"), background_color="#ffffff", scale=2)
                    addToPdfPath = savepath.replace("svg", "png")
                    os.remove(savepath)

                filesToPdf.append(addToPdfPath)

            if savePdf:
                with open(os.path.join(save, f'{score["title"]}.pdf'), "wb") as f:
                    f.write(img2pdf.convert(sorted(glob.glob(f'{save}/{score["title"]}*.png'))))

            if not saveImages:
                for image in filesToPdf:
                    os.remove(image)
