import scrapy
from scrapy.utils.response import open_in_browser
import json


class IftttRuleCreater(scrapy.Spider):
    name = "ifttt.com"
    start_urls = ["https://ifttt.com/login"]
    keys_path = "../.././keys/keys.json"  #因为对于main.ts来说是在electron文件夹层级调用的

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

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                "utf8": "✓",
                # "authenticity_token": authenticity_token,
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

        # yield scrapy.Request(
        #     "https://ifttt.com/api/v3/graph",
        #     method="POST",
        #     body=json.dumps(payload),
        #     headers=headers,
        #     callback=self.get_trigger_by_name,
        #     meta={"module_name": module_name},
        # )

    # def get_trigger_by_name(self, response):
