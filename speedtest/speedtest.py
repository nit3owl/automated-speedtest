import subprocess
import json
import csv
import datetime
import smtplib
from email.message import EmailMessage


def run_speedtest():
    print('Starting speedtest...')
    command = ['speedtest-cli', '--json']
    output, error = subprocess.Popen(command, universal_newlines=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE).communicate()

    if error:
        print('An error occurred: {}'.format(error))
        exit(1)

    print('Speedtest complete.\n')

    return output


def test_data():
    return '{"download": 108125551.66701199, "upload": 3423090.9812021744, "ping": 31.563, "server": {"url": ' \
           '"http://seattle.speedtest.centurylink.net:8080/speedtest/upload.php", "lat": "47.6062", ' \
           '"lon": "-122.3321", "name": "Seattle, WA", "country": "United States", "cc": "US", "sponsor": ' \
           '"CenturyLink", "id": "8864", "url2": "http://tuk-speedtest-01.inet.qwest.net/speedtest/upload.php", ' \
           '"host": "seattle.speedtest.centurylink.net:8080", "d": 32.40888418375512, "latency": 31.563}, ' \
           '"timestamp": "2020-01-20T05:54:54.162753Z", "bytes_sent": 5242880, "bytes_received": 270509185, ' \
           '"share": null, "client": {"ip": "66.235.10.132", "lat": "47.725", "lon": "-121.9369", "isp": "Wave ' \
           'Broadband", "isprating": "3.7", "rating": "0", "ispdlavg": "0", "ispulavg": "0", "loggedin": "0", ' \
           '"country": "US"}} '


def process_results(raw_result):
    print('Parsing results...')

    result = json.loads(raw_result)
    timestamp = result['timestamp']
    download = result['download']
    upload = result['upload']
    ping = result['ping']

    record_test(timestamp, download, upload, ping)


def read_tests(filename):
    rows = []

    # reading csv file
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows.append(row)

    print(f'Total number of test results: {csvreader.line_num}')

    for row in rows:
        # parsing each column of a row
        for col in row:
            print("%10s" % col),
        print('\n')


def record_test(timestamp, download, upload, ping):
    print('Logging test...')

    date = datetime.datetime.today().strftime('%Y-%m-%d')
    filename = f'{date}.csv'

    row = [timestamp, download, upload, ping]
    print(f'Logging to file: {filename} test: {row}')

    with open(filename, 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(row)

    print('Test logged.\n')


def email_results(sender, recipient, report):
    print('Emailing report...')

    filetype_index = report.find('.')
    test_date = report[0: filetype_index]

    with open(report) as body:
        msg = EmailMessage()
        msg.set_content(body.read())

    subject = f'Speedtest report for {test_date}'
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    # TODO send email once SMTP server set up
    # Send the message via local SMTP server.
    # s = smtplib.SMTP('localhost')
    # s.send_message(msg)
    # s.quit()

    print(f'Subject: {subject}\nSender: {sender}\nRecipient: {recipient}\nBody: {msg.get_content()}')
    print('Email sent.\n')


def main():
    raw_result = run_speedtest()
    process_results(raw_result)

    # TODO only run every 24 hours (or as scheduled)
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    report = f'{today}.csv'
    email_results('foo@example.com', 'boo@example.com', report)


main()
