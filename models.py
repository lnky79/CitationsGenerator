from sqlalchemy import (
    Column, Integer,
    String, DateTime,
    Boolean,
)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class ArticleORM(Base):
    __tablename__ = 'articles'

    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String)
    link = Column(String)
    bibtex = Column(String)
    resource_type = Column(String)
    resource_link = Column(String)
    google_id = Column(String(50))
    citations_link = Column(String)
    id_by_journal = Column(String)
    year = Column(Integer)
    citations_count = Column(Integer)
    create_time = Column(DateTime)
    pdf_temp_url = Column(String)
    cite_links_init_ok = Column(Boolean)
    citations_init_ok = Column(Boolean)

    def __repr__(self):
        return ("<ArticleORM(title='%s', google_id='%s',"
                " link='%s', id=%s)>"
        ) % (self.title, self.google_id,self.link, self.id)


class CitationLinkORM(Base):
    __tablename__ = 'citation_link'

    id = Column(Integer,primary_key=True,autoincrement=True)
    link = Column(String)
    article_google_id = Column(String(50))
    is_crawled = Column(Boolean)

    def __repr__(self):
        return ("<CiteLinkORM(link='%s', article_google_id='%s',"
                " is_crawled=%s), id=%s>"
        ) % (self.link, self.article_google_id, self.is_crawled,self.id)


class CiteRelationORM(Base):
    __tablename__ = 'cite_relation'

    id = Column(Integer,primary_key=True,autoincrement=True)
    cite_google_id = Column(String(50))
    cited_google_id = Column(String(50))

    def __repr__(self):
        return ("<CiteRelationORM(cite_google_id='%s', cited_google_id=%s), id=%s>"
        ) % (self.cite_google_id, self.cited_google_id, self.id)