#### set env config
export FLASK_CONFIG=development
export CLOUDSML_API_SERVER_SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:whcxhwyz@127.0.0.1:3306/flask_rest_demo



#### generate the new database version
invoke app.env.enter

invoke app.db.init
invoke app.db.migrate
invoke app.db.upgrade
invoke app.db.downgrade

invoke app.db.init_development_data

#### migrate the database and install dependency , start server
invoke app.run
