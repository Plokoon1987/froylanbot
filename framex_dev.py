from urllib import request
import json
import statistics

BASE_URL = 'https://framex-dev.wadrid.net/api/video/Falcon%20Heavy%20Test%20Flight%20(Hosted%20Webcast)-wbSwFU6tY1c'

class Video:
    def __init__(self, base_url):
        self.base_url = base_url
        self.response_dict = self.get_video_dict()
        self.bisect_endpoints = [0, self.response_dict['frames'] - 1]

    def get_video_dict(self):
        response = request.urlopen(self.base_url)
        response = response.read().decode('utf-8')
        return json.loads(response)

    def can_bisect(self):
        return self.bisect_endpoints[0] < self.bisect_endpoints[1]

    def get_frame(self, index):
        return '{}/frame/{}'.format(self.base_url, index)

    def bisect_frame(self):
        if self.bisect_endpoints[1] - self.bisect_endpoints[0] <= 1:
            # endpoint[1] is never returned until the very end
            return self.bisect_endpoints[1]
        return round(statistics.mean(self.bisect_endpoints))

    def remove(self, answer):
        if answer == 'gte':
            # Removes any value >= bisect_frame()
            self.bisect_endpoints[1] = self.bisect_frame() - 1
        elif answer == 'lt':
            # Removes any value < bisect_frame()
            self.bisect_endpoints[0] = self.bisect_frame()


def main():
    vid = Video(BASE_URL)
    counter = 0
#    answers = 'nynyynyyynyynnny'
    answers = 'nnnnnnnnnnnnnnnnnnnn'

    while vid.can_bisect():
        print(vid.bisect_endpoints)
        index = vid.bisect_frame()
        print(index)
#        answer = input('Did the rocket launch yet?   (Y/n)')
        answer = answers[counter]
        print(answer)
        if answer.lower() in ['', 'y']:
            vid.remove('gte')
            counter += 1
        elif answer.lower() == 'n':
            vid.remove('lt')
            counter += 1
        else:
            print('That is not a valid answer')
    print(vid.bisect_frame())


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
