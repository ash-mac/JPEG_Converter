import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from .QuantizationMatrix import quantization_matrix
from .mapping import mapping
import os

quant_mat = quantization_matrix.quant_mat
mapping = mapping.mapping

class Encoder:
        
    def __init__(self, padding = 'median'):
        self.padding = padding
        
    def pad_img(self, im):
        """
        Padding Image to have rows and columns as multiple of 8,
        Number of Rows are rounded up to next greater multiple of 8
        Number of Columns are rounded up to next greater multiple of 8
        (Total padded columns)/2 number of columns are added to left and right of image,
        with 1 extra column on right side if total padded columns are odd
        (Total padded rows)/2 number of rows are added to top and bottom of image,
        with 1 extra column on bottom side if total padded rows are odd
        This is done as JPEG DCT assumes rows and columns are multiple of 8.
        """
        
        hori_total = (8 - im.shape[0]%8)
        vert_total = (8 - im.shape[1]%8)        
        left_pad = hori_total//2
        right_pad = hori_total - hori_total//2
        top_pad = vert_total//2
        bot_pad = vert_total - vert_total//2
        
        im_new = np.pad(im, ((left_pad, right_pad), (top_pad, bot_pad)), mode = self.padding)
        
        return im_new
    
    def block(self, im):
        """
        Assumes image is 8x8
        divides the img into an array of 8x8 blocks
        """
        m, n = im.shape
        im_ = np.array(im, dtype = np.float64)
        im_ = np.array(im_)
        im_new = im_.copy()

        m, n = im_new.shape

        img_array = []
        for start_row in np.arange(0, m, 8):
            for start_col in np.arange(0, n, 8):
                img_array.append(im_new[start_row:start_row + 8, start_col:start_col+8])

        img_array = np.array(img_array)            
        return img_array
    
    def offset(self, img_array):
        """
        Takes in input of 8x8 array of image blocks
        Subtracts 128 from all pixels of image
        """
        img_array = img_array - 128
        return img_array
    
    def DCT(self, img_array):
        """
        Returns DCT of all blocks of the array of image blocks
        """
        new_img_array = []
        for i in range(img_array.shape[0]):
            new_img_array.append(cv2.dct(img_array[i]))
        new_img_array = np.array(new_img_array)
        return new_img_array
    
    def quantization(self, img_array):
        """
        Quantizes each block of the image according to quantization matrix
        """
        for i in range(img_array.shape[0]):
            img_array[i] = np.round(img_array[i]/quant_mat)
        return np.array(img_array, dtype = np.int32)
    
    def zigzag(self, im):   
        "This function returns the zig-zag ordering of cell values in a 8 x 8 block"
        reordered = []
        max_sumrc = 15
        flag = 0
        start_row = 0
        start_col = 0    
        for sumrc in range(1, max_sumrc):
            if flag == 0:
                while start_row <= min(sumrc, 7):                                 
                    reordered.append(im[start_row, sumrc - start_row])                    
                    start_row = start_row + 1
                    if start_row > 7:
                        start_col = sumrc + 1 - 7
                        start_row = 7
                        break
                    else:
                        start_col = 0
                flag = 1            
            else:
                while start_col <= min(sumrc, 7):                                    
                    reordered.append(im[sumrc - start_col, start_col])              
                    start_col = start_col + 1
                    if start_col > 7:
                        start_row = sumrc + 1 - 7
                        start_col = 7
                        break
                    else:
                        start_row = 0
                flag = 0            
        reordered = np.array(reordered, dtype = np.int32)
        return reordered

    def jDCenc(self, img_array):
        '''
        Returns DC encoding of all dc components of all 8x8 blocks
        '''
        dc_enc = []
        prev = 0
        for i in range(img_array.shape[0]):        
            dc_enc.append(img_array[i][0][0] - prev)
            prev = img_array[i][0][0]    
        return np.array(dc_enc)    
    
    def jACenc(self, arr):
        '''
        Returns Run Length Encoding of a single 8x8 block
        '''
        rle = []
        num0 = 0
        for i in range(arr.shape[0]):
            if arr[i] != 0:
                rle.append([num0, int(arr[i])])        
                num0 = 0
            else:
                num0 += 1
        rle.append([0, 0])
        rle = np.array(rle, dtype = np.int32)    
        return rle    

    def encode_bw(self, img_path, im, c_num = 0, file = None):
        img_name = ''
        img_name_parts = img_path.split('.')
        for part in img_name_parts[:-1]:
            img_name += part          
        im_new = self.pad_img(im)
        img_array = self.block(im_new)
        img_array = self.offset(img_array)
        img_array = self.DCT(img_array)
        img_array = self.quantization(img_array)
        
        zigzag_arrays = []
        for i in range(img_array.shape[0]):
            temp = self.zigzag(img_array[i])
            zigzag_arrays.append(temp)
        zigzag_arrays = np.array(zigzag_arrays)   
        
        rle_zigzag_arrays = []
        for i in range(zigzag_arrays.shape[0]):
            rle_zigzag_arrays.append(self.jACenc(zigzag_arrays[i]))    
        
        file = None
        path = 'encoded_imgs'
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)
        if c_num <=1:
            file = open(f'encoded_img_{img_name}.rle', 'w')
        else:
            file = open(f'encoded_img_{img_name}.rle', 'a')
        file.write(f'{im.shape[0]}')
        file.write(',')
        file.write(f'{im.shape[1]}')
        file.write('|')
        for i in range(len(rle_zigzag_arrays)):
            for j in range(len(rle_zigzag_arrays[i])):
                for k in range(2):
                    file.write(str(rle_zigzag_arrays[i][j][k]))
                    if k == 1 and j == len(rle_zigzag_arrays[i]) - 1:
                        if i != len(rle_zigzag_arrays) - 1:
                            file.write('.')
                    else:
                        file.write(',')    
        file.write('|')                
        dc_enc_arr = self.jDCenc(img_array)
        for i in range(len(dc_enc_arr)):    
            file.write(str(dc_enc_arr[i]))
            if i != len(dc_enc_arr) - 1:
                file.write(',')
                        
        if c_num:
            if c_num !=3:                
                file.write(':')
            file.close()
            os.chdir('..')
            return file 
        file.close()
        os.chdir('..')
    
    def encode(self, img_path):
        
        img = Image.open(img_path)
        img = img.convert('L')
        img = np.array(img)
#         img = plt.imread(img_path)        
        os.chdir('..')
        if img.ndim == 2:
            self.encode_bw(img_path, img)
            return
            
        file = None
        for channel in range(3):
            file = self.encode_bw(img_path, img[:, :, channel], c_num = channel + 1, file = file)        