from fastapi import FastAPI, Request
#from fastapi.responses import Response
import json
import xmltodict 

app = FastAPI()

@app.get("/test")
def xml_to_json():

    with open("data.xml","rb") as f:
        data = f.read()
        '''xml_bytes = dicttoxml(
            data,
            custom_root="root",
            attr_type=False
        )

        return Response(
                content=xml_bytes,
                media_type="application/xml"
        )'''

        json_parsed = xmltodict.parse(data)

        return json_parsed
