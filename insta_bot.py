from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException


class InstaBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome("C:\chromedriver.exe")
        self.username = username
        self.driver.get("https://instagram.com")
        sleep(10)
        self.driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
        self.driver.find_element_by_xpath("//input[@name='password']").send_keys(pw)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        sleep(10)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        sleep(5)

    def get_unfollowers(self):
        """Contains all functions and final run"""
        self.driver.find_element_by_xpath("//a[contains(@href, '" + self.username + "')]").click()
        sleep(15)
        self.driver.find_element_by_xpath("//a[contains(@href, 'following')]").click()
        self._scroll_names()
        verified = self._get_celebs()  # Get the name of usernames with verified badge
        following = self._get_names()  # list of names of following
        self.driver.find_element_by_xpath("//a[contains(@href, 'followers')]").click()
        self._scroll_names()
        followers = self._get_names()  # List of names of followers

        # Remove the list of verified usernames from the list
        celeb_following = [user for user in following if user not in verified]

        # Remove the list of people who dont follow back from the list
        self.not_following_back = [user for user in celeb_following if user not in followers and user != ' ']

        # Sends a list of unfaithful persons names to a file
        myfile = open('unfaithful.txt', 'w')
        myfile.write("Unfaithful persons in your life: \n")
        for name in self.not_following_back:
            myfile.write(name)
            myfile.write('\n')
        myfile.close()

        self.driver.find_element_by_xpath("//a[contains(@href, 'following')]").click()
        self._scroll_names()
        self._unfollower()

    def _scroll_names(self):
        """Scroll the following /  followers list box"""
        sleep(10)
        self.scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        sleep(4)
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(5)
            ht = self.driver.execute_script("""
                    arguments[0].scrollTo(0, arguments[0].scrollHeight);
                    return arguments[0].scrollHeight;
                    """, self.scroll_box)

    def _get_names(self):
        """Returns the usernames in the following and followers list"""
        links = self.scroll_box.find_elements_by_tag_name('a')

        names = [name.text for name in links if name.text != ' ']
        sleep(3)

        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click()
        return names

    def _get_celebs(self):
        """Returns the usernames with verified badges"""
        links_list = self.scroll_box.find_elements_by_class_name("d7ByH")  # Takes a list of usernmaes in the scrollbox
        names_list = []
        for link in links_list:
            try:
                if link.find_element_by_tag_name('span'):
                    user = link.find_element_by_tag_name('a').text
                    names_list.append(user)
            except NoSuchElementException:
                pass

        # Copy the user text from the names list
        names = [name for name in names_list if name != ' ']
        return names

    def _unfollower(self):
        """Unfollows the unfaithful piece of shit"""
        names_list_1 = []
        for nf in self.not_following_back:
            name = self.scroll_box.find_element_by_xpath("//a[@title='" + nf + "']/ancestor::div[@class = 'uu6c_']")
            names_list_1.append(name)

        for i in names_list_1:
            i.find_element_by_xpath(".//div[@class='Pkbci']/button").click()
            sleep(2)
            self.driver.find_element_by_xpath("//button[@class='aOOlW -Cab_   ']").click()
            sleep(2)


my_bot = InstaBot("username", "password")  # Pass your username and password
my_bot.get_unfollowers()




