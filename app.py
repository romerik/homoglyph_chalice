from chalice import Chalice, Response
import dnstwist
import json
import gzip
from function import genTldsDnstwist, homoglyphGenerator
from threading import Thread

app = Chalice(app_name='domainhomoglyph')
app.api.binary_types.append('application/json')

"""
@app.route('/dnstwist/{domain}', methods=['GET'])
def get_dnstwist(domain):
    try:
        result = json.dumps(genTldsDnstwist(domain)).encode('utf-8')
        custom_headers = {
        'Content-Type': 'application/json',
        }
        return Response(body=result,
                    status_code=200,
                    headers=custom_headers
        )
    except Exception as err:
        print(err)
        """
@app.route('/homoglyph/{domain}', methods=['GET'])
def get_homoglyph(domain):
    try:
        result = list(set(homoglyphGenerator(domain)))
        custom_headers = {
        'Content-Type': 'application/json',
        }
        to_write = {f"{domain}_homoglyphs": result}
        """with open(f"{domain}_homoglyphs.json", "w") as file:
            json.dump(to_write, file, indent=4)"""
        return Response(body=result,
                    status_code=200,
                    headers=custom_headers
        )
        #return {"homoglyphs" : result}
    except Exception as err:
        print(err)


