import cv2
import numpy as np
from .QuantizationMatrix import quantization_matrix
from .mapping import mapping


quant_mat = quantization_matrix.quant_mat
mapping = mapping.mapping

class Decoder:
    def __init__(self):        
        # Empty init
        pass
    
    def retrieve_info(self, size_ac_dc):
        img_size, ac_encoded_txt, dc_encoded_txt = size_ac_dc.split('|')
        return img_size, ac_encoded_txt, dc_encoded_txt
    
    def izigzag(self, ac_dec, ind, dc_dec):    
        img = np.zeros((8, 8), dtype = np.float64)
        img[0, 0] = dc_dec[ind]
        for i in range(len(ac_dec)):
            img[mapping[i][0], mapping[i][1]] = ac_dec[i]
        return img    
    
    def jACdec(self, ac_encoded_txt):

        ac_encoded_file = ac_encoded_txt.split('.')
        ac_encoded_array = []
        for i in range(len(ac_encoded_file)):
            local_string_array = ac_encoded_file[i].split(',')
            local_array = []
            for j in range(len(local_string_array)):
                local_array.append(int(local_string_array[j]))
            local_array = np.array(local_array)
            ac_encoded_array.append(local_array) 

        ac_decoded_array  = []
        for i in range(len(ac_encoded_array)):
            j = 0
            local = []
            while j < len(ac_encoded_array[i]) - 2:        
                local += ac_encoded_array[i][j] * [0]
                local += [ac_encoded_array[i][j+1]]
                j     += 2        
            local += (63 - len(local)) * [0]
            local = np.array(local)    
            ac_decoded_array.append(local)
        return ac_decoded_array
    
    def jDCdec(self, dc_encoded_txt):
        
        dc_decoded_file = dc_encoded_txt.split(',')
        dc_decoded_file = [int(entry) for entry in dc_decoded_file]
        prev = 0    
        for i in range(len(dc_decoded_file)):
            dc_decoded_file[i] += prev
            prev = dc_decoded_file[i]
        dc_decoded_file = np.array(dc_decoded_file)    
        return dc_decoded_file
    
    def rescaling(self, blocks_array):
        for i in range(blocks_array.shape[0]):
            blocks_array[i] = (blocks_array[i] * quant_mat)
        return blocks_array        
    
    def IDCT(self, blocks_array):
        img_array = []
        for i in range(blocks_array.shape[0]):
            img_array.append(cv2.idct(blocks_array[i]))
        img_array = np.array(img_array)
        return img_array    

    def addOffset(self, img_array, offset = 128):
        img_array += offset
        img_array[img_array<0] = 0
        img_array[img_array>255] = 255
        img_array = np.round(img_array)
        img_array = np.array(img_array, dtype = np.int32)
        return img_array  

    def reconstruct(self, reconstructed_img_array, m, n):
        """
        Combines all the 8 x 8 blocks to form an image
        """
        counter = 0
        reconstructed_img = np.zeros((m, n), dtype = np.int32)
        for start_row in np.arange(0, m, 8):
            for start_col in np.arange(0, n, 8):            
                reconstructed_img[start_row:start_row + 8, start_col:start_col+8] = reconstructed_img_array[counter]
                counter += 1    
        return reconstructed_img
    
    def decode(self, size_ac_dc):
        
        img_size, ac_encoded_txt, dc_encoded_txt = self.retrieve_info(size_ac_dc)
        
        dc_dec = self.jDCdec(dc_encoded_txt)
        ac_decoded_array = self.jACdec(ac_encoded_txt)
        blocks_array = []
        for i in range(len(ac_decoded_array)):
            local_block = self.izigzag(ac_decoded_array[i], i, dc_dec)
            blocks_array.append(local_block)
        blocks_array = np.array(blocks_array)  
        
        blocks_array = self.rescaling(blocks_array)
        
        reconstructed_img_array = self.IDCT(blocks_array)
        
        reconstructed_img_array = self.addOffset(reconstructed_img_array)
        
        num_rows = int(img_size.split(',')[0])
        num_cols = int(img_size.split(',')[1])
        hori_total = (8 - num_cols%8)
        vert_total = (8 - num_rows%8)                
        reconstructed_img = self.reconstruct(reconstructed_img_array, num_rows + vert_total, num_cols + hori_total)
        
        left_pad = hori_total//2
        right_pad = hori_total - hori_total//2
        top_pad = vert_total//2
        bot_pad = vert_total - vert_total//2        
        
        reconstructed_img = np.array(reconstructed_img, dtype = 'uint8')
        
        return reconstructed_img[top_pad:-bot_pad, left_pad:-right_pad]