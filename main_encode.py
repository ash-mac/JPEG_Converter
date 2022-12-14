#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Modules.Encode import Encode
from PIL import Image
import numpy as np
import os


# In[2]:


list_imgs = os.listdir('imgs')


# In[3]:


encoder = Encode.Encoder()


# In[4]:


for img in list_imgs:
    os.chdir('imgs')
    encoder.encode(img)

