# Auction Website - CS50 Project

This project is an e-commerce auction website, designed as part of the CS50 Web Programming with Python and JavaScript course. The website allows users to create auction listings, place bids, comment on listings, and manage their own watchlist. The purpose of this project is purely educational, and the design and functionality have not been optimized for real-world usage.

## Features

- **User Registration & Authentication:**
  - Users can register, log in, and log out.
  - User authentication is required for most actions (e.g., placing bids, adding to the watchlist, commenting).

- **Auction Listings:**
  - Users can create auction listings by specifying a title, description, starting bid, category, and an optional image.
  - Listings are displayed on the homepage as "active auctions."

- **Bidding:**
  - Authenticated users can place bids on auction listings.
  - The bid must be higher than the current price or starting bid.
  - Users who create the listing can close the auction, marking the highest bidder as the winner.

- **Watchlist:**
  - Users can add or remove items from their watchlist.
  - A separate page displays all the listings that the user has added to their watchlist.

- **Categories:**
  - Users can browse active listings by category.
  - Each category displays all the active auction listings under that category.

- **Comments:**
  - Authenticated users can add comments to auction listings.
  - All comments on a listing are visible to other users.


## How to Run the Project

1. **Clone the repository:**
   ```bash
   git clone <repository-link>
   cd <repository-folder>

2. **Install dependencies:**
   Ensure you have pip installed and install the required dependencies:
   ```bash
    pip install -r requirements.txt

3. **Run database migrations:**
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate

4. **Create a superuser (optional, for accessing Django admin panel):**
   ```bash
   python3 manage.py createsuperuser

5. **Run the development server:**
   ```bash
   python3 manage.py runserver

6. **Access the site:**
   Visit http://127.0.0.1:8000/ in your browser to use the auction site.

## Demo Video

A demo of this project is available on YouTube:

YouTube Demo Link

## Notes

- **Educational Purpose:**
This project was built solely for educational purposes as part of CS50's Web Programming with Python and JavaScript course. The design, functionality, and user experience have not been optimized for real-world use.

- **Limitations:**
The application is intentionally simplistic and does not include some advanced features that might be found in production-level auction websites (e.g., real-time bidding, payment systems, etc.).



