import json
from .database import Database


class ExerciseRecord:
    def __init__(self, id=None, user_id=None, script_id=None, script_name=None,
                 final_risk_score=0, final_risk_level=None, total_duration=0,
                 choices_made=None, result_summary=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.script_id = script_id
        self.script_name = script_name
        self.final_risk_score = final_risk_score
        self.final_risk_level = final_risk_level
        self.total_duration = total_duration
        self.choices_made = choices_made or []
        self.result_summary = result_summary
        self.created_at = created_at

    @staticmethod
    def create(user_id, script_id, script_name):
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO exercise_records (user_id, script_id, script_name) VALUES (?, ?, ?)",
            (user_id, script_id, script_name)
        )
        conn.commit()
        return ExerciseRecord.get_by_id(cursor.lastrowid)

    @staticmethod
    def get_by_id(record_id):
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM exercise_records WHERE id = ?", (record_id,))
        row = cursor.fetchone()
        if row:
            return ExerciseRecord._from_row(row)
        return None

    @staticmethod
    def _from_row(row):
        choices = json.loads(row["choices_made"]) if row["choices_made"] else []
        return ExerciseRecord(
            id=row["id"],
            user_id=row["user_id"],
            script_id=row["script_id"],
            script_name=row["script_name"],
            final_risk_score=row["final_risk_score"],
            final_risk_level=row["final_risk_level"],
            total_duration=row["total_duration"],
            choices_made=choices,
            result_summary=row["result_summary"],
            created_at=row["created_at"]
        )

    def update(self):
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE exercise_records SET final_risk_score=?, final_risk_level=?,
               total_duration=?, choices_made=?, result_summary=? WHERE id=?""",
            (self.final_risk_score, self.final_risk_level,
             self.total_duration, json.dumps(self.choices_made, ensure_ascii=False),
             self.result_summary, self.id)
        )
        conn.commit()

    def add_choice_log(self, node_id, option_id, risk_delta):
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO choice_logs (record_id, node_id, option_id, risk_delta) VALUES (?, ?, ?, ?)",
            (self.id, node_id, option_id, risk_delta)
        )
        conn.commit()
        self.choices_made.append({
            "node_id": node_id,
            "option_id": option_id,
            "risk_delta": risk_delta
        })

    @staticmethod
    def list_by_user(user_id, limit=20):
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM exercise_records WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit)
        )
        rows = cursor.fetchall()
        return [ExerciseRecord._from_row(row) for row in rows]

    def get_choice_logs(self):
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM choice_logs WHERE record_id = ? ORDER BY timestamp ASC",
            (self.id,)
        )
        return cursor.fetchall()
