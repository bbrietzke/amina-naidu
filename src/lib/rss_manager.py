from __future__ import annotations
from ast import List
from email import message
import logging
import feedparser
from lib.database_service import DatabaseService

logger = logging.getLogger("rss")

class Feed():
    def __init__(self, url:str, feedId:int = 0):
        self.__id = feedId
        self.__url = url

    @property
    def id(self):
        return self.__id

    @property
    def url(self):
        return self.__url

    def save(self):
        if self.__id:
            return (
                "UPDATE Feeds SET Url = ? WHERE Id = ?;",
                (self.__url, self.__id)
            )
        else:
            return (
                "INSERT INTO Feeds(Url) VALUES (?);",
                (self.__url,)
            )

    @staticmethod
    def all():
        return (
            "SELECT Id, Url, Title FROM Feeds ORDER BY Id ASC;",
            ()
        )


class Entry():
    def __init__(self, url:str, title:str = None, id:int = 0, feed_id:int = 0, message_id:str = None, feed_title:str = None):
        self.__url = url
        self.__title = title
        self.__id = id
        self.__feed_id = feed_id
        self.__message_id = message_id
        self.__feed_title = feed_title

    def __str__(self):
        return "ENTRY[id:{}, url:{}, title: {}, feed_id: {}, message_id: {}, feed_title: {}".format(
            self.__id, self.__url, self.__title, self.__feed_id, self.__message_id, self.__feed_title)

    def __repr__(self):
        return "ENTRY[id:{}, url:{}, title: {}, feed_id: {}, message_id: {}, feed_title: {}".format(
            self.__id, self.__url, self.__title, self.__feed_id, self.__message_id, self.__feed_title)

    @property
    def id(self):
        return self.__id
    
    @property
    def url(self):
        return self.__url

    @property
    def title(self):
        return self.__title

    @property
    def feed_id(self):
        return self.__feed_id

    @feed_id.setter
    def feed_id(self, value:int):
        self.__feed_id = value

    @property
    def message_id(self):
        return self.__message_id

    @message_id.setter
    def message_id(self, value:int):
        self.__message_id = value

    @property
    def feed_title(self):
        return self.__feed_title

    @feed_title.setter
    def feed_title(self, value:str):
        self.__feed_title = value

    def save(self):
        if self.__id:
            pass
        else:
            return (
                "insert or ignore into FeedEntries(url, title, FeedId, MessageId) values (?, ?, ?, ?);",
                (self.__url, self.__title, self.__feed_id, self.__message_id)
            )

    @staticmethod
    def update_with_message_id(url:str, message_id:str):
        return (
            "update feedentries set messageid = ? where url = ?;", 
            (message_id, url)
        )

    @staticmethod
    def new_entries():
        return (
            "select feedentries.id, feedentries.url, feedentries.title, feedentries.feedid, feeds.title from feedentries inner join feeds on feedentries.feedid = feeds.id where feedentries.messageid is null;",
            ()
        )
        pass

class RSSManager():
    def __init__(self, serviceManager:DatabaseService):
        self.__service:DatabaseService = serviceManager

    def update_feed_id(self, url, message_id) -> int:
        (q, p) = Entry.update_with_message_id(url, message_id)
        with self.__service as c:
            return c.execute(q, p).lastrowid

    def add_feed(self, url) ->  int:
        retVal = 0
        (q, p) = Feed(url).save()
        with self.__service as c:
            results = c.execute(q, p)
            retVal = results.lastrowid

        entries:List[Entry] = self.refresh_feed(url)

        saved = []
        query = ""
        for entry in entries:
                entry.feed_id = retVal
                entry.message_id = retVal
                (query, p) = entry.save()
                saved.append(p)

        with self.__service as service:
            service.executemany(query, saved)

        return retVal

    def refresh_feed(self, feed_url:str):
        retVal:List[Entry] = []
        f = feedparser.parse(feed_url)
        for item in f['items']:
            entry = Entry(item['link'], title = item['title'])
            retVal.append(entry)

        return retVal

    def new_entries(self):
        retVal:List[Entry] = []

        with self.__service as c:
            (q, p) = Feed.all()
            saved = []
            query = None
            feed_results = c.execute(q, p).fetchall()

            for feed in feed_results:
                (id, url, title) = feed
                entries = self.refresh_feed(url)

                for entry in entries:
                    entry.feed_id = id
                    (query, p) = entry.save()
                    saved.append(p)
                
                c.executemany(query, saved)

        with self.__service as service:
            (q, p) = Entry.new_entries()
            entries = service.execute(q, p).fetchall()

            for entry in entries:
                logger.debug(entry)
                (id, url, title, feed_id, feed_title) = entry
                retVal.append(Entry(url, title = title, id = id, feed_title=feed_title, feed_id=feed_id))

        return retVal


    async def show_feeds(self):
        retVal = []
        with self.__service as c:
            (q, p) = Feed.all()
            values = c.execute(q, p).fetchall()
            for v in values:
                (url, id) = v
                retVal.append(Feed(url, feedId=id))

        return retVal

    async def published_entries(self, results):
        collection = []
        query:str = ""
        for r in results:
            (msg, url) = r
            (query, p) = Entry.update_with_message_id(url, msg)
            logger.debug("query: {} \n params: {}".format(query, p))
            with self.__service as service:
                service.execute(query, p)
            

