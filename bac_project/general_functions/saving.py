
# coding: utf-8

# In[ ]:

def save_as_txt(folder, filename, txt):
    file_txt = open(folder+'/'+filename+'.txt', 'w')
    file_txt.write(txt)
    file_txt.close()

