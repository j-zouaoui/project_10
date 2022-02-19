# SoftDesk--API: Test API providing projects information

The SoftDesk-API project is a REST API application to be executed locally. It provides projects informations and track issues from different http endpoints.
The API provides these endpoints to get, post and update detailed infomation about projects issues and share comments filtered by
id. Endpoints allow users to retrieve information for individual project, users, issues or comments.

## Installation

This locally-executable API can be installed and executed from [http://localhost:8000/api/projects/](http://localhost:8000/api/projects/) using the following steps.

1. Clone this repository using `$ git clone clone https://github.com/j-zouaoui/project_10.git` 
2. Activate the virtual environment with `$ env\Scripts\activate` on windows or `$ source env/bin/activate` on macos or linux.
3. Install project dependencies with `$ pip install -r requirements.txt`
4. Run the server with `$ python manage.py runserver`

When the server is running after step 4 of the procedure, the SoftDesk API can be requested from endpoints starting with the following base URL: http://localhost:8000/api/projects/.

## Usage and detailed endpoint documentation

One you have launched the server, you can read the documentation through the
browseable documentation interface of the API by visiting [https://documenter.getpostman.com/view/18041284/UVkjwHxJ).
