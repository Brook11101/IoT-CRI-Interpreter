import json
import os


class ElectronJsonParser:
    def __init__(
            self,
            in_trigger_folder,
            in_query_folder,
            in_action_folder,
            out_trigger_folder,
            out_query_folder,
            out_action_folder,
            private_path,
            trigger_names,
            query_names,
            action_names,
    ) -> None:
        self.in_trigger_folder = in_trigger_folder
        self.in_query_folder = in_query_folder
        self.in_action_folder = in_action_folder

        self.out_trigger_folder = out_trigger_folder
        self.out_query_folder = out_query_folder
        self.out_action_folder = out_action_folder
        self.private_path = private_path

        self.trigger_names = trigger_names
        self.query_names = query_names
        self.action_names = action_names

    def run(self):
        self.handle_all(self.in_trigger_folder, self.out_trigger_folder, "trigger")
        self.handle_all(self.in_query_folder, self.out_query_folder, "query")
        self.handle_all(self.in_action_folder, self.out_action_folder, "action")
        # self.parse_private(self.private_path)

    def handle_all(self, input_dir, output_dir, type):
        filenames = os.listdir(input_dir)
        for filename in filenames:
            self.handle_file(filename, input_dir, output_dir, type)

    def handle_file(self, filename, input_dir, output_dir, type):
        with open(input_dir + filename) as f:
            input_json = json.load(f)
        output_json = self.parse_json(input_json, type)
        if output_json == "":
            return
        output_str = json.dumps(output_json, indent=4)
        with open(output_dir + filename, "w+") as wf:
            wf.write(output_str)

    def parse_json(self, json_dict, type):
        if json_dict["data"]["channel"] is None:
            return ""

        item_channel = json_dict["data"]["channel"]["live_channels"]
        # 根据trigger query action三种不同格式清洗出electron需要的数据
        if type == "trigger":
            items = json_dict["data"]["channel"]["public_triggers"]
            item_names = [
                {
                    "module_name": item["module_name"],
                    "name": item["name"],
                    "description": item["description"],
                    "id": item["id"],
                    "weight": item["weight"],
                    "trigger_fields_num":len(item["trigger_fields"]),
                    "trigger_fields": [
                        {
                            "name": fields["name"],
                            "label": fields["label"],
                            "hideable": fields["hideable"],
                            "normalized_field_type": fields["normalized_field_type"],
                            "helper_text": fields["helper_text"],
                        }
                        for fields in item["trigger_fields"]
                        if item["trigger_fields"] != []
                    ],
                    "ingredients": [
                        {
                            "id": ingre["id"],
                            "name": ingre["name"],
                            "normalized_name": ingre["normalized_name"],
                            "note": ingre["note"],
                            "value_type": ingre["value_type"],
                        }
                        for ingre in item["ingredients"]
                        if item["ingredients"] != []
                    ],
                    "live_channels": item_channel
                }
                for item in items
                if "ingredients" in item
            ]
            if item_names == []:
                return ""


        elif type == "query":
            items = json_dict["data"]["channel"]["public_queries"]
            item_names = [
                {
                    "module_name": item["module_name"],
                    "name": item["name"],
                    "description": item["description"],
                    "id": item["id"],
                    "weight": item["weight"],
                    "query_fields_num": len(item["query_fields"]),
                    "query_fields": [
                        {
                            "name": fields["name"],
                            "label": fields["label"],
                            "hideable": fields["hideable"],
                            "normalized_field_type": fields["normalized_field_type"],
                            "helper_text": fields["helper_text"],
                        }
                        for fields in item["query_fields"]
                        if item["query_fields"] != []
                    ],
                    "ingredients": [
                        {
                            "id": ingre["id"],
                            "name": ingre["name"],
                            "normalized_name": ingre["normalized_name"],
                            "note": ingre["note"],
                            "value_type": ingre["value_type"],
                        }
                        for ingre in item["ingredients"]
                        if item["ingredients"] != []
                    ],
                    "live_channels": item_channel
                }
                for item in items
                if "ingredients" in item
            ]
            if item_names == []:
                return ""
        else:
            items = json_dict["data"]["channel"]["public_actions"]
            item_names = [
                {
                    "module_name": item["module_name"],
                    "name": item["name"],
                    "description": item["description"],
                    "id": item["id"],
                    "weight": item["weight"],
                    "action_fields_num": len(item["action_fields"]),
                    "action_fields": [
                        {
                            "name": fields["name"],
                            "label": fields["label"],
                            "hideable": fields["hideable"],
                            "normalized_field_type": fields["normalized_field_type"],
                            "helper_text": fields["helper_text"],
                        }
                        for fields in item["action_fields"]
                        if item["action_fields"] != []
                    ],
                    "live_channels": item_channel
                }
                for item in items
            ]
            if item_names == []:
                return ""

        return item_names

    # private可以暂时先不处理 处理所有格式化的T A
    # def parse_private(self, private_path):
    #     with open(private_path) as f:
    #         private_json = json.load(f)
    #
    #     append_trigger_names = []
    #     append_action_names = []
    #
    #     items = private_json["data"]["me"]["private_channels"]
    #     for item in items:
    #         triggers = [
    #             {
    #                 "module_name": trigger_item["module_name"],
    #                 "name": trigger_item["name"],
    #             }
    #             for trigger_item in item["public_triggers"]
    #         ]
    #         actions = [
    #             {
    #                 "module_name": action_item["module_name"],
    #                 "name": action_item["name"],
    #             }
    #             for action_item in item["public_actions"]
    #         ]
    #         module_name = item["module_name"]
    #         output_trigger_str = json.dumps(triggers, indent=4)
    #         if triggers != []:
    #             with open(self.out_trigger_folder + module_name + ".json", "w+") as wf:
    #                 wf.write(output_trigger_str)
    #             append_trigger_names.append(
    #                 {"module_name": item["module_name"], "name": item["name"]}
    #             )
    #         output_action_str = json.dumps(actions, indent=4)
    #         if actions != []:
    #             with open(self.out_action_folder + module_name + ".json", "w+") as wf:
    #                 wf.write(output_action_str)
    #             append_action_names.append(
    #                 {"module_name": item["module_name"], "name": item["name"]}
    #             )
    #     self.update_names(append_trigger_names, append_action_names)
    #
    # def update_names(self, append_trigger_devices, append_action_devices):
    #     with open(self.trigger_names) as f:
    #         trigger_names_json = json.load(f)
    #     with open(self.action_names) as f:
    #         action_names_json = json.load(f)
    #     for item in append_trigger_devices:
    #         trigger_names_json.append(item)
    #     for item in append_action_devices:
    #         action_names_json.append(item)
    #     # trigger_names_json = trigger_names_json + append_trigger_devices
    #     # action_names_json = action_names_json + append_action_devices
    #     with open(self.trigger_names, "w") as wf:
    #         wf.write(json.dumps(trigger_names_json, indent=4))
    #     with open(self.action_names, "w") as wf:
    #         wf.write(json.dumps(action_names_json, indent=4))


if __name__ == "__main__":
    input_trigger_dir = "./data/trigger_json/"  # trigger完整信息的目录
    output_trigger_dir = "./data/electron_json/trigger/"  # 输出trigger name与trigger说明
    input_query_dir = "./data/query_json/"
    output_query_dir = "./data/electron_json/query/"
    input_action_dir = "./data/action_json/"  # action信息的完整目录
    output_action_dir = "./data/electron_json/action/"  # 输出action name与action说明
    private_json = "./data/private_module.json"

    trigger_names = "./data/electron_json/trigger_device_names.json"  # trigger的索引
    query_names = "./data/electron_json/query_device_name.json"
    action_names = "./data/electron_json/action_device_names.json"  # action的索引

    ejp = ElectronJsonParser(
        input_trigger_dir,
        input_query_dir,
        input_action_dir,
        output_trigger_dir,
        output_query_dir,
        output_action_dir,
        private_json,
        trigger_names,
        query_names,
        action_names,
    )
    ejp.run()
