class TraceEvent:

    def __init__(self, stage: str, inputs: str, outputs_summary: str, timing_ms: int, error: str = None):
        self.__stage = stage
        self.__inputs = inputs
        self.__outputs_summary = outputs_summary
        self.__timing_ms = timing_ms
        self.__error = error

    # Getter methods
    def get_stage(self) -> str:
        return self.__stage

    def get_inputs(self) -> str:
        return self.__inputs

    def get_outputs_summary(self) -> str:
        return self.__outputs_summary

    def get_timing_ms(self) -> int:
        return self.__timing_ms

    def get_error(self) -> str:
        return self.__error

    def has_error(self) -> bool:
        return self.__error is not None

    def to_json(self) -> str:
        json_parts = [
            f'"stage":"{self.__escape_json(self.__stage)}"',
            f'"inputs":"{self.__escape_json(self.__inputs)}"',
            f'"outputsSummary":"{self.__escape_json(self.__outputs_summary)}"',
            f'"timingMs":{self.__timing_ms}'
        ]
        if self.__error is not None:
            json_parts.append(f'"error":"{self.__escape_json(self.__error)}"')
        return "{" + ",".join(json_parts) + "}"

    # Private helper method
    def __escape_json(self, s: str) -> str:
        if s is None:
            return ""
        return s.replace("\\", "\\\\") \
                .replace("\"", "\\\"") \
                .replace("\n", "\\n") \
                .replace("\r", "\\r") \
                .replace("\t", "\\t")
