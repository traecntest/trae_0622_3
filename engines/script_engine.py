import json
import os
from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class DialogOption:
    id: str
    text: str
    next_node_id: str
    risk_delta: int = 0
    is_safe_choice: bool = False
    trigger_calm: bool = False


@dataclass
class DialogNode:
    id: str
    speaker: str
    text: str
    options: List[DialogOption] = field(default_factory=list)
    is_start: bool = False
    is_end: bool = False
    trigger_calm: bool = False
    calm_message: str = ""
    risk_tip: str = ""
    node_type: str = "normal"


class ScriptEngine:
    def __init__(self):
        self.scripts: Dict[str, dict] = {}
        self.current_node: Optional[DialogNode] = None
        self.current_script_id: str = ""
        self.visited_nodes: List[str] = []

    def load_script(self, script_path: str) -> dict:
        with open(script_path, "r", encoding="utf-8") as f:
            script_data = json.load(f)
        script_id = script_data.get("id", os.path.basename(script_path).replace(".json", ""))
        self.scripts[script_id] = script_data
        return script_data

    def get_script_info(self, script_id: str) -> Optional[dict]:
        return self.scripts.get(script_id)

    def list_available_scripts(self, scripts_dir: str) -> List[dict]:
        scripts = []
        if not os.path.exists(scripts_dir):
            return scripts
        for filename in os.listdir(scripts_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(scripts_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        data["file_path"] = filepath
                        scripts.append(data)
                except (json.JSONDecodeError, KeyError):
                    continue
        return scripts

    def start_script(self, script_id: str) -> DialogNode:
        script_data = self.scripts.get(script_id)
        if not script_data:
            raise ValueError(f"Script {script_id} not found")

        self.current_script_id = script_id
        self.visited_nodes = []

        nodes_data = script_data.get("nodes", [])
        start_node = None
        for node_data in nodes_data:
            if node_data.get("is_start", False):
                start_node = self._parse_node(node_data)
                break

        if not start_node and nodes_data:
            start_node = self._parse_node(nodes_data[0])

        self.current_node = start_node
        if start_node:
            self.visited_nodes.append(start_node.id)
        return start_node

    def _parse_node(self, node_data: dict) -> DialogNode:
        options_data = node_data.get("options", [])
        options = []
        for opt_data in options_data:
            option = DialogOption(
                id=opt_data["id"],
                text=opt_data["text"],
                next_node_id=opt_data.get("next_node", ""),
                risk_delta=opt_data.get("risk_delta", 0),
                is_safe_choice=opt_data.get("is_safe_choice", False),
                trigger_calm=opt_data.get("trigger_calm", False)
            )
            options.append(option)

        return DialogNode(
            id=node_data["id"],
            speaker=node_data.get("speaker", "骗子"),
            text=node_data.get("text", ""),
            options=options,
            is_start=node_data.get("is_start", False),
            is_end=node_data.get("is_end", False),
            trigger_calm=node_data.get("trigger_calm", False),
            calm_message=node_data.get("calm_message", ""),
            risk_tip=node_data.get("risk_tip", ""),
            node_type=node_data.get("node_type", "normal")
        )

    def get_node_by_id(self, node_id: str) -> Optional[DialogNode]:
        script_data = self.scripts.get(self.current_script_id)
        if not script_data:
            return None
        for node_data in script_data.get("nodes", []):
            if node_data["id"] == node_id:
                return self._parse_node(node_data)
        return None

    def choose_option(self, option_id: str) -> DialogNode:
        if not self.current_node:
            raise RuntimeError("No active dialog in progress")

        chosen_option = None
        for option in self.current_node.options:
            if option.id == option_id:
                chosen_option = option
                break

        if not chosen_option:
            raise ValueError(f"Option {option_id} not found")

        next_node = self.get_node_by_id(chosen_option.next_node_id)
        if next_node:
            self.current_node = next_node
            self.visited_nodes.append(next_node.id)

        return next_node

    def get_current_node(self) -> Optional[DialogNode]:
        return self.current_node

    def is_end(self) -> bool:
        return self.current_node is not None and self.current_node.is_end

    def get_script_metadata(self, script_id: str) -> Optional[dict]:
        script_data = self.scripts.get(script_id)
        if not script_data:
            return None
        return {
            "id": script_data.get("id"),
            "name": script_data.get("name"),
            "description": script_data.get("description", ""),
            "difficulty": script_data.get("difficulty", "medium"),
            "estimated_time": script_data.get("estimated_time", 0),
            "scam_type": script_data.get("scam_type", ""),
        }
