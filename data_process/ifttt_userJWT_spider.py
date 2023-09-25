import scrapy
import json
import re
from scrapy.utils.response import open_in_browser


class ifttt_userJWT_spider(scrapy.Spider):
    name = "ifttt.com"
    start_urls = ["https://ifttt.com/login"]
    keys_path = "./keys/keys.json"
    module_name_path = "./data/module_name.json"

    def __init__(self, *args, **kwargs):
        super(ifttt_userJWT_spider, self).__init__(*args, **kwargs)

        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

        # load keys
        with open(self.keys_path, "r") as f:
            keys = json.load(f)
        self.username = keys["username"]
        self.email = keys["email"]
        self.password = keys["password"]
        # self.authorization = keys["authorization"]

    def parse(self, response):
        # open_in_browser(response)
        # get authenticity token
        # self.logger.info(response.text)

        # authenticity_token = response.css(
        #     "input[type=hidden]:nth-child(2)::attr(value)"
        # ).get()

        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                "utf8": "✓",
                #"authenticity_token": authenticity_token,
                "return_to": None,
                "psu_": None,
                "user[username]": self.email,
                "user[password]": self.password,
                "commit": "Log+in",
            },
            headers={"User-Agent": self.user_agent},
            callback=self.login_check,
        )

    def login_check(self, response):
        # check if successfully logged in
        if b"The email and password don&#39;t match." in response.body:
            self.logger.error("Login failed: Wrong username or password.")
            return

        self.logger.info("Successfully login.")

        headers = {
            "Content-Type": "text/html; charset=utf-8",
        }

        yield scrapy.Request(
            "https://ifttt.com/create",
            method="GET",
            headers=headers,
            callback=self.get_JWTtoken,
        )

    def get_JWTtoken(self, response):
        # open_in_browser(response)
        # self.logger.info(response.text)

        pattern_JWT = r'userJWT:\s*\'(.*?)\''
        pattern_authenticityToken = r'authenticityToken:\s*\'(.*?)\''

        with open("./keys/keys.json", "r") as f:
            data = json.load(f)

        match_JWT = re.search(pattern_JWT, response.text)
        if match_JWT:
            user_jwt = match_JWT.group(1)
            data["private-authorization"] = user_jwt
            with open("./keys/keys.json", "w") as f:
                json.dump(data, f, indent=4)

        match_authenticityToken = re.search(pattern_authenticityToken,response.text)
        if match_authenticityToken:
            authenticity = match_authenticityToken.group(1)
            data["authorization"] = authenticity
            with open("./keys/keys.json", "w") as f:
                json.dump(data, f, indent=4)
