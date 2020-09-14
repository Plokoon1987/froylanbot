"""Module to manage the Video object."""

import sys
from urllib import request
import json
import statistics


class Video:
    """Manages Video obtained from the Framex-Dev API."""

    def __init__(self, base_url):
        """base_url is the source of the Video object from the API.

        base_url is the maximum common denominator when establishing the
        request url
        response_dict is the metadata obtained from the API
        bisect_endpoints are the min and max values to be checked
        """
        self.base_url = base_url
        self.response_dict = self.get_video_dict()
        self.bisect_endpoints = [0, self.response_dict['frames'] - 1]

    def get_video_dict(self):
        """Request to get the Video's metadata as a dict."""
        response = request.urlopen(self.base_url)
        response = response.read().decode('utf-8')
        return json.loads(response)

    def can_bisect(self):
        """Veryfies that bisect_endpoints is bisectable.

        In other words, a midpoint can be obtained from it
        """
        return self.bisect_endpoints[0] < self.bisect_endpoints[1]

    def get_frame(self, index):
        """Complete url to be requested to the API."""
        return '{}/frame/{}'.format(self.base_url, index)

    def bisect_frame(self):
        """Frame to be requested to the API.

        It is established as the midpoint of the bisect_endpoints list unless
        the two points in bisect_endpoints are contiguous. In that case the
        the last element in bisect_enpoints is returned
        """
        if self.bisect_endpoints[1] - self.bisect_endpoints[0] <= 1:
            # endpoint[1] is never returned until the very end
            return self.bisect_endpoints[1]
        return round(statistics.mean(self.bisect_endpoints))

    def remove(self, answer):
        """Min or Max values are set depending on answer from user."""
        if answer == 'gte':
            # Removes any value >= bisect_frame()
            self.bisect_endpoints[1] = self.bisect_frame() - 1
        elif answer == 'lt':
            # Removes any value < bisect_frame()
            self.bisect_endpoints[0] = self.bisect_frame()


def main():
    """Use for testing purposes only.

    This function carries out a similar job to the Telegram Bot but in a
    simplyfied way
    """
    vid = Video('https://framex-dev.wadrid.net/api/video/'\
                'Falcon%20Heavy%20Test%20Flight%20(Hosted%20Webcast)-'\
                'wbSwFU6tY1c')

    while vid.can_bisect():
        index = vid.bisect_frame()
        question = '{}  Did the rocket launch yet?   (Y/n)'.format(index)
        answer = input(question)
        if answer.lower() in ['', 'y']:
            vid.remove('gte')
        elif answer.lower() == 'n':
            vid.remove('lt')
        else:
            print('That is not a valid answer')
    print(vid.bisect_frame())


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
