from PIL import Image
from scipy.spatial.distance import hamming





def dHash(img: Image.Image) -> int:
    img = img.resize((9, 8)).convert('L')
    i = 0
    for y in range(8):
        for x in range(8):
            if img.getpixel((x, y)) < img.getpixel((x+1, y)):
                i |= 1 << (y * 8 + x)
    return i


# img = Image.open('../../imgs/Alyson_Hannigan_200512.jpg')
# hash = dHash(img)
# print(hex(hash), bin(hash), bin(0x3a6c6565498da525), sep='\n')

def compare(img1: Image.Image, img2: Image.Image):
    h1 = dHash(img1)
    h2 = dHash(img2)
    dst = hamming(list('{:064b}'.format(h1)), list('{:064b}'.format(h2)))
    return dst*64


if __name__ == '__main__':
    scales = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.5, 2, 4, 6, 7, 8, 10, 20]

    orig = Image.open('../../imgs/troll.jpg')  # type: Image.Image
    ts = Image.open('../../imgs/troll.jpg')

    for scale in scales:
        scaled = ts.resize((int(orig.width*scale), int(orig.height*scale)))
        dst = compare(orig, scaled)
        print(f'scale = {scale}, dst = {dst}')
