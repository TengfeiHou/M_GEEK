import pymysql
from tqdm import tqdm

def putindatabase(dirs):
    try :
        connc = pymysql.Connect(
            user = 'root',
            password='ayhtf123',
            database = 'yewuyuan',
            charset = 'utf8'
        )
        
        cur = connc.cursor()
        sql = "insert into yewuyuan values (%s,%s,%s,%s)"
        with open(dirs) as f:
            for a in tqdm(f):
                #print(a)
                b = a.strip().split(',')
                #print(b)
                b = ['0',b[0],str(round(float(b[1]),2)),str(round(float(b[2]),2))]
                #print(b)
       

                cur.execute(sql,b)
                
        connc.commit()
    except Exception as e:
        print(e)
        connc.rollback()
    finally :
        cur.close()
        connc.close()
    print('done')
        
if __name__ == "__main__":
    dirs =  '../yewuyuan@CMB/data.txt'
    # read data
    #putindatabase(dirs)


