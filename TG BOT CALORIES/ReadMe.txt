his is a Telegram bot that counts calories.

How does it work?
The user types anything to the bot to start. The bot responds with:
"Hello! I am a calorie tracking bot. To start, choose an option:"

There are visual buttons you can click (optional for users): Add Product, View Report, and Calorie History.

For Add Product, the bot prompts:
"To track calories, enter the product name and amount in grams (e.g., Apple 100). Enter the product name and amount in grams:"
You can add several products using the format [Name] [grams]. The bot checks the database of products for their calories per 100 grams, calculates the total, and saves it as data.
Here’s an example:

Some One:
banana 100
CaloriesBot:
89 calories added for banana.
CaloriesBot:
"You can add another product or press 'Return to Menu'."
Some One:
Apple 100
CaloriesBot:
52 calories added for Apple.
CaloriesBot:
"You can add another product or press 'Return to Menu'."
Some One:
Milk 100
CaloriesBot:
61 calories added for Milk.
CaloriesBot:
"You can add another product or press 'Return to Menu'."

Then, you can view your daily report using the View Report option. Here is the output:
"Your report for today:"

    Apple: 52 calories
    Milk: 61 calories
    Banana: 89 calories
    Total: 202 calories

You can also check data for past days using the Calorie History option:
"Your calorie history:"

    2024-10-08: 202 calories

