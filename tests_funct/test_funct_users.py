import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


class TestRegisterPage(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(
            executable_path='/mnt/c/webdrivers/chromedriver.exe'
        )

    def tearDown(self):
        self.browser.close()

    def test_valid_registration(self):
        self.browser.get(self.live_server_url + reverse("register") )
        time.sleep(1)
        self.browser.find_element_by_name("username").send_keys("elvis")
        time.sleep(1)
        self.browser.find_element_by_name("email").send_keys("elvis@isnotdead.com")
        time.sleep(1)
        self.browser.find_element_by_name("password1").send_keys("Dickrivers76")
        time.sleep(1)
        self.browser.find_element_by_name("password2").send_keys("Dickrivers76")
        time.sleep(1)
        self.browser.find_element_by_id("btn-register").click()
        time.sleep(5)
        redirection_url = self.live_server_url + reverse("login")
        self.assertEquals(self.browser.current_url, redirection_url)

    def test_invalid_registration_missing_login(self):
        self.browser.get(self.live_server_url + reverse("register"))
        time.sleep(1)
        self.browser.find_element_by_name("email").send_keys("jojo@labuvette.com")
        time.sleep(1)
        self.browser.find_element_by_name("password1").send_keys("Dickrivers76")
        time.sleep(1)
        self.browser.find_element_by_name("password2").send_keys("Dickrivers76")
        time.sleep(1)
        self.browser.find_element_by_id("btn-register").click()
        time.sleep(5)
        self.assertEquals(self.browser.current_url, self.live_server_url + reverse("register"))

    def test_invalid_registration_missing_email(self):
        self.browser.get(self.live_server_url + reverse("register"))
        time.sleep(1)
        self.browser.find_element_by_name("username").send_keys("jojo")
        time.sleep(1)
        self.browser.find_element_by_name("password1").send_keys("Dickrivers76")
        time.sleep(1)
        self.browser.find_element_by_name("password2").send_keys("Dickrivers76")
        time.sleep(1)
        self.browser.find_element_by_id("btn-register").click()
        time.sleep(5)
        self.assertEquals(self.browser.current_url, self.live_server_url + reverse("register"))

    def test_invalid_registration_missing_pwd1(self):
        self.browser.get(self.live_server_url + reverse("register"))
        time.sleep(1)
        self.browser.find_element_by_name("username").send_keys("jojo")
        time.sleep(1)
        self.browser.find_element_by_name("email").send_keys("jojo@labuvette.com")
        time.sleep(1)
        self.browser.find_element_by_name("password2").send_keys("Dickrivers76")
        time.sleep(1)
        self.browser.find_element_by_id("btn-register").click()
        time.sleep(5)
        self.assertEquals(self.browser.current_url, self.live_server_url + reverse("register"))



class TestLoginPage(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(
            executable_path='/mnt/c/webdrivers/chromedriver.exe'
        )

    def tearDown(self):
        self.browser.close()

    def test_valid_login(self):
        self.browser.get(self.live_server_url + reverse("register") )
        time.sleep(1)
        self.browser.find_element_by_name("username").send_keys("bobby")
        time.sleep(1)
        self.browser.find_element_by_name("email").send_keys("bobby@isnotdead.com")
        time.sleep(1)
        self.browser.find_element_by_name("password1").send_keys("Dickrivers76")
        time.sleep(1)
        self.browser.find_element_by_name("password2").send_keys("Dickrivers76")
        time.sleep(1)
        self.browser.find_element_by_id("btn-register").click()
        time.sleep(5)
        redirection_url = self.live_server_url + reverse("login")
        self.assertEquals(self.browser.current_url, redirection_url)
        self.browser.find_element_by_name("username").send_keys("bobby")
        time.sleep(1)
        self.browser.find_element_by_name("password").send_keys("Dickrivers76")
        self.browser.find_element_by_id("btn-login").click()
        time.sleep(5)
        self.assertEquals(self.browser.current_url, self.live_server_url + '/')

class TestUserInformationPage(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(
            executable_path='/mnt/c/webdrivers/chromedriver.exe'
        )

    def tearDown(self):
        self.browser.close()

    def test_valid_profile(self):
        self.browser.get(self.live_server_url + reverse("register") )
        time.sleep(1)
        self.browser.find_element_by_name("username").send_keys("robert")
        time.sleep(1)
        self.browser.find_element_by_name("email").send_keys("robert@isnotdead.com")
        time.sleep(1)
        self.browser.find_element_by_name("password1").send_keys("Dickrivers76")
        time.sleep(1)
        self.browser.find_element_by_name("password2").send_keys("Dickrivers76")
        time.sleep(1)
        self.browser.find_element_by_id("btn-register").click()
        time.sleep(5)
        redirection_url = self.live_server_url + reverse("login")
        self.assertEquals(self.browser.current_url, redirection_url)
        self.browser.find_element_by_name("username").send_keys("robert")
        time.sleep(1)
        self.browser.find_element_by_name("password").send_keys("Dickrivers76")
        self.browser.find_element_by_id("btn-login").click()
        time.sleep(5)
        self.browser.find_element_by_id("profile-link").click()
        time.sleep(5)
        redirection_url = self.live_server_url + reverse("profile")
        self.assertEquals(self.browser.current_url, redirection_url)
        email = self.browser.find_element_by_id("p-email").text
        self.assertEquals(email, "robert@isnotdead.com" )
        login = self.browser.find_element_by_id("profile-un").text
        self.assertEquals(login, "robert" )

class TestUserInformationPage(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(
            executable_path='/mnt/c/webdrivers/chromedriver.exe'
        )

    def tearDown(self):
        self.browser.close()

    def test_valid_user_products(self):
        self.browser.get(self.live_server_url + reverse("register") )
        time.sleep(1)
        self.browser.find_element_by_name("username").send_keys("brenda")
        time.sleep(1)
        self.browser.find_element_by_name("email").send_keys("brendat@isnotdead.com")
        time.sleep(1)
        self.browser.find_element_by_name("password1").send_keys("Dickrivers76")
        time.sleep(1)
        self.browser.find_element_by_name("password2").send_keys("Dickrivers76")
        time.sleep(1)
        self.browser.find_element_by_id("btn-register").click()
        time.sleep(5)
        redirection_url = self.live_server_url + reverse("login")
        self.assertEquals(self.browser.current_url, redirection_url)
        self.browser.find_element_by_name("username").send_keys("brenda")
        time.sleep(1)
        self.browser.find_element_by_name("password").send_keys("Dickrivers76")
        self.browser.find_element_by_id("btn-login").click()
        time.sleep(5)
        self.browser.find_element_by_id("selections-link").click()
        time.sleep(5)
        redirection_url = self.live_server_url + reverse("user_search")
        self.assertEquals(self.browser.current_url, redirection_url)
        
