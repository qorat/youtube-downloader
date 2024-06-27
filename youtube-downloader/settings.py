import json
import os

class Settings:
    def __init__(self):
        self.settings_file = 'user_settings.json'
        self.default_settings = {
            'default_output_path': os.path.expanduser('~/Downloads'),
            'default_video_quality': '720p',
            'default_audio_quality': '128kbps',
            'keep_temp_files': False,
            'auto_rename_existing': True
        }
        self.current_settings = self.load_settings()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        return self.default_settings.copy()

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.current_settings, f, indent=4)

    def get(self, key):
        return self.current_settings.get(key, self.default_settings.get(key))

    def set(self, key, value):
        self.current_settings[key] = value
        self.save_settings()

    def reset_to_default(self):
        self.current_settings = self.default_settings.copy()
        self.save_settings()