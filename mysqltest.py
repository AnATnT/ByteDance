import pymysql
import re



def ruleList():
    db = pymysql.connect(host='47.104.70.37', user='root',
                         password='bytedance', database='bytedance')
    cursor = db.cursor()
    sql = 'select * from rule where status = 1'
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    return data


if __name__ == '__main__':
    ruler = ruleList()
    requestData = 'test'
    for i in ruler:
        attackData = re.search(i[2], requestData)
        if attackData:
            vulnerable = i[1]
            attackReason = attackData.group()
            risk = i[4]
            print(vulnerable, attackReason, risk)
