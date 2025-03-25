
-- connect ec2
	ssh -i D:/python/restaurant_app/restaurant_key.pem ubuntu@3.110.217.146 
-- to move only one file
	scp -i "D:/python/restaurant_app/restaurant_key.pem" "D:/python/restaurant_app/app.py" ubuntu@3.110.217.146:~/restaurant_app
-- to move all the files
	scp -i "D:/python/restaurant_app/restaurant_key.pem" -r "D:/python/restaurant_app/Zomato_Recommendation_and_Price_Prediction_System-main" ubuntu@3.110.217.146:~/zomato_app  
	
	

--to run the app
streamlit run app.py --server.port=8501 --server.enableCORS=false --server.enableXsrfProtection=false
---------------------------------------------------
--Create a Virtual Environment
	cd ~/restaurant_app
--Activate the Virtual Environment
	source venv/bin/activate



streamlit run app.py -- local



 Local URL: http://localhost:8501
  Network URL: http://i
  External URL: http://ip
  
  
  
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://172.31.4.85:8501
  External URL: http://3.110.217.146:8501
  
  
  ~/restaurant_app/venv/bin$
  
  restaurant_app/venv/bin$
  
  export PATH=$HOME/.local/bin:$PATH
  
  sudo kill -9 57896

  
  http://3.110.217.146:8501






python -c "import sklearn; print(sklearn.__version__)"
python -c "import pymysql; print(pymysql.__version__)"



$ scp -i "D:/python/restaurant_app/restaurant_key.pem" "D:/python/restaurant_app/resturant_recommendations_all_json.py" ubuntu@3.110.217.146:~/restaurant_app


$ ssh -i D:/python/restaurant_app/restaurant_key.pem ubuntu@3.110.217.146

cd restaurant_app
source venv/bin/activate

-- to get the pkl file
python3 resturant_recommendations.py

-- to run the app
streamlit run app.py --server.port=8501 --server.enableCORS=false --server.enableXsrfProtection=false


telnet 3.110.217.146 22



liting all the files with details:
ls -lh

