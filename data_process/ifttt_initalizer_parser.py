import json


# 获取trigger_device_name.json, query_device_name.json, action_device_name.json

class IftttInitalizerParser:
    def __init__(self, json_file: str) -> None:
        with open(json_file, "r") as f:
            self.input_data = json.load(f)


    def parser(self, output_dir: str) -> None:
        self.output_trigger_data = [
            {"module_name": item["module_name"], "name": item["name"]}
            for item in self.input_data["preloadedServices"]
            if item["public_triggers"] != []
        ]
        self.output_query_data = [
            {"module_name": item["module_name"], "name": item["name"]}
            for item in self.input_data["preloadedServices"]
            if item["public_queries"] != []
        ]
        self.output_action_data = [
            {"module_name": item["module_name"], "name": item["name"]}
            for item in self.input_data["preloadedServices"]
            if item["public_actions"] != []
        ]
        output_trigger_str = json.dumps(self.output_trigger_data, indent=4)
        output_queries_str = json.dumps(self.output_query_data, indent=4)
        output_action_str = json.dumps(self.output_action_data, indent=4)

        # with open(output_file, "w") as f:
        #     f.write(output_str)
        with open(output_dir + "trigger_device_names.json", "w") as f:
            f.write(output_trigger_str)
        with open(output_dir + "query_device_names.json", "w") as f:
            f.write(output_queries_str)
        with open(output_dir + "action_device_names.json", "w") as f:
            f.write(output_action_str)


if __name__ == "__main__":
    iip = IftttInitalizerParser("./data/public_module.json")
    iip.parser("./data/electron_json/")
