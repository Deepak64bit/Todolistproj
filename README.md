# Introduction

The repository contains a web app to manage a todolist. 
The following features are supported

1. List of tasks
1. Sorting tasks by various fields (clicking on the headers of created scheduled and progress)
1. Click on a task id to see details.
1. Edit the task option is available inside the title description page. Click on `update`
1. Click on setprogress to change progress
1. Navigate onto next and previous page using the suitable buttons provided inside the description details page.
1. Delete icon is also provided in the main page
1. Check the missing id number to find whether you have deleted
   
   
# Setting up

1. Clone repository
1. Create a virtualenv and activate it
1. Install dependencies using `pip install -r requirements.txt`
1. Setup application using `python setup.py develop`
1. `export FLASK_APP=todo` to set the application
1. `flask initdb` to create the initial database
1. `flask run` to start the app.



