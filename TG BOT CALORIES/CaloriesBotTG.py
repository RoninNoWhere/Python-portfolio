import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import sqlite3
from datetime import datetime
import pandas as pd  # for calories.xls

# Logging configuration
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load product data from CSV
def load_product_data():
    df = pd.read_csv('calories.csv', header=None)  # Reading CSV
    df.columns = ['Category', 'Product', 'Serving', 'Calories', 'Energy']  # Column names
    df['Calories'] = df['Calories'].str.extract('(\d+)').astype(int)  # Calories information
    return df

# SQLite database connection
def init_db():
    conn = sqlite3.connect('calorie_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calories (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            date TEXT,
            product TEXT,
            weight INTEGER,  -- Добавьте этот столбец
            calories INTEGER
        )
    ''')
    conn.commit()
    conn.close()
    

product_data = load_product_data()  # download data when programm starts

# Function to create the main menu
def get_main_menu_keyboard():
    keyboard = [
        ['Add Product'],
        ['View Report'],
        ['Calorie History'],
    ]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)

# Function to create a keyboard for adding products
def get_add_product_keyboard():
    return ReplyKeyboardMarkup([['Return to Menu']], one_time_keyboard=True, resize_keyboard=True)

# Handler for the /start command
async def start(update: Update, context) -> None:
    reply_markup = get_main_menu_keyboard()
    await update.message.reply_text("Hello! I am a calorie tracking bot. To start, choose an option:", reply_markup=reply_markup)

# Handler for the /null command
async def reset(update: Update, context) -> None:
    context.user_data.clear()  # Reset all user data
    await start(update, context)

# Handling button presses
async def button_click(update: Update, context) -> None:
    query = update.message.text
    product_data = load_product_data()  # Load product data from the CSV file

    if query == 'Add Product':
        await update.message.reply_text("To track calories, enter the product name and amount in grams (e.g., Apple 100):")
        context.user_data['adding_product'] = True
        context.user_data['add_keyboard'] = get_add_product_keyboard()  # Get keyboard for adding product
        await update.message.reply_text("Enter the product name and amount in grams:", reply_markup=context.user_data['add_keyboard'])

    elif context.user_data.get('adding_product'):
        if query == 'Return to Menu':
            context.user_data['adding_product'] = False  # Reset the adding state
            await start(update, context)  # Return to the main menu
            return

        try:
            product_name, amount = update.message.text.rsplit(' ', 1)  # Split the text into product and amount
            amount = int(amount)  # Convert the amount to an integer
            user_id = update.message.from_user.id
            date = datetime.now().strftime("%Y-%m-%d")

            # Convert user input to lower case for comparison
            product_name_lower = product_name.lower()  

            # Get calories from the database, converting product names to lower case for comparison
            calories_per_100g = product_data.loc[product_data['Product'].str.lower() == product_name_lower, 'Calories']

            if not calories_per_100g.empty:
                calories = int(calories_per_100g.values[0] * (amount / 100))  # Calculate calories
                # Write to the database
                conn = sqlite3.connect('calorie_tracker.db')
                cursor = conn.cursor()
                cursor.execute('INSERT INTO calories (user_id, date, product, calories) VALUES (?, ?, ?, ?)',
                               (user_id, date, product_name, calories))
                conn.commit()
                conn.close()

                await update.message.reply_text(f"{calories} calories added for {product_name}.")
                await update.message.reply_text("You can add another product or press 'Return to Menu'.", reply_markup=context.user_data['add_keyboard'])
            else:
                await update.message.reply_text("Product not found in the database. Please try again.")

        except (ValueError, IndexError):
            await update.message.reply_text("Error. Use the format: product name amount in grams.")


    elif query == 'View Report':
        logger.info("View Report button pressed") 
        await send_report(update)


    elif query == 'Calorie History':
        await send_history(update)

    elif context.user_data.get('adding_product') and query == 'Return to Menu':
        context.user_data['adding_product'] = False  # Reset the adding state
        await start(update, context)

    # Handling product input
    elif context.user_data.get('adding_product'):
        try:
            product, weight = update.message.text.rsplit(' ', 1)  # Split text into product and weight
            weight = int(weight)  # Convert weight to an integer
            user_id = update.message.from_user.id
            date = datetime.now().strftime("%Y-%m-%d")

            # Searching products in database
            product_info = product_data[product_data['Product'].str.lower() == product.lower()]

            if not product_info.empty:
                calories_per_100g = product_info['Calories_per_100g'].values[0]
                total_calories = (calories_per_100g * weight) / 100

                # Adds values to database
                conn = sqlite3.connect('calorie_tracker.db')
                cursor = conn.cursor()
                cursor.execute('INSERT INTO calories (user_id, date, product, weight, calories) VALUES (?, ?, ?, ?, ?)',
                               (user_id, date, product, weight, total_calories))
                conn.commit()
                conn.close()

                await update.message.reply_text(f"{weight}g of {product} contains {total_calories} calories.")
                await update.message.reply_text("You can add another product or press 'Return to Menu'.")

            else:
                await update.message.reply_text("Product not found. Please try again.")

        except (ValueError, IndexError):
            await update.message.reply_text("Error. Use the format: product name weight")

# Sending the report
async def send_report(update):
    user_id = update.message.from_user.id
    date = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect('calorie_tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT product, weight, SUM(calories) FROM calories WHERE user_id = ? AND date = ? GROUP BY product, weight', (user_id, date))
    rows = cursor.fetchall()
    conn.close()

    logger.info(f"Fetched rows for report: {rows}")  # Логируем извлеченные строки

    if rows:
        report_message = "Your report for today:\n"
        total_calories = 0
        for row in rows:
            product, weight, cal = row
            report_message += f"{weight}g of {product}: {cal} calories\n"
            total_calories += cal
        report_message += f"Total: {total_calories} calories"
    else:
        report_message = "You haven't added any calories today."

    await update.message.reply_text(report_message)

# Sending the calorie history
async def send_history(update):
    user_id = update.message.from_user.id
    conn = sqlite3.connect('calorie_tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT date, SUM(calories) FROM calories WHERE user_id = ? GROUP BY date', (user_id,))
    rows = cursor.fetchall()
    conn.close()

    if rows:
        history_message = "Your calorie history:\n"
        for row in rows:
            date, total_calories = row
            history_message += f"{date}: {total_calories} calories\n"
    else:
        history_message = "No calorie history."

    await update.message.reply_text(history_message)

# Main function
def main():
    init_db()

    application = Application.builder().token("7743409818:AAFcaP1uPv9qlZ-_UdzNqrnpb0qHr-sflt8").build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("null", reset))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_click))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
