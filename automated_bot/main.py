import json
import random
import time

import requests
import secrets
import string


class BlogRequestError(Exception):
    pass


class BlogApiClient:
    """
    Special interface for working with blog api
    """
    def __init__(self, base_url: str = None, username: str = None, password: str = None):
        self.base_url = base_url
        self.refresh_token = None
        self.headers = {"Authorization": None}
        self.verify_token_url = self.base_url + '/auth/jwt/verify/'
        self.create_token_url = self.base_url + '/auth/jwt/create/'
        self.refresh_token_url = self.base_url + '/auth/jwt/refresh/'
        self.signup_url = self.base_url + '/auth/users/'
        self.posts_url = self.base_url + '/posts/'
        self.post_init(username, password)

    def post_init(self, username: str, password: str) -> None or BlogRequestError:
        """
        Post init operation for user authentication
        """
        if username and password:
            data = {'username': str(username), 'password': str(password)}
            try:
                self.post(self.signup_url, data=data, expected_status_code=201)
            except BlogRequestError:
                pass
            token_resp = self.post(self.create_token_url, data=data, expected_status_code=200)
            self.refresh_token = token_resp.get('refresh')
            self.headers.update(**{'Authorization': f'JWT {token_resp.get("access")}'})

    def verify_refresh_token(self) -> None or BlogRequestError:
        """
        Verify token and if it has expired, try to refresh
        """
        if not self.headers.get("Authorization", None):
            return
        resp = requests.post(self.verify_token_url, data={"token": self.headers.get("Authorization")})

        if resp.status_code == 401:
            resp = requests.post(self.refresh_token_url, data={"refresh": self.refresh_token})

            if resp.status_code != 200:
                raise BlogRequestError(f'Response status_code: {resp.status_code}\nrefresh: {self.refresh_token}')

            self.headers.update(**{'Authorization': f'JWT {resp.json().get("access")}'})

    def post(self, url: str, data: dict = None, expected_status_code: int = None) -> dict or BlogRequestError:
        """
        POST requests operation
        """
        self.verify_refresh_token()
        resp = requests.post(url, data=data, headers=self.headers)
        if resp.status_code == expected_status_code:
            return resp.json()
        raise BlogRequestError(f'Response status_code: {resp.status_code}\nurl: {url}\ndata: {data}')

    def get(self, url, params: dict = None, expected_status_code: int = None):
        """
        GET requests operation
        """
        self.verify_refresh_token()
        resp = requests.get(url, headers=self.headers, params=params)
        if resp.status_code == expected_status_code:
            return resp.json()
        raise BlogRequestError(f'Response status_code: {resp.status_code}\nurl: {url}\ndata: {data}')

    def create_post(self, data: dict) -> dict:
        """
        Create new post.
        data={
            "title": string,
            "body": string
        }
        """
        resp = self.post(self.posts_url, data=data, expected_status_code=201)
        return resp

    def vote(self, post_id: int, data: dict) -> dict:
        """
        Add new vote for post
        data={
            "vote": int (-1 or 1)
        }
        """
        resp = self.post(f'{self.posts_url}{post_id}/votes/', data=data, expected_status_code=201)
        return resp


class AutomatedBot:
    """
    Automated bot for creating new objects in database through the Blog API
    """
    def __init__(self, configs: dict = None, base_url: str = None):
        self.base_url = base_url
        self.max_users_num = random.randint(1, configs.get('max_users_num'))
        self.max_posts_num_per_user = random.randint(1, configs.get('max_posts_num_per_user'))
        self.max_votes_num_per_user = random.randint(1, configs.get('max_votes_num_per_user'))
        self.api_client = None
        self.posts = []

    @property
    def secure_random_string(self):
        """
        Generate a random string
        """
        secure_str = ''.join((secrets.choice(string.ascii_letters) for i in range(12)))
        return secure_str

    def run(self):
        """
        Bot start
        """
        for user in range(self.max_users_num):
            username = f'user_{self.secure_random_string}'
            password = self.secure_random_string
            self.api_client = BlogApiClient(base_url=self.base_url, username=username, password=password)
            # Initialization time.sleep for a 5 second to show difference
            # between user last login date and last activity date
            time.sleep(5)
            self.create_posts()
            self.vote()

    def vote(self):
        """
        Create Votes objects
        """
        for vote in range(self.max_votes_num_per_user):
            vote = random.choice([1, -1])
            post_id = random.choice([i.get('id') for i in self.posts])
            self.api_client.vote(post_id=post_id, data={"vote": vote})

    def create_posts(self):
        """
        Create Posts objects
        """
        for post in range(self.max_posts_num_per_user):
            data = {
                'title': f'title{post}',
                'body': f'body{post}'
            }
            post_data = self.api_client.create_post(data)
            self.posts.append(post_data)


if __name__ == '__main__':
    """
    Add configs to configs.json file before running bot.
    {
      "max_users_num": integer, Max num of users that bot can create,
      "max_posts_num_per_user": integer, Max num of posts that each user can create,
      "max_votes_num_per_user": integer, Max num of votes that each user can create
    }
    """
    try:
        with open('configs.json', "r") as s:
            data = s.read()
            configs = json.loads(data)
    except FileNotFoundError:
        configs = {}

    auto_bot = AutomatedBot(base_url="http://0.0.0.0:8000", configs=configs)
    auto_bot.run()
