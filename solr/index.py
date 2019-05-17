from mbox2solr import mbox2solr

if __name__ == '__main__':
    m2s = mbox2solr()
    print('start')
    m2s.split(remove_trashcode=True)
    print('finish')