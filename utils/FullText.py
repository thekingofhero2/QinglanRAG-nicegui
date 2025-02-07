from jieba.analyse import ChineseAnalyzer
from whoosh.fields import TEXT, SchemaClass,ID
analyzer = ChineseAnalyzer()
class ArticleSchema(SchemaClass):
    title = TEXT(stored=True, analyzer=analyzer)
    abstracts = TEXT(stored=True, analyzer=analyzer)
    content = TEXT(stored=True, analyzer=analyzer)
    path=ID(stored=True,unique=True)
    