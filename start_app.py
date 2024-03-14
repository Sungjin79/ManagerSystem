from app import app


if __name__=="__main__":
    
    app.run(host='0.0.0.0',debug=True,port=9988,threaded=True)
    # app.run(host='0.0.0.0',port=80, threaded=True)
    
