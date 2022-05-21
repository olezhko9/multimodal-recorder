class SessionManager:
    def __init__(self, device_manager, record_manager):
        self.device_manager = device_manager
        self.record_manager = record_manager

    def get_session(self):
        return {
            'is_recording': self.record_manager.is_recording(),
            'started_devices': list(self.device_manager.get_devices())
        }
