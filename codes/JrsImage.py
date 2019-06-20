from skimage import io
import matplotlib.pyplot as plt

if __name__ == "__main__":
    img = io.imread("E:\JrsGithub\JrsScrapy\codes\\1212.jpg")
    io.imshow(img)
    plt.show()