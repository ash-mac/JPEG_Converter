from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os


ssim1 = ssim(np.array(Image.open('imgs/Img1.tiff')), np.array(Image.open('reconstructed_imgs/r_encoded_img_Img1.rle.tiff')))
ssim2 = ssim(np.array(Image.open('imgs/Img2.tiff')), np.array(Image.open('reconstructed_imgs/r_encoded_img_Img2.rle.tiff')))
ssim3 = ssim(np.array(Image.open('imgs/Img3.tiff')), np.array(Image.open('reconstructed_imgs/r_encoded_img_Img3.rle.tiff')))
ssim4 = ssim(np.array(Image.open('imgs/Lena512.gif').convert('L')), np.array(Image.open('reconstructed_imgs/r_encoded_img_Lena512.rle.tiff')))

original_imgs = os.listdir('imgs')

compressed_imgs = os.listdir('encoded_imgs')

crs = []
for oi, ci in zip(original_imgs, compressed_imgs):
    oi_siz = os.stat(f'imgs/{oi}').st_size    
    ci_siz = os.stat(f'encoded_imgs/{ci}').st_size
    crs.append(round(oi_siz/ci_siz, 2))

fig, ax = plt.subplots(4, 2, figsize = (15, 15))

ax[0, 0].imshow(np.array(Image.open('imgs/Img1.tiff')), cmap = 'gray')
ax[0, 1].imshow(np.array(Image.open('reconstructed_imgs/r_encoded_img_Img1.rle.tiff')), cmap = 'gray')
ax[0, 1].set_ylabel(f'Compression = {crs[0]}')
ax[0, 1].set_xlabel(f'ssim = {ssim1}')

ax[1, 0].imshow(np.array(Image.open('imgs/Img2.tiff')), cmap = 'gray')
ax[1, 1].imshow(np.array(Image.open('reconstructed_imgs/r_encoded_img_Img2.rle.tiff')), cmap = 'gray')
ax[1, 1].set_ylabel(f'Compression = {crs[1]}')
ax[1, 1].set_xlabel(f'ssim = {ssim2}')

ax[2, 0].imshow(np.array(Image.open('imgs/Img3.tiff')), cmap = 'gray')
ax[2, 1].imshow(np.array(Image.open('reconstructed_imgs/r_encoded_img_Img3.rle.tiff')), cmap = 'gray')
ax[2, 1].set_ylabel(f'Compression = {crs[2]}')
ax[2, 1].set_xlabel(f'ssim = {ssim3}')

ax[3, 0].imshow(np.array(Image.open('imgs/Lena512.gif').convert('L')), cmap = 'gray')
ax[3, 1].imshow(np.array(Image.open('reconstructed_imgs/r_encoded_img_Lena512.rle.tiff')), cmap = 'gray')
ax[3, 1].set_ylabel(f'Compression = {crs[3]}')
ax[3, 1].set_xlabel(f'ssim = {ssim4}')

for i in range(4):
    for j in range(2):
        ax[i, j].set_xticklabels([])
        ax[i, j].set_yticklabels([])
        if j == 0:
            ax[i, j].set_title('Original Image')
        else:
            ax[i, j].set_title('Reconstructed Image')
plt.tight_layout()
fig.savefig('results.png', bbox_inches = 'tight')