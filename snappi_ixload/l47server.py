from flask import Flask, request, jsonify, Response
#from exceptions import Snappil47Exception
import sys
#sys.path.insert(0, "c:\\Users\\waseebai\\Documents\\project\\snappi_l47\\snappi\\artifacts\\snappi")
#sys.path.insert(0, "C:\\Users\\waseebai\\Documents\\project\\GitHub\\snappi\\artifacts\\snappi")

import snappi

app = Flask(__name__)

global CONFIG 
CONFIG = snappi.Config()
CS = snappi.ControlState()
GM = snappi.MetricsRequest()
#sys.path.append("C:\\Users\\waseebai\\Documents\\project\\GitHub\\snappi-ixload")
from snappi_ixload import ixloadapi
API = ixloadapi.Api(host="localhost", version="10.00.0.152")



@app.route("/config", methods=["POST"])
def set_config():
    #print("server ----> ", request.data)
    CONFIG.deserialize(request.data.decode("utf-8"))
    try:
        response = API.set_config(CONFIG)
        warn = snappi.Warning()
        warn.warnings = ["Successfully configured IxLoad"]
        return Response(warn.serialize(), mimetype="application/json", status=200)
    except Exception as err:
        error = snappi.Error()
        error.code = err._status_code
        error.kind = "validation"
        error.errors = [err._message]
        print(err)
        return Response(
            status=400,
            response=error.serialize(),
            headers={"Content-Type": "application/json"},
        )
        return Response(err.status_code)
        #return Response(response=err.message, mimetype="application/json", status=err.status_code)
    # try:
    #     response = API.set_config(CONFIG)
    # except Exception as error:
    #     print("error")
    
    # warn = snappi.Warning()
    # warn.warnings = ["Successfully configured IxLoad"]
    # return Response(warn.serialize(), mimetype="application/json", status=200)

@app.route('/config', methods=['GET'])
def get_config():
    try:
        config = API.get_config()
        return Response(config.serialize(),
                    mimetype='application/json',
                    status=200)

    except Exception as error:
        print("error")
    
@app.route('/control/state', methods=["POST"])
def set_control_state():
    CS.deserialize(request.data.decode("utf-8"))
    
    try:
        
        config = API.set_control_state(CS)
        return Response(config.serialize(), mimetype="application/json", status=200)
        #return Response(config.serialize(),
        #            mimetype='application/json',
        #            status=200)
    except Exception as err:
        error = snappi.Error()
        error.code = err._status_code
        error.kind = "validation"
        error.errors = [err._message]
        print(err)
        return Response(
            status=400,
            response=error.serialize(),
            headers={"Content-Type": "application/json"},
        )
   


@app.route('/monitor/metrics', methods=["POST"])
def get_metrics():
    GM.deserialize(request.data.decode("utf-8"))
    
    try:
        
        config = API.metrics_request(CS)
        return Response(config.serialize(),
                    mimetype='application/json',
                    status=200)
    except Exception as error:
        print(error)

# main driver function
if __name__ == "__main__":
    app.run()
    #run_server()

#from snappi_ixload import l47server as x

#x.run_server()


