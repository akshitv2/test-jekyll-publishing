class LogUtil:
    # Define level constants
    LEVELS = {
        "trace": 0,
        "debug": 1,
        "info": 2,
        "off": 3
    }

    def __init__(self, loglevel="info"):
        """Initializes the logger with a specific threshold."""
        self.threshold = self.LEVELS.get(loglevel.lower(), 2)

    def _should_log(self, level_name):
        return self.LEVELS[level_name] >= self.threshold

    def trace(self, message):
        if self._should_log("trace"):
            print(f"[TRACE] {message}")

    def debug(self, message):
        if self._should_log("debug"):
            print(f"[DEBUG] {message}")

    def info(self, message):
        if self._should_log("info"):
            print(f"[INFO] {message}")