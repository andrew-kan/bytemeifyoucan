from openai import OpenAI
from datetime import datetime
import time
import json

class Assistant():
    def __init__(self, openai_key, assistant_id, repo):
        self.client = OpenAI(api_key=openai_key)

        self.id = assistant_id
        self.db = repo

    def create_user(self, email, name):
        thread = self.client.beta.threads.create()
        user = self.db.create_user(name, email, thread.id)
        if user == None:
            return None
        else:
            return str(user)

    def run_is_completed(self, thread_id, run_id):
        run = self.client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        print(run.status)
        return run.status == "requires_action" or run.status == "completed"

    def get_reply(self, email, subject, message, from_person, to_person):
        user = self.db.get_user(email)
        name = user["name"]
        thread_id = user["thread"]
        status = user["status"]
        today = datetime.today().strftime('%Y-%m-%d')

        message = self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=f"Subject: {subject}\nFrom: {from_person}\nTo: {to_person}\nMessage: {message}"
        )

        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.id,
            instructions=f"Details on the user:\nName: {name}\nToday's date: {today}\nStatus of the user:\n{status}"
        )

        while not self.run_is_completed(thread_id, run.id):
            time.sleep(1)  # Add a delay to avoid excessive API requests

        run = self.client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

        reply = run.required_action.submit_tool_outputs.tool_calls[0].function.arguments
        call_ids = [tool_call.id for tool_call in run.required_action.submit_tool_outputs.tool_calls]

        # messages = self.client.beta.threads.messages.list(
        #     thread_id=thread_id
        # )
        print(reply, call_ids)
        run = self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run.id,
            tool_outputs=[
                {
                    "tool_call_id": call_id,
                    "output": "{\"success\": \"true\"}",
                } for call_id in call_ids
            ]
        )

        return json.loads(reply)