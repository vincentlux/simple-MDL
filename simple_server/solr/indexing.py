import datetime, re
from mbox2solr import mbox2solr

def indexing(filename='chunk_0_filtered.txt'):
    m2s = mbox2solr(f_name=filename, dir_in='./data/Mail', dir_out='./data/xml')
    print('start txt to xml')
    m2s.split(remove_trashcode=True, save_as_txt=False)
    m2s.txt2xml()
    print('finish xml conversion')
    print('start indexing')
    corename = re.sub("[^0-9]", "", str(datetime.datetime.now()))
    # save name for afterwards deletion
    save_name_for_record(corename)
    dirname = filename.replace(".", "_")
    m2s.call_solr(corename, dirname)
    print(corename, 'finished')
    return corename


def save_name_for_record(corename):
    with open('corename_list.txt', 'a') as f:
        f.write(corename+'\n')

if __name__ == '__main__':
    indexing()

    
