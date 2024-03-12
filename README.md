## LOCATION API
***
It helps to normalize input location using google map geocode api and also give functionality to compare two location using range in km.

### HOW SETUP ENVIRONMENT ?
* There are two ways you can run and deploy this application.
### FIRST METHOD
* Using docker container.
* cmd to be followed for deployment or run locally.
* `cd <project_dir>`
* `docker build -t location_api .`
* `docker volume create location_api_log`
* `docker run -itd -p 3000:3000 --name location_v1 -v location_api_log:/logs/logs.log location_api`

### SECOND METHOD
* create new python virtual env
* activate virtual env
* `cd <project_dir>`
* `pip install wheel`
* `pip install -r requirements.tx`
* `python -m src.main > logs/logs.log`
* Access port 3000