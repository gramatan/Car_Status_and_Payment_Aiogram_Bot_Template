# Car Status and Payment Bot Template

This template provides a Telegram bot that allows users to check the status of their cars and make payments or refuse payment. It also includes features for moderators and administrators to manage car numbers, change statuses, and access payment information.

## Features

* Users can enter their car number and view its status.
* Users can choose to pay or refuse payment.
* Moderators can add car numbers to the database and change their statuses.* Administrators can view the entire car numbers database and access payment information.

## Requirements

* Python 3.7+
* aiogram: pip install aiogram
* asyncio: pip install asyncio
* SQLite3

## Setup

1. Clone this repository or copy the provided code.
2. Install the required dependencies.
3. Replace "BOT_TOKEN" with your bot's token obtained from the BotFather on Telegram.
4. Run the bot: python main.py

## Usage

* Users can send a message containing their car number to the bot.
* The bot will reply with the current status of the car and provide options to pay or refuse payment.
* Moderators can use the following commands:
  * /add_car_number <car_number> <status> to add a car number to the database.
  * /change_status <car_number> <new_status> to change the status of a car number in the database.
* Administrators can access the database and payment information directly through the SQLite3 database file.

## Customization

This bot template is easily customizable. You can modify the database schema, add more commands, or change the bot's responses as needed. If you encounter any issues or need assistance with customization, feel free to ask for help.