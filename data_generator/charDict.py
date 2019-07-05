# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 21:01:07 2019

@author: Nuo Xu
"""

import os
import numpy as np
import struct
from PIL import Image

#%%

train_data_dir = "C:\\Users\\Nuo Xu\\Desktop\\WORK\\Intern\\Solution1\\HWDB1.1trn_gnt"
test_data_dir = "C:\\Users\\Nuo Xu\\Desktop\\WORK\\Intern\\Solution1\\HWDB1.1tst_gnt"


def read_from_gnt_dir(gnt_dir=train_data_dir):
    def one_file(f):
        header_size = 10
        while True:
            header = np.fromfile(f, dtype='uint8', count=header_size)
            if not header.size: break
            sample_size = header[0] + (header[1]<<8) + (header[2]<<16) + (header[3]<<24)
            tagcode = header[5] + (header[4]<<8)
            width = header[6] + (header[7]<<8)
            height = header[8] + (header[9]<<8)
            if header_size + width*height != sample_size:
                break
            image = np.fromfile(f, dtype='uint8', count=width*height).reshape((height, width))
            yield image, tagcode
    for file_name in os.listdir(gnt_dir):
        if file_name.endswith('.gnt'):
            file_path = os.path.join(gnt_dir, file_name)
            with open(file_path, 'rb') as f:
                for image, tagcode in one_file(f):
                    yield image, tagcode


char_set = set()
for _, tagcode in read_from_gnt_dir(gnt_dir=train_data_dir):
    tagcode_unicode = struct.pack('>H', tagcode).decode('gb2312')#.encode('utf-8')
    char_set.add(tagcode_unicode)
char_list = list(char_set)
char_dict = dict(zip(sorted(char_list), range(len(char_list))))
print(len(char_dict))

# %%
np.save('C:\\Users\\Nuo Xu\\Desktop\\WORK\\Intern\\Solution1\\charDict.npy', char_dict)
# %%
read_dictionary = np.load('charDict.npy').item()