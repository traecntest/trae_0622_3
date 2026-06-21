from dataclasses import dataclass
from config import RISK_LEVELS


@dataclass
class RiskLevel:
    key: str
    label: str
    color: str
    min_score: int
    max_score: int


class RiskAssessor:
    def __init__(self):
        self.current_score: int = 0
        self.risk_history: list = []
        self.choice_count: int = 0
        self.safe_choice_count: int = 0
        self.dangerous_choice_count: int = 0

    def reset(self):
        self.current_score = 0
        self.risk_history = []
        self.choice_count = 0
        self.safe_choice_count = 0
        self.dangerous_choice_count = 0

    def add_risk(self, delta: int, node_id: str = "", option_id: str = "") -> int:
        self.current_score = max(0, min(100, self.current_score + delta))
        self.risk_history.append({
            "node_id": node_id,
            "option_id": option_id,
            "delta": delta,
            "score_after": self.current_score
        })
        self.choice_count += 1
        if delta <= 0:
            self.safe_choice_count += 1
        else:
            self.dangerous_choice_count += 1
        return self.current_score

    def get_current_score(self) -> int:
        return self.current_score

    def get_current_level(self) -> RiskLevel:
        return self._score_to_level(self.current_score)

    def _score_to_level(self, score: int) -> RiskLevel:
        for key, level_info in RISK_LEVELS.items():
            if level_info["min"] <= score <= level_info["max"]:
                return RiskLevel(
                    key=key,
                    label=level_info["label"],
                    color=level_info["color"],
                    min_score=level_info["min"],
                    max_score=level_info["max"]
                )
        return RiskLevel(
            key="danger",
            label="危险",
            color="#ef4444",
            min_score=81,
            max_score=100
        )

    def get_all_levels(self) -> list:
        levels = []
        for key, level_info in RISK_LEVELS.items():
            levels.append(RiskLevel(
                key=key,
                label=level_info["label"],
                color=level_info["color"],
                min_score=level_info["min"],
                max_score=level_info["max"]
            ))
        return levels

    def get_risk_trend(self) -> str:
        if len(self.risk_history) < 2:
            return "stable"
        recent = self.risk_history[-3:]
        total_delta = sum(item["delta"] for item in recent)
        if total_delta > 5:
            return "rising"
        elif total_delta < -5:
            return "falling"
        return "stable"

    def get_safety_rate(self) -> float:
        if self.choice_count == 0:
            return 1.0
        return self.safe_choice_count / self.choice_count

    def generate_summary(self) -> dict:
        level = self.get_current_level()
        return {
            "final_score": self.current_score,
            "final_level": level.key,
            "final_level_label": level.label,
            "total_choices": self.choice_count,
            "safe_choices": self.safe_choice_count,
            "dangerous_choices": self.dangerous_choice_count,
            "safety_rate": self.get_safety_rate(),
            "risk_trend": self.get_risk_trend(),
            "history": self.risk_history
        }
