# JPEG_Converter
### This repository contains the implementation of the JPEG DCT Compression and Reconstruction from Compressed Image Algorithm for Grayscale Images
- Works for all image sizes
- All images are currently converted to Grayscale Format
- Not Complete for RGB images. Modifyable for RGB images, needs some work to convert to YCbCr format
- **Scroll down to see the results**

<hr>

### Steps to run the repository:

- Download the repository on your local system
- Navigate inside the repostiry directory
- Delete the existing encoded_imgs, reconstructed_imgs directries. Also delete the preexisting results.png, results.jpeg images
- Put the images to be encoded using jpeg algorithm in the imgs directories
- Execute below commands on terminal:
```
    Step 1) python main_encode.py
    Step 2) python main_decode.py
    Step 3) python visualize_results.py
```
- Step 1 encodes the images present in the imgs directory in run lenght encoded format and stores in the newly created (automatically) encoded_imgs directory
- Step 2 decodes and reconstucts the original image from the compressed images. The images are stored in the newly created (automatically) reconstructed_imgs directory
- Step 3 displays the original and reconstructed images along with the ```SSIM``` and Compression Ratios

<hr>

### Results
- SSIM of above 90 were observed in all images
- Compression ratios obtained were above 1.45 and upto 1.83
![results](https://user-images.githubusercontent.com/60055422/207804603-9cc61d5a-377e-4887-81c1-d0a8f920d46e.jpg)

<hr>

### Algorithm Followed:
#### Encoding Algorithm:
![image](https://user-images.githubusercontent.com/60055422/207807734-a4e90af7-99d9-4f07-a04a-e713dc26a085.png)

<hr>

#### Decoding Algorithm:
![image](https://user-images.githubusercontent.com/60055422/207808013-ff705e8d-6f44-4663-9884-09fe534e8021.png)

<hr>

- Any feedbacks/suggestions are welcome
- Feel free to create a pull request suggesting changes
