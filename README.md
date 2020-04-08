# BBDN-Collab-REST-Demo-Python

This code relies on several libraries:

* cachetools==4.0.0
* PyJWT==1.7.1
* requests==2.22.0
* urllib3==1.25.3

To install:

pip install -r requirements.txt

Built on Python 3.7

To configure this app for your use, copy the ConfigTemplate.py file to Config.py and add your key, secret, and the post event URL.

```
config = {
    "collab_key" : "YOURKEY",
    "collab_secret" : "YOURSECRET",
    "collab_base_url" : "techpreview.bbcollab.com/collab/api/csa",
    "verify_certs" : "True",
    "survey_url" : "YOURSURVEYURL"
}
```

To run, simply navigate to the bbdn/rest/collab directory at the command line and type:

```
  python Collab.py
```  
  
