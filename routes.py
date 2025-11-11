from app import app, api
from views import *

# api.add_resource(Home,"/")
api.add_resource(SearchQuery,"/search-query")
api.add_resource(SearchQueryAnswerMode,"/search-query-answer")
api.add_resource(UploadFiles,"/upload-files")