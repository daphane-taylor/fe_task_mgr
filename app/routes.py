from flask import (
	Flask,
	render_template,
	request as flask_request
)
import requests

app = Flask(__name__)

BACKEND_URL = "http://127.0.0.1:5000/tasks"

@app.get("/")
def home():
	return render_template("index.html")
@app.get("/about")
def about():
	return render_template("about.html")

@app.get("/tasks")
def task_list():
	response = requests.get(BACKEND_URL)
	if response.status_code == 200:
		task_data = response.json().get("tasks")
		return render_template("list.html", tasks=task_data)
	return (
		render_template("error.html", error=response.status_code),
		response.status_code
	)

@app.get("/tasks/<int:pk>") 
def task_detail(pk):
	url = "%s/%s" % (BACKEND_URL, pk)
	response = requests.get(url)
	if response.status_code == 200:
		single_task = response.json().get("task")
		return render_template("detail.html", task=single_task)
	return (
		render_template("error.html", error=response.status_code), 
		response.status_code
	)

@app.get("/tasks/new")
def get_new_form():
	return render_template("new.html")

@app.post("/tasks/new")
def create_task():
	task_data = flask_request.form
	response = requests.post(BACKEND_URL, json=task_data)
	if response.status_code == 204:
		return render_template("success.html",
		message= "You have successfully submitting the form")
	return (
		render_template("error.html", error=response.status_code),
		response.status_code
	)

@app.get("/tasks/edit/<int:pk>")
def get_edit_form(pk):
	url = "%s/%s" % (BACKEND_URL, pk)
	response = requests.get(url)
	if response.status_code == 200:
		single_task = response.json().get("task")
		return render_template("edit.html", task=single_task)
	return (
		render_template("error.html", status=response.status_code),
		response.status_code
	)

@app.post("/tasks/edit/<int:pk>")
def edit_task(pk):
	task_data = flask_request.form
	url = "%s/%s" %(BACKEND_URL, pk)
	response = requests.put(url, json=task_data)
	if response.status_code == 200:
		return render_template("success.html", message="task successfully edited")
	return (
		render_template("error.html", error=response.status_code),
		response.status_code
	)

@app.get("/tasks/delete/<int:pk>")
def get_delete_form(pk):
	url = "%s/%s" % (BACKEND_URL, pk)
	response = requests.get(url)
	if response.status_code == 200:
		single_task = response.json().get("task")
		return render_template("delete.html", task=single_task)
	return (
		render_template("error.html", error=response.status_code),
		response.status_code
	)

@app.post("/tasks/delete/<int:pk>")
def delete_task(pk):
	url = "%s/%s" % (BACKEND_URL, pk)
	response = requests.delete(url)
	if response.status_code == 204:
		return render_template("success.html", message="Task successfully deleted")
	return (
		render_template("error.html", status=response.status_code),
		response.status_code
	)
