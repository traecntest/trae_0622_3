import time
from engines import ScriptEngine, DialogNode
from risk_assessment import RiskAssessor
from models import ExerciseRecord


class ExerciseController:
    def __init__(self, script_engine: ScriptEngine, record: ExerciseRecord,
                 risk_assessor: RiskAssessor = None):
        self.script_engine = script_engine
        self.record = record
        self.risk_assessor = risk_assessor or RiskAssessor()
        self.start_time = time.time()
        self.is_paused = False
        self.is_completed = False
        self.current_node = None

    def start(self):
        self.start_time = time.time()
        self.risk_assessor.reset()
        start_node = self.script_engine.get_current_node()
        self.current_node = start_node
        return start_node

    def choose_option(self, option_id: str):
        current_node = self.script_engine.get_current_node()
        if not current_node:
            return None

        chosen_option = None
        for option in current_node.options:
            if option.id == option_id:
                chosen_option = option
                break

        if not chosen_option:
            return None

        risk_delta = chosen_option.risk_delta
        self.risk_assessor.add_risk(risk_delta, current_node.id, option_id)

        self.record.add_choice_log(current_node.id, option_id, risk_delta)

        next_node = self.script_engine.choose_option(option_id)
        self.current_node = next_node

        if next_node and next_node.is_end:
            self._finish_exercise()

        return {
            "next_node": next_node,
            "risk_delta": risk_delta,
            "current_score": self.risk_assessor.get_current_score(),
            "current_level": self.risk_assessor.get_current_level(),
            "trigger_calm": chosen_option.trigger_calm or (next_node.trigger_calm if next_node else False),
            "calm_message": next_node.calm_message if next_node and next_node.trigger_calm else ""
        }

    def _finish_exercise(self):
        self.is_completed = True
        duration = int(time.time() - self.start_time)
        summary = self.risk_assessor.generate_summary()

        self.record.final_risk_score = summary["final_score"]
        self.record.final_risk_level = summary["final_level"]
        self.record.total_duration = duration
        self.record.result_summary = self._generate_result_summary(summary)
        self.record.update()

    def _generate_result_summary(self, summary: dict) -> str:
        level = summary["final_level_label"]
        score = summary["final_score"]
        safety_rate = int(summary["safety_rate"] * 100)
        total_choices = summary["total_choices"]

        return (f"最终风险等级：{level}（{score}分）\n"
                f"安全选择率：{safety_rate}%\n"
                f"总选择次数：{total_choices}次")

    def get_current_risk(self):
        return {
            "score": self.risk_assessor.get_current_score(),
            "level": self.risk_assessor.get_current_level(),
            "trend": self.risk_assessor.get_risk_trend()
        }

    def get_risk_summary(self):
        return self.risk_assessor.generate_summary()

    def is_calm_needed(self, node: DialogNode = None) -> bool:
        if node is None:
            node = self.current_node
        if node and node.trigger_calm:
            return True
        return False

    def get_elapsed_time(self) -> int:
        return int(time.time() - self.start_time)

    def get_record(self):
        return self.record
