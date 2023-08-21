from locust import FastHttpUser, task, between


class WebUser(FastHttpUser):
    host = "http://127.0.0.1:8000"
    wait_time = between(1, 5)

    @task
    def task1(self):
        self.client.post("/msg", json={"message": "Task 1 message (request)"})

    @task
    def task2(self):
        self.client.post("/msg", json={"message": "Task 2 message (publish)"})
