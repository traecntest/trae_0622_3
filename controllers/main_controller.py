import os
from engines import ScriptEngine
from models import User, ExerciseRecord
from config import SCRIPTS_DIR


class MainController:
    def __init__(self):
        self.script_engine = ScriptEngine()
        self.current_user = None
        self._load_all_scripts()

    def _load_all_scripts(self):
        scripts = self.script_engine.list_available_scripts(SCRIPTS_DIR)
        for script in scripts:
            script_path = script.get("file_path", "")
            if script_path and os.path.exists(script_path):
                self.script_engine.load_script(script_path)

    def get_all_scripts(self):
        scripts = []
        for script_id in self.script_engine.scripts.keys():
            metadata = self.script_engine.get_script_metadata(script_id)
            if metadata:
                scripts.append(metadata)
        return scripts

    def create_user(self, username, nickname=None, age=None, is_elderly_mode=False):
        existing = User.get_by_username(username)
        if existing:
            return existing
        return User.create(username, nickname, age, is_elderly_mode)

    def get_user(self, user_id):
        return User.get_by_id(user_id)

    def list_users(self):
        return User.list_all()

    def set_current_user(self, user):
        self.current_user = user

    def get_current_user(self):
        return self.current_user

    def start_exercise(self, script_id):
        if not self.current_user:
            raise ValueError("No current user selected")

        script_metadata = self.script_engine.get_script_metadata(script_id)
        if not script_metadata:
            raise ValueError(f"Script {script_id} not found")

        record = ExerciseRecord.create(
            user_id=self.current_user.id,
            script_id=script_id,
            script_name=script_metadata.get("name", "")
        )

        start_node = self.script_engine.start_script(script_id)

        return {
            "record": record,
            "start_node": start_node,
            "script_metadata": script_metadata
        }

    def get_exercise_records(self, user_id=None, limit=20):
        if user_id is None and self.current_user:
            user_id = self.current_user.id
        if user_id is None:
            return []
        return ExerciseRecord.list_by_user(user_id, limit)

    def get_record_detail(self, record_id):
        return ExerciseRecord.get_by_id(record_id)
