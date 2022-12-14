#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Modules.Decode import Decode
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim


# In[2]:


list_imgs = os.listdir('encoded_imgs/')


# In[3]:


decoder = Decode.Decoder()


# In[4]:


for encoded_img in list_imgs:
    os.chdir('encoded_imgs')
    file = open(encoded_img, 'r')
    content = file.readlines()
    file.close()
    os.chdir('..')
    channelwise_files = content[0].split(':')
    channelwise_decoded_files = []
    for channelwise_file in channelwise_files:
        channelwise_decoded_files.append(decoder.decode(channelwise_file))
    path = 'reconstructed_imgs'
    if not os.path.exists(path):
        os.makedirs(path)    
    os.chdir(path)    
    if len(channelwise_decoded_files) == 1:
        r_img = Image.fromarray(channelwise_decoded_files[0])        
        r_img.save(f'r_{encoded_img}.tiff')
        os.chdir('..')
    else:
        os.chdir('..')
        pass

