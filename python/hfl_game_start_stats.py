import requests
from collections import defaultdict

from bs4 import BeautifulSoup


def scrape_html(url):
    """Scrape HTML"""
    response = requests.get(url)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup


def generate_time_stats(soup):
    """Parse stats"""

    days_to_ints_dict = {
        'субота': 6,
        'неділя': 7,
    }

    def empty_days():
        return {i: [] for i in range(6, 8)}

    time_stats = defaultdict(empty_days)
    matches = soup.find_all('li', class_='schedule__matches-item')
    for match in matches:
        day_block = match.parent.parent.find(class_='schedule__head')
        day = day_block.get_text(strip=True).split(',')[1].strip()
        if day in days_to_ints_dict.keys():
            day_of_the_week = days_to_ints_dict[day]
            team_home = match.find(class_='schedule__team-name--left').get_text(strip=True)
            team_away = match.find(class_='schedule__team-name--right').get_text(strip=True)
            time = match.find(class_='schedule__time').get_text(strip=True)
            if time != '0:00':
                for team in [team_home, team_away]:
                    time_stats[team][day_of_the_week].append(time)
    return time_stats


def print_team_header(team, symbol='-'):
    max_stars = 60
    stars = int((max_stars - 2 - len(team))/2)
    first_half = symbol * stars + ' '
    second_half = ' ' + symbol * stars
    result = f'{first_half}{team}{second_half}'
    stars_to_end = max_stars - len(result)
    print(result + symbol * stars_to_end)


def print_days_stats(day_stats):
    print(f'СБ:{len(day_stats[6])} НД:{len(day_stats[7])}')


def calculate_frequencies(day_stats):
    hours_frequency = {i:0 for i in range(8, 21)}
    hours = [int(time.split(':')[0]) for time in day_stats[6] + day_stats[7]]
    for time in hours:
        hours_frequency[time] += 1
    return hours_frequency


def print_lines_by_hours(hours_frequency):
     for hour, freq in hours_frequency.items():
        padding_from = '0' * (2 - len(str(hour)))
        padding_to = '0' * (2 - len(str(hour + 1)))
        print(f'{padding_from}{hour}:00-{padding_to}{hour+1}:00 ' + '|' * freq)


def print_frequency_stats(time_stats):
    for team, day_stats in time_stats.items():
        print_team_header(team)
        print_days_stats(day_stats)
        print_lines_by_hours(calculate_frequencies(day_stats))


def main():
    soup = scrape_html('https://diamondliga.join.football/tournament/1015193/calendar?round_id=1026185')
    time_stats = generate_time_stats(soup)
    print_frequency_stats(time_stats)


if __name__ == '__main__':
    main()
    
