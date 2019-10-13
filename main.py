import os
import csv
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

CSV_FILENAME = "data.csv"
CSV_FIELDS = ['event_type', 'user_id', 'timestamp']

def init_csv():
    "Init csv file if it doesn't exist."
    if not os.path.isfile(CSV_FILENAME):
        with open(CSV_FILENAME, 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(CSV_FIELDS)

def get_long_poll():
    "Get a long poll interface."
    vk_session = vk_api.VkApi(token=os.getenv('ACCESS_TOKEN'))
    return VkLongPoll(vk_session)

def main():
    init_csv()
    long_poll = get_long_poll()
    for event in long_poll.listen():
        if event.type == VkEventType.USER_OFFLINE or event.type == VkEventType.USER_ONLINE:
            with open(CSV_FILENAME, 'a') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([0 if event.type.value == 9 else 1,
                                     event.user_id,
                                     event.timestamp])

if __name__ == '__main__':
    main()
