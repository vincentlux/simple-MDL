from mbox2solr import mbox2solr

if __name__ == '__main__':
    m2s = mbox2solr(f_name='chunk_0_filtered.txt', dir_in='./data/Mail', dir_out='./data/xml')
    print('start')
    m2s.split(remove_trashcode=True, save_as_txt=False)
    m2s.txt2xml()
    print('finish')