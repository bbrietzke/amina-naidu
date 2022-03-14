from __future__ import annotations
from ast import List
import logging
import feedparser
from lib.database_service import DatabaseService

logger = logging.getLogger("RSS")

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
            "SELECT Url, FeedId FROM Feeds ORDER BY FeedId ASC;",
            ()
        )


class Entry():
    def __init__(self, url:str, title:str = None, id:int = 0, feed_id:int = 0):
        self.__url = url
        self.__title = title
        self.__id = id
        self.__feed_id = feed_id

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

    def save(self):
        if self.__id:
            pass
        else:
            return (
                "insert into FeedEntries(url, title, FeedId) values (?, ?, ?);",
                (self.__url, self.__title, self.__feed_id)
            )

class RSSManager():
    def __init__(self, serviceManager:DatabaseService, announments:str = None):
        self.__service:DatabaseService = serviceManager
        self.__announcments:str = announments

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


    async def show_feeds(self):
        retVal = []
        with self.__service as c:
            (q, p) = Feed.all()
            values = c.execute(q, p).fetchall()
            for v in values:
                (url, id) = v
                retVal.append(Feed(url, feedId=id))

        return retVal