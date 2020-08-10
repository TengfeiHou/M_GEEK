import pymysql
from tqdm import tqdm

def putindatabase():
    
    connc = pymysql.Connect(
        user = 'root',
        password='ayhtf123',
        database = 'yewuyuan',
        charset = 'utf8'
    )
    
    
    connc.rollback()
    connc.close()
    print('done')
        
if __name__ == "__main__":
    # read data
    putindatabase()


