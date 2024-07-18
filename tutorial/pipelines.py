# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
# from dataclasses import dataclass
from typing import Tuple
class TutorialPipeline:
    def process_item(self, item, spider):
        return item


class BookspiderSpider:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # columns = adapter.field_names()

        # print('-----------')    


        # print('-----------')    
        
        
        adapter['title'] = adapter['title'][0].strip()
        adapter['price'] = float(adapter['price'].replace('£',''))
        adapter['description'] = adapter['description'][0].strip()
        adapter['cateogry'] = adapter['cateogry'][0].lower()
        adapter['availability'] = int(adapter['availability'][0].split()[2].replace('(',''))
        adapter['upc'] = adapter['upc'][0].strip()
        
        rating_col = adapter['rating'].split()[1]
        if rating_col == 'One':
            adapter['rating'] = 1
        elif rating_col == 'Two':
            adapter['rating'] = 2
        elif rating_col == 'Three':
            adapter['rating'] = 3
        elif rating_col == 'Four':
            adapter['rating'] = 4
        elif rating_col == 'Five':
            adapter['rating'] = 5

        
        return item


import mysql.connector


class MysqlDemoPipeline:
    
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'admin_dev',
            password = '2101',
            database = 'edw'
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()
        
        # self.cur.execute("""drop table if exists books """)

        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS  books(
            id int NOT NULL auto_increment, 
            
            title text,
            price float,                        
            description text,
            cateogry text,
            availability TINYINT,             
            upc text,
            rating TINYINT,
            last_updated_dt DATETIME,
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):
        
        ## Check to see if text is already in database 
        self.cur.execute("select * from books where title = %s", (item['title'],))
        result = self.cur.fetchone()

        ## If it is in DB, create log message
        if result:
            spider.logger.warn("Item already in database: %s" % item['title'])
            print('-----------------')
            print('-----------------')
            print('-----------------')
            


        ## If text isn't in the DB, insert data
        else:
        ## Define insert statement
            self.cur.execute(""" insert into books
                            (title, price,description,cateogry,availability,upc,rating,last_updated_dt) 
                            values 
                            (%s,%s,%s,%s,%s,%s,%s,%s)
                            
                            
                            """, (
                item["title"],
                item["price"],
                item["description"],
                item["cateogry"],
                item["availability"],
                item["upc"],
                item["rating"],
                item["last_updated_dt"]
                
                
            ))

            ## Execute insert of data into database
            self.conn.commit()

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()
