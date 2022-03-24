import json
import os
import shutil
from flask import Response,request,render_template,jsonify
from models import app_model

PROJ_FOLDER = os.getenv('PROJ_FOLDER')

def store_data():
    """
    STORE USER PROVIDED DATASET IN DB
    """
    try: 
        file = request.files['files']
        data_name = str(request.form.get('data_name'))
        data_path = os.path.join(PROJ_FOLDER+'/datasets/')
        print(data_path)
        print(file,data_name)
        dirs = os.listdir(data_path)
        # print(dirs)
        if (file.filename != '') and (data_name != 'None') and (data_name != '') and (data_name+".csv" not in dirs):
            if file.filename.endswith('.csv') and not file.filename.startswith('~$'):
                # os.mkdir(data_path+"/"+data_name)
                file.save(os.path.join(data_path,data_name+".csv"))
                print(file.filename)
                fun = app_model.add_data(data_name,data_path)

                if fun == "success":
                    # return list_data()
                    return render_template("xvector_base.html",datas = app_model.list_data()[0])

                    # return Response (json.dumps({"message": data_name + " created successfully"}),content_type='application/json', status = 200)
                else:
                    return Response (json.dumps({"error": fun}),content_type='application/json', status = 400) 
            else:
                ret_data = {"error" : "Invalid File Type"}
                res = Response (json.dumps(ret_data),content_type='application/json', status = 400)
                return res
        else:
            ret_data = {"error" : "file name and data name mandatory / {} already exists".format(data_name+".csv")}
            res = Response (json.dumps(ret_data),content_type='application/json', status = 400)
            return res
    
    except Exception as e:
        return Response (json.dumps({"error":str(e)}),content_type='application/json', status = 400)

    finally:
        dirs = os.listdir(data_path)
        if data_name+".csv" in dirs:
            os.remove(data_path+data_name+".csv")

def list_data():
    """
    LIST TABLES
    """
    try:
        fun = app_model.list_data()

        if fun[1] == "success":
            return render_template("xvector_base.html",datas = fun[0])
            # return Response (json.dumps(fun[0]),content_type='application/json', status = 200)
        else:
            return Response (json.dumps({"error": fun}),content_type='application/json', status = 400)

    except Exception as e:
        return Response (json.dumps({"error":str(e)}),content_type='application/json', status = 400)

def compute_data(data_name):
    """
    PERFORM OPERATIONS BETWEEN COLUMNS
    """
    try:
        column_name = request.form['column_name']
        operation = request.form['operation']
        fun = app_model.data_compute(data_name,column_name,operation)
        if fun[1] == "success":
            return Response (json.dumps({"result":fun[0]}),content_type='application/json', status = 200)
        else:
            return Response (json.dumps({"error": fun}),content_type='application/json', status = 400)
    except Exception as e:
        return Response (json.dumps({"error":str(e)}),content_type='application/json', status = 400)

def plot_data(data_name):
    """
    FETCH DATA FOR PLOT 
    """
    try:
        column_one = request.args.get('column1')
        column_two = request.args.get('column2')

        fun = app_model.data_plot(data_name,column_one,column_two)
        if fun[1] == "success":
            return Response (json.dumps(fun[0]),content_type='application/json', status = 200)
        else:
            return Response (json.dumps({"error": fun}),content_type='application/json', status = 400)
    except Exception as e:
        return Response (json.dumps({"error":str(e)}),content_type='application/json', status = 400)

