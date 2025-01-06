import re 
from dateutil import parser

def search_rag(cmd):
    
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