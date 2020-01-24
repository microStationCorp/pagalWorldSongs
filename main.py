from bs4 import BeautifulSoup
import requests
import json


class pwScrapper:
    MAIN_DATA_LIST = []
    BASE_URL = "https://www.pagalworld.mobi"
    ALL_CATEGORY_URL = "https://www.pagalworld.mobi/a-to-z-bollywood-mp3-songs/list.html"

    def all_category(self):
        response = requests.get(self.ALL_CATEGORY_URL)
        category_list = []
        soup = BeautifulSoup(response.content, 'html.parser')
        anchorDiv = soup.find_all('div', class_='div-nogap')
        anchors = anchorDiv[1].find_all('a')
        for anchor in anchors:
            print(anchor['title'])
            category_list.append({
                'category': anchor['title'],
                'url': self.BASE_URL + anchor['href'],
                'movies': self.get_movie_list(self.BASE_URL + anchor['href'])
            }
        return category_list

    def get_movie_list(self, URL):
        page_list = self.get_page_list(URL)
        movie_list = []
        if page_list != None:
            for url in page_list:
                movie_list = movie_list + self.movie_list_in_page(url)
        else:
            movie_list = self.movie_list_in_page(URL)
        return movie_list

    def movie_list_in_page(self, URL):
        movie_data = []
        response = requests.get(URL)
        soup = BeautifulSoup(response.content, 'html.parser')
        div = soup.find_all(id='w0')
        h3 = div[0].find_all('h3')
        for i in h3:
            print("movie name: " + i.a.text)
            movie_data.append({
                'movie-name': i.a.text,
                'url': self.BASE_URL + i.a['href'],
                'songs': self.get_songs(self.BASE_URL + i.a['href'], i.a.text)
            })
        return movie_data

    def get_dLink(self, URL):
        response = requests.get(URL)
        dLink = []
        soup = BeautifulSoup(response.content, 'html.parser')
        div = soup.find_all('div', class_='downloaddiv')
        for i in div:
            dLink.append({
                'dLink': i.a['href']
            })
        return dLink

    def get_songs(self, URL, title):
        response = requests.get(URL)
        soup = BeautifulSoup(response.content, 'html.parser')
        divList = soup.find_all('div', class_='listbox')
        songList = []
        for i in divList:
            print("song name: " + i.a.h2.text)
            if i.a.h2.text.find('Title') != -1 or i.a.h2.text.find('Theme') != -1:
                new_title = i.a.h2.text + " " + title
            else:
                new_title = i.a.h2.text
            songList.append({
                'song-name': new_title,
                'url': self.BASE_URL + i.a['href'],
                'dLink': self.get_dLink(self.BASE_URL + i.a['href'])
            })
        return songList

    def get_page_list(self, URL):
        try:
            total_page_url_list = []
            response = requests.get(URL)
            soup = BeautifulSoup(response.content, 'html.parser')

            ul = soup.find_all('ul', class_='name-sort')
            anchors = ul[0].find_all('a')
            for anchor in anchors:
                if anchor.text != '»':
                    total_page_url_list.append(self.BASE_URL + anchor['href'])
            return total_page_url_list
        except:
            return None


if __name__ == '__main__':
    data = pwScrapper()
    movies = data.all_category()
    with open('movies.json', 'w') as file:
        json.dump(movies, file, indent=4)
        print(json.dumps(movies, indent=4))
