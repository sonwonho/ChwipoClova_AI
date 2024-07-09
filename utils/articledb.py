import json

import MySQLdb


class ArticleDB:
    def __init__(self):
        self.host, self.port, self.id, self.password, self.db = self._get_config()
        self.conn = MySQLdb.connect(
            host=self.host,
            port=self.port,
            user=self.id,
            password=self.password,
            database=self.db,
        )
        self.cursor = self.conn.cursor()

    def _get_config(self):
        with open("config.json", "r") as cf:
            config = json.load(cf)
        return (
            config["ARTICLEDB"]["HOST"],
            config["ARTICLEDB"]["PORT"],
            config["ARTICLEDB"]["ID"],
            config["ARTICLEDB"]["PASS"],
            config["ARTICLEDB"]["DATABASE"],
        )

    def _execute(self, sql):
        self.cursor.execute(sql)
        return self.cursor

    def show_columns(self, table):
        for r in self._execute(f"SHOW columns FROM {table}"):
            print(r)

    def show_all_data_in_table(self, table):
        for r in self._execute(f"SELECT * FROM {table}"):
            print(r)

    def get_category_list(self):
        category_list_sql = f"SELECT name FROM FeedSubCategory"
        return [i[0] for i in self._execute(category_list_sql)]

    def get_category_id(self, category):
        if category in self.get_category_list():
            get_category_id_sql = (
                f"SELECT id FROM FeedSubCategory WHERE name='{category}'"
            )
            return self._execute(get_category_id_sql).fetchone()[0]
        else:
            raise Exception("Undefined category")

    def insert_feed_category_result(self, feedid, category):
        try:
            categoryid = self.get_category_id(category)
            sql = f"INSERT into FeedAndCategory(feedId, categoryId, regDate) values({feedid}, {categoryid}, NOW())"
            self._execute(sql)
        except Exception as e:
            print(e)

    def get_feed_information_iter(self, gap_day=1):
        sql = f"SELECT id, link FROM feed WHERE created_at>=DATE_ADD(NOW(), INTERVAL -{gap_day} DAY)"
        return self._execute(sql)


if __name__ == "__main__":
    mdb = ArticleDB()
    # mdb.show_columns("feed")
    # mdb.show_all_data_in_table("feed")
    # mdb.show_columns("FeedSubCategory")
    # mdb.show_all_data_in_table("FeedSubCategory")
    # mdb.show_columns("FeedAndCategory")
    # mdb.show_all_data_in_table("FeedAndCategory")
    # mdb.insert_feed_category_result(974, "목표 설정")
    # mdb.show_all_data_in_table("FeedAndCategory")
    # mdb._execute(f"DELETE FROM FeedAndCategory WHERE id = 580")
    # mdb.show_all_data_in_table("FeedAndCategory")
    for id, link in mdb.get_feed_information_iter(100):
        print(f"id : {id} // link : {link}")
