from rest_framework.decorators import api_view
from rest_framework.response import Response
import io
from rest_framework.parsers import JSONParser
from myproject.settings import BASE_DIR
path=f"{BASE_DIR}\\myapp\\data.json"
import json

@api_view(['GET'])
def get_data(request,id):
    if request.method == 'GET':
        with open(path,'r') as f:
            data = json.load(f)
            d=data['items'][int(id)]
        return Response(d)
    
@api_view(['GET'])
def get_all_data(request):
    if request.method == 'GET':
        with open(path,'r') as f:
            data = json.load(f)
        return Response(data)
    
@api_view(["POST"])
def post_data(request):
    if request.method=="POST":
        json_data=request.body
        stream=io.BytesIO(json_data)
        python_data=JSONParser().parse(stream)
        with open(path,'r') as f:
            exiting_data=json.load(f)

        exiting_data['items'].append(python_data)
        with open(path, 'w') as f:
            json.dump(exiting_data,f, indent=4)
        return Response('Data posted!')
    
@api_view(["DELETE"])
def delete_data(request,id):
    if request.method=="DELETE":
        with open(path,'r') as f:
            data=json.load(f)
            del data["items"][int(id)]
        with open(path, 'w') as f:
            json.dump(data,f, indent=4)
        



      
        return Response("Item deleted!")
