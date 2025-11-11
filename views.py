from flask import request
from flask_restful import Resource
from utils import *
import os
from google import genai
from prompts import *

os.makedirs("./embedding_contents", exist_ok=True)
os.makedirs("./files", exist_ok=True)
os.makedirs("./text_data", exist_ok=True)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GC_CLIENT = genai.Client(api_key=GOOGLE_API_KEY)
GC_MODEL = 'gemini-2.5-flash-lite'


class UploadFiles(Resource):
    def post(self):
        files = request.files.getlist('files')

        for file in files:
            file.save(f"./files/{file.filename}")

        get_text()
        sync_embeddings()
        
        return {'msg':'All files uploaded successfully!'}


class SearchQuery(Resource):
    def post(self):
        json_data = request.get_json()
        query = json_data.get("query")
        keyword_query_response = GC_CLIENT.models.generate_content(
            model=GC_MODEL,
            contents=get_exhaustive_keyword_prompt(user_query=query)
        ).text
        # print(keyword_query_response)

        top_files_list = get_top_filenames(query=keyword_query_response)
        
        top_files_text_list = []
        for filename in top_files_list:
            with open(f"./text_data/{filename}.txt",'r') as f:
                text = f.read()
            top_files_text_list.append({
                'filename': filename,
                'content': text
            })
        
        model_prompt = get_search_query_prompt(user_query=query,context=top_files_text_list)

        response = GC_CLIENT.models.generate_content(
            model=GC_MODEL,
            contents=model_prompt
        )

        response = (response.text)[8:-4]

        return response


class SearchQueryAnswerMode(Resource):
    def post(self):
        json_data = request.get_json()
        query = json_data.get("query")

        keyword_query_response = GC_CLIENT.models.generate_content(
            model=GC_MODEL,
            contents=get_exhaustive_keyword_prompt(user_query=query)
        ).text
        # print(keyword_query_response)

        top_files_list = get_top_filenames(query=keyword_query_response)
        
        top_files_text_list = []
        for filename in top_files_list:
            with open(f"./text_data/{filename}.txt",'r') as f:
                text = f.read()
            top_files_text_list.append({
                'filename': filename,
                'content': text
            })
        
        model_prompt = get_answer_mode_query_prompt(user_query=query,context=top_files_text_list)
        # print(model_prompt)
        response = GC_CLIENT.models.generate_content(
            model=GC_MODEL,
            contents=model_prompt
        )
        # print(response)
        response = response.text

        return response