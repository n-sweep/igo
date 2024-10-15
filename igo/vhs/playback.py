import json
from time import sleep


def main():
    with open('/tmp/68039187.json', 'r') as f:
        data = json.loads(f.read())

    for frame in data['turns']:
        print(frame)
        sleep(data['speed'])


if __name__ == "__main__":
    main()
