import scrapy
from scrapy.utils.response import open_in_browser
import json


# 在elecreon_json文件里面的每一个操作trigger/action/query加入设备的mac地址和名称等信息

class IftttElectronSupplementSpider(scrapy.Spider):
    name = "ifttt.com"
    start_urls = ["https://ifttt.com/login"]
    keys_path = "./keys/keys.json"
    trigger_module_name_path = "./data/electron_json/trigger_device_names.json"
    query_module_name_path = "./data/electron_json/query_device_names.json"
    action_module_name_path = "./data/electron_json/action_device_names.json"

    def __init__(self, *args, **kwargs):
        super(IftttElectronSupplementSpider, self).__init__(*args, **kwargs)
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

        # load keys
        with open(self.keys_path, "r") as f:
            keys = json.load(f)
        self.username = keys["username"]
        self.email = keys["email"]
        self.password = keys["password"]
        self.authorization = keys["private-authorization"]

        with open(self.trigger_module_name_path, "r") as f:
            trigger_module_names = json.load(f)
        self.trigger_module_name_list = [item["module_name"] for item in trigger_module_names]

        with open(self.query_module_name_path, "r") as f:
            query_module_names = json.load(f)
        self.query_module_name_list = [item["module_name"] for item in query_module_names]

        with open(self.action_module_name_path, "r") as f:
            action_module_names = json.load(f)
        self.action_module_name_list = [item["module_name"] for item in action_module_names]

    def parse(self, response):
        # open_in_browser(response)

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


    # 注意，由于账号缺乏绑定设备的数据，这里面的if条件判断里加了是否为wemo_switch的判断。后面限制放开后，需要增加获取数据为空时的判断
    def login_check(self, response):
        # check if successfully logged in
        if b"The email and password don&#39;t match." in response.body:
            self.logger.error("Login failed: Wrong username or password.")
            return
        self.logger.info("Successfully login.")

        headers = {"Content-Type": "application/json", "User-Agent": self.user_agent,
                   "Authorization": 'Token jwt="' + self.authorization + '"'}

        for trigger_module_name in self.trigger_module_name_list:
            with open("./data/electron_json/trigger/" + trigger_module_name + ".json", "r") as f:
                module_json = json.load(f)
                for item in module_json:
                    sub_module_name = item["module_name"]
                    sub_module_live_channels = item["live_channels"]
                    for channel in sub_module_live_channels:
                        channel_id = channel["id"]
                        if trigger_module_name == "wemo_switch":
                            queryString = "https://ifttt.com/stored_fields/options?resolve_url=/stored_fields/triggers/" + trigger_module_name + "." + sub_module_name + "/macaddress/options&live_channel_id=" + channel_id
                            yield scrapy.Request(
                                url=queryString,
                                headers=headers,
                                method="GET",
                                callback=self.get_trigger_module_channel_supplement,
                                meta={"module_json": module_json, "trigger_module_name": trigger_module_name,
                                      "sub_module_name": sub_module_name, "channel_id": channel_id}
                            )

        for query_module_name in self.query_module_name_list:
            with open("./data/electron_json/query/" + query_module_name + ".json", "r") as f:
                module_json = json.load(f)
                for item in module_json:
                    sub_module_name = item["module_name"]
                    sub_module_live_channels = item["live_channels"]
                    for channel in sub_module_live_channels:
                        channel_id = channel["id"]
                        if query_module_name == "wemo_switch":
                            queryString = "https://ifttt.com/stored_fields/options?resolve_url=/stored_fields/queries/" + query_module_name + "." + sub_module_name + "/macaddress/options&live_channel_id=" + channel_id
                            yield scrapy.Request(
                                url=queryString,
                                headers=headers,
                                method="GET",
                                callback=self.get_query_module_channel_supplement,
                                meta={"module_json": module_json, "query_module_name": query_module_name,
                                      "sub_module_name": sub_module_name, "channel_id": channel_id}
                            )

        for action_module_name in self.action_module_name_list:
            with open("./data/electron_json/action/" + action_module_name + ".json", "r") as f:
                module_json = json.load(f)
                for item in module_json:
                    sub_module_name = item["module_name"]
                    sub_module_live_channels = item["live_channels"]
                    for channel in sub_module_live_channels:
                        channel_id = channel["id"]
                        if action_module_name == "wemo_switch":
                            queryString = "https://ifttt.com/stored_fields/options?resolve_url=/stored_fields/actions/" + action_module_name + "." + sub_module_name + "/macaddress/options&live_channel_id=" + channel_id
                            yield scrapy.Request(
                                url=queryString,
                                headers=headers,
                                method="GET",
                                callback=self.get_action_module_channel_supplement,
                                meta={"module_json": module_json, "action_module_name": action_module_name,
                                      "sub_module_name": sub_module_name, "channel_id": channel_id}
                            )

    def get_trigger_module_channel_supplement(self, response):
        module_json = response.meta["module_json"]
        trigger_module_name = response.meta["trigger_module_name"]
        sub_module_name = response.meta["sub_module_name"]
        channel_id = response.meta["channel_id"]
        supplement = response.json()
        target_json = module_json
        for item in target_json:
            if item["module_name"] == sub_module_name:
                channels = item["live_channels"]
                for target in channels:
                    if target["id"] == channel_id:
                        handle = {
                            "id": target["id"],
                            "user_name_field": target["user_name_field"],
                            "offline": target["offline"],
                            "macaddress": supplement["macaddress"],
                        }
                        target.update(handle)
        with open("./data/electron_json/trigger/" + trigger_module_name + ".json", "w") as f:
            json.dump(target_json, f, indent=4)

    # 这里欠返回响应为空的判断
    def get_query_module_channel_supplement(self, response):
        module_json = response.meta["module_json"]
        query_module_name = response.meta["query_module_name"]
        sub_module_name = response.meta["sub_module_name"]
        channel_id = response.meta["channel_id"]
        supplement = response.json()
        target_json = module_json
        for item in target_json:
            if (item["module_name"] == sub_module_name):
                channels = item["live_channels"]
                for target in channels:
                    if target["id"] == channel_id:
                        handle = {
                            "id": target["id"],
                            "user_name_field": target["user_name_field"],
                            "offline": target["offline"],
                            "macaddress": supplement["macaddress"],
                        }
                        target.update(handle)
        with open("./data/electron_json/query/" + query_module_name + ".json", "w") as f:
            json.dump(target_json, f, indent=4)

    def get_action_module_channel_supplement(self, response):
        module_json = response.meta["module_json"]
        action_module_name = response.meta["action_module_name"]
        sub_module_name = response.meta["sub_module_name"]
        channel_id = response.meta["channel_id"]
        supplement = response.json()
        target_json = module_json
        for item in target_json:
            if (item["module_name"] == sub_module_name):
                channels = item["live_channels"]
                for target in channels:
                    if target["id"] == channel_id:
                        handle = {
                            "id": target["id"],
                            "user_name_field": target["user_name_field"],
                            "offline": target["offline"],
                            "macaddress": supplement["macaddress"],
                        }
                        target.update(handle)
        with open("./data/electron_json/action/" + action_module_name + ".json", "w") as f:
            json.dump(target_json, f, indent=4)
