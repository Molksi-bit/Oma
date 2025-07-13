import json
import os
from typing import Optional

SETTINGS_PATH = "user_data.json"
MAX_HISTORY = 10

class UserDataManager:
    def __init__(self, path=SETTINGS_PATH):
        self.path = path
        self.data = {
            "search_history": [],
            "recent_sections": {}, 
            "last_file": ""
        }
        self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                try:
                    self.data = json.load(f)
                except json.JSONDecodeError:
                    print("[warn] Konnte Benutzerdaten nicht laden – Datei wird neu erstellt.")
        else:
            self.save()

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def add_search_term(self, term: str):
        term = term.strip()
        if term and term not in self.data["search_history"]:
            self.data["search_history"].insert(0, term)
            self.data["search_history"] = self.data["search_history"][:MAX_HISTORY]
            self.save()

    def get_search_history(self):
        return self.data["search_history"]

    
    def record_section_use(self, lattice_name: str, section: str):
        if lattice_name not in self.data["recent_sections"]:
            self.data["recent_sections"][lattice_name] = {}
        counts = self.data["recent_sections"][lattice_name]
        counts[section] = counts.get(section, 0) + 1
        self.save()

    def get_most_used_section(self, lattice_name: str) -> Optional[str]:
        sections = self.data["recent_sections"].get(lattice_name, {})
        if not sections:
            return None
        return max(sections, key=sections.get)
    
    def set_last_file(self, path: str):
        self.data["last_file"] = path
        self.save()
    
    def get_last_file(self) -> str:
        return self.data.get("last_file", "")
