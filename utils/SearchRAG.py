import re 
from dateutil import parser

def search_rag(cmd):
    #配置全文检索，通过jieba获取关键词进行查询
    import jieba.posseg as jp
    from whoosh.qparser import QueryParser,MultifieldParser
    from whoosh.query import compound
    from whoosh.index import open_dir,exists_in
    from settings import index_dir,org_file_dir
    l = jp.lcut(cmd)
    keywords = [i.word for i in filter(lambda x:x.flag=='eng' or x.flag.startswith('n') ,l)]
    if exists_in(index_dir,indexname="test_idx"):
        ix = open_dir(index_dir,indexname="test_idx")
        query = []
        for keyword in keywords:
            query.append(MultifieldParser(fieldnames=['title','abstracts'],schema=ix.schema).parse(keyword))
        print(query)
        print("--------------------")
        res = []
        with ix.searcher() as searcher:
            results = searcher.search(compound.Or(query))
            for result in results:
                res.append(result.get('content'))
        return "。".join(res)
    else :
        return ""

# import chromadb
# def search_rag(cmd):
#     chroma_client = chromadb.PersistentClient(path="db")
#     collection = chroma_client.get_or_create_collection(name="my_collection_ptyy")
#     #cmd = "2024年11月15日相较于24年11月13日，省融资信用服务平台注册企业变化情况"
#     p_date =  re.compile('\d{2,4}[-/年]\d{1,2}[-/月]\d{1,2}')
#     match_date_list = [parser.parse(date_i.replace("年", "-").replace("月", "-").replace("/", "-"),yearfirst=True).strftime(r"%Y-%m-%d")  for date_i in re.findall(p_date,cmd)]
#     print(match_date_list)
#     where_meta = {}
#     where_meta['$and'] = [{'meta_date':{'$ne':"0000"}},{'meta_date':{'$ne':"0001"}}]
#     if len(match_date_list) > 0:
#         where_meta['$and'].append(
#             {
#                 'meta_date':
#                 {
#                     "$in":match_date_list
#                 }
#             }
#         )



#     results = collection.query(
#         query_texts=[cmd], # Chroma will embed this for you
#         #query_texts=[], # Chroma will embed this for you
#         where=where_meta,
#         #where_document={"$contains":"2024年11月13日"},
#         n_results=30 # how many results to return
#     )
#     if "documents" in results.keys() and len(results['documents']) > 0:
#         return ".".join(results['documents'][0])
#     return ""