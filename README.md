# 1-2-3 Point Play!
### ***Purpose***

My immediate family loves to do NFL pick'ems, and we like to make it a competition. 

We would pick three games based on the spread of the game, and we would assign the games we picked a point value from 1 to 3. The family member with the most points at the end of the season wins!

We used to write these picks down on paper - not inefficient by any means, but when it comes to:
- **Tracking statistics** - most frequently picked team to cover the spread, amount of 1/2/3 point plays correct, percentage of correctness overall
- **Viewing historical metrics** - previous picks + their outcomes
- The process of having to walk to the living room/text a family member your picks for them to be written down on the "master paper"

You run into some manual processes that could be made, in a sense, *simpler*.

#
### ***So, I built an app that tackles these issues***

This app enables my family members to make picks from anywhere they want, at any time.

To accomplish this, I'm pulling data from The Odds API to get information about the current listing of games and their betting spreads. Two sets of buttons are displayed under each game:

1. Two betting spread options to pick from, and
2. Point values to assign that pick

Point totals are tallied automatically, and all results are stored in a database that enables the implementation statistic tracking and historical metrics, all handled by the application.

#
### ***Goals***

This application has went through a first round of testing on the "version/MLB-new" branch, where I asked my family members to:
- Follow the link and select their name on the front page.
- Select three games from a listing of MLB games based on the over/under line.
- Finalize their picks so that they're stored in the database.
- View the results of their picks by going to the "View This Week's Picks" button.

This first run-through was very successful! Future implementations include:
1. Creating a statistics page that shows the players % of successful picks + other important metrics (Streamlit visualizations will be very useful here)
2. Creating a history section that shows the player's results by week.
