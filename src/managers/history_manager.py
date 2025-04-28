import json
import os
from kivy.event import EventDispatcher
from kivy.properties import ListProperty

class HistoryManager(EventDispatcher):
    history = ListProperty([])
    
    def __init__(self, storage_dir):
        super().__init__()
        self.history_file = os.path.join(storage_dir, 'history.json')
        self.load_history()
    
    def add_link(self, link):
        """Add a new link to history"""
        if link and link not in self.history:
            self.history.append(link)
            self.save_history()
    
    def clear_history(self):
        """Clear all history"""
        self.history.clear()
        self.save_history()
    
    def remove_link(self, link):
        """Remove a specific link from history"""
        if link in self.history:
            self.history.remove(link)
            self.save_history()
    
    def load_history(self):
        """Load history from storage"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
        except Exception as e:
            print(f"Error loading history: {e}")
            self.history = []
    
    def save_history(self):
        """Save history to storage"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(list(self.history), f)
        except Exception as e:
            print(f"Error saving history: {e}")