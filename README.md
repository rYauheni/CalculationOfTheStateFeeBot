# CalculationOfTheStateDutyBot

[**CalculationOfTheStateDutyBot**](https://t.me/CotSD_bot) is a Telegram bot. This bot allows you to calculate the state duty for the courts of
the Republic of Belarus,
as well as the arbitration fee for the International Arbitration Court at the BelCCI, taking into account the following:

- for all courts;
- for all types of processes;
- for all judicial instances;
- for all types of legal proceedings;
- for all kinds of claims.

The procedure for calculating the state duty (arbitration fee) is determined based on the
Tax Code of the Republic of Belarus, the Civil Procedure Code of the Republic of Belarus,
the Economic Procedure Code of the Republic of Belarus,
the regulations of the International Arbitration Court at the BelCCI,
the resolution of the Council of Ministers of the Republic of Belarus
on the approval of establishing the size of the base value.

You can try the application [here](https://t.me/CotSD_bot).
___

## Technologies

[![Python](https://img.shields.io/badge/Python-3.10-%23FFD040?logo=python&logoColor=white&labelColor=%23376E9D)](https://www.python.org/downloads/release/python-31012/)
[![TelegramAPI](https://img.shields.io/badge/TelegramAPI-%23293133)](https://core.telegram.org/bots/api)

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-%232F6792?logoColor=white&labelColor=%23293133&logo=postgresql)](https://www.postgresql.org/)
[![SQLite](https://img.shields.io/badge/SQLite-%23003156?logoColor=white&labelColor=%23293133&logo=sqlite)](https://www.sqlite.org/)

[![Docker](https://img.shields.io/badge/Docker-%232496ED?logo=docker&logoColor=white&labelColor=%23293133)](https://www.docker.com/)

[![UnitTest](https://img.shields.io/badge/UnitTest-%23293133)](https://docs.python.org/3/library/unittest.html)

[![GitHub](https://img.shields.io/badge/GitHub-%23000000?logoColor=white&labelColor=%23293133&logo=github)](https://github.com/)

___

## Installation

Run the following commands to bootstrap your environment.

For Windows:

```commandline
git clone https://github.com/rYauheni/CalculationOfTheStateFeeBot.git

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

copy .env.template .env

```

For Linux:

```commandline
git clone https://github.com/rYauheni/CalculationOfTheStateFeeBot.git

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.template .env
```

___

## QuickStart for development

1. Determine the value of environment variables in the file `.env`


2. Set in `settings/settings.py`:

   ```python
   PRODUCTION = False
   ```


3. Run the app locally:

   for Windows:

   ```commandline
   python CalculatorOfTheStateDuty_BOT.py
   ```

   for Linux:

   ```commandline
   python3 CalculatorOfTheStateDuty_BOT.py
   ```


4. Run unittests:

   for Windows:
   ```commandline
   python -m unittest discover -s tests -p "test_*.py" -v
   ```

   for Linux:
   ```commandline
   python3 -m unittest discover -s tests -p "test_*.py" -v
   ```

___

## Launch for production

1. Determine the value of environment variables in the file `.env`


2. Set in `settings/settings.py`:

   ```python
   PRODUCTION = True
   ```


3. Run docker container with command:

    ```commandline
    docker-compose up
    ```

 ___

## Contributing

Bug reports and/or pull requests are welcome
___

## License

The app is dedicated to the public domain under the CC0 license
___

## Disclaimer

The calculation of the state duty (arbitration fee) is approximate.
The calculation made by this bot CAN NOT be used as evidence in court and DOES NOT HAVE legal force.