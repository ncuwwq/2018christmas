# coding: utf-8
import pymysql
import hashlib
import random


mysql_host = "ncuhomev5.mysql.rds.aliyuncs.com"

mysql_user = "ususer"
mysql_password = "US--asdf123"

connect = pymysql.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    database="us"
)

new_connect = pymysql.connect(
    host="47.93.63.56",
    user="root",
    password="#?#",
    database="2018christmas"
)


def get_users_list():
    with open("name", encoding="utf-8") as f:
        for name in f:
            yield name.strip()


def get_special_users_list():
    with open("special", encoding="utf-8") as f:
        return f.read().strip().split("\n")


def get_xiaoheiwu_list():
    with open("special", encoding="utf-8") as f:
        return f.read().strip().split("\n")


def get_inform(truename):
    with connect.cursor() as cursor:
        sql = """
            SELECT truename, photo, department, email, sex, user_id From user
            WHERE truename = %s
        """
        cursor.execute(sql, args=[truename])
        return cursor.fetchone()


# def get_users_list():
#     with connect.cursor() as cursor:
#         sql = r"""
#             SELECT truename From us.user
#             WHERE user.jobposition != '老家园'
#             AND user.jobposition != '非正常离职';
#         """
#         cursor.execute(sql)
#         result = cursor.fetchall()
#         return [element[0] for element in result]


def start_king_and_angle():

    # 获取特殊名单
    special_names = get_special_users_list()
    xiaoheiwu_list = get_xiaoheiwu_list()

    men_list = []  # 男生列表
    women_list = []  # 女生列表
    special_list = []  # 特殊人群列表
    if len(special_names) % 2 != 0:
        print("特殊人群数量不为偶数")
        exit()

    # 获取成员信息
    for name in get_users_list():
        info = get_inform(name)
        if info[0] in xiaoheiwu_list:
            continue
        if info[0] in special_names:  # 如果跳过名字在特殊名单里就
            special_list.append(info)
            continue
        if info[4] == 0:
            women_list.append(info)
        else:
            men_list.append(info)

    # 打乱列表
    random.shuffle(men_list)
    random.shuffle(women_list)

    king_angle_list = []  # 国王与天使列表

    men_count = len(men_list)
    women_count = len(women_list)

    if men_count >= women_count:
        more = men_list
    else:
        more = women_list
    # 男-女-男-女-男-女-男-男-男
    for i in range(max(men_count, women_count)):
        if i >= min(men_count, women_count):
            king_angle_list.append(more[i])
        else:
            king_angle_list.append(men_list[i])
            king_angle_list.append(women_list[i])

    for i in range(len(special_list)):
        if i % 2 == 1:
            king = special_list[i - 1][0]
        else:
            king = special_list[i + 1][0]
        yield {
            "username": special_list[i][0],
            "uuid": hashlib.md5((special_list[i][0] + "king").encode()).hexdigest()[8:-8],
            "king": king,
            "user_id": special_list[i][3],
            "department": special_list[i][2],
            "photo": special_list[i][1],
            "us_id": special_list[i][5],
            "sex": special_list[i][4]
        }

    for i in range(len(king_angle_list)):
        if i != len(king_angle_list) - 1:
            king = king_angle_list[i+1][0]
        else:
            king = king_angle_list[0][0]
        yield {
            "username": king_angle_list[i][0],
            "uuid": hashlib.md5((king_angle_list[i][0] + "king").encode()).hexdigest()[8:-8],
            "king": king,
            "user_id": king_angle_list[i][3],
            "department": king_angle_list[i][2],
            "photo": king_angle_list[i][1],
            "us_id": king_angle_list[i][5],
            "sex": king_angle_list[i][4]
        }


# 判断是否已经匹配过了
def check_is_start():
    with new_connect.cursor() as cur:
        cur.execute("SELECT count(*) FROM user2")
        if cur.fetchone()[0] != 0:
            return True
        else:
            return False


def delete_all_info():
    with new_connect.cursor() as cur:
        cur.execute("DELETE FROM user2")
    new_connect.commit()


def insert_into_database():
    if not check_is_start():
        sql = """INSERT INTO 2018christmas.user(username, uuid, king, user_id, department, us_id) VALUES 
        """
        for info in start_king_and_angle():
            sql += "('{}', '{}', '{}', '{}', '{}', '{}'),".format(
                info.get("username"),
                info.get("uuid"),
                info.get("king"),
                info.get("user_id"),
                info.get("department"),
                info.get("us_id")
            )
        with new_connect.cursor() as cur:
            cur.execute(sql.strip(","))
        new_connect.commit()
    else:
        print("已经匹配过了")


if __name__ == '__main__':
    delete_all_info()
    insert_into_database()