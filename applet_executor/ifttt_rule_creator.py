import scrapy
from scrapy.utils.response import open_in_browser
import json


class IftttRuleCreater(scrapy.Spider):
    name = "ifttt.com"
    start_urls = ["https://ifttt.com/login"]
    keys_path = "../.././keys/keys.json"  # 因为对于main.ts来说是在electron文件夹层级调用的
    module_id_path = "../../data/public_module.json"

    def __init__(self, *args, **kwargs) -> None:
        super(IftttRuleCreater, self).__init__(*args, **kwargs)

        self.trigger_device = kwargs["trigger_device"]
        self.trigger_condition = kwargs["trigger_condition"]
        self.trigger_DAC = kwargs["trigger_DAC"]
        self.trigger_DSN = kwargs["trigger_DSN"]
        self.query_device = kwargs["query_device"]
        self.query_content = kwargs["query_content"]
        self.query_DAC = kwargs["query_DAC"]
        self.query_DSN = kwargs["query_DSN"]
        self.action_device = kwargs["action_device"]
        self.action_execution = kwargs["action_execution"]
        self.action_DAC = kwargs["action_DAC"]
        self.action_DSN = kwargs["action_DSN"]
        self.is_pro = kwargs["is_pro"]
        self.priority = kwargs["priority"]

        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        # load keys
        with open(self.keys_path, "r") as f:
            keys = json.load(f)
        self.username = keys["username"]
        self.email = keys["email"]
        self.password = keys["password"]
        self.authorization = keys["private-authorization"]

        with open(self.module_id_path, "r") as f:
            module_id_list = json.load(f)
        for item in module_id_list["preloadedServices"]:
            if item["module_name"] == self.trigger_device:
                self.trigger_channel = item["id"]
            if (item["module_name"]) == self.query_device:
                self.query_channel = item["id"]
            if (item["module_name"]) == self.action_device:
                self.action_channel = item["id"]

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                "utf8": "✓",
                "return_to": None,
                "psu_": None,
                "user[username]": self.email,
                "user[password]": self.password,
                "commit": "Log+in",
            },
            headers={"User-Agent": self.user_agent, "Authorization": 'Token jwt="' + self.authorization + '"'},
            callback=self.login_check,
        )

    def login_check(self, response):
        # check if successfully logged in
        if b"The email and password don&#39;t match." in response.body:
            self.logger.error("Login failed: Wrong username or password.")
            return

        self.logger.info("Successfully login.")
        headers = {"Content-Type": "application/json", "User-Agent": self.user_agent,
                   "Authorization": 'Token jwt="' + self.authorization + '"'}

        payload = {
            "query": "\n  mutation DIYCreateAppletMutation(\n    $name: String!\n    $description: String\n    $channel_id: ID!\n    $push_enabled: Boolean\n    $filter_code: String\n    $trigger: DiyTandaInput!\n    $queries: [DiyTandaInput]\n    $actions: [DiyTandaInput]!\n    $actions_delay: Int\n  ) {\n    diyAppletCreate(\n      input: {\n        name: $name\n        description: $description\n        channel_id: $channel_id\n        filter_code: $filter_code\n        push_enabled: $push_enabled\n        trigger: $trigger\n        queries: $queries\n        actions: $actions\n        actions_delay: $actions_delay\n      }\n    ) {\n      errors {\n        attribute\n        message\n      }\n      normalized_applet {\n        id\n      }\n    }\n  }\n",
            "variables": {"name": "This is an automated created testing rule", "channel_id": self.trigger_channel,
                          "filter_code": "",
                          "trigger": {"step_identifier": self.trigger_device + "." + self.trigger_condition,
                                      "fields": [{"name": "macaddress", "hidden": "false", "value": self.trigger_DSN}],
                                      "channel_id": self.trigger_channel, "live_channel_id": self.trigger_DAC},
                          "actions": [{"step_identifier": self.action_device + "." + self.action_execution,
                                       "fields": [{"name": "macaddress", "hidden": "false", "value": self.action_DSN}],
                                       "channel_id": self.action_channel, "live_channel_id": self.action_DAC}],
                          "queries": [
                              {"step_identifier": self.query_device + "." + self.query_content,
                               "fields": [{"name": "macaddress", "hidden": "false", "value": self.query_DSN}],
                               "channel_id": self.query_channel, "live_channel_id": self.query_DAC}],
                          "actions_delay": 0},
        }

        yield scrapy.Request(
            "https://ifttt.com/api/v3/graph",
            method="POST",
            body=json.dumps(payload),
            headers=headers,
            callback=self.check_rule_create,
        )

    def check_rule_create(self, response):
        print(response.text)