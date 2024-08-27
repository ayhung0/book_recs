# book_recs
This project is a collaborative filtering-based book recommendation system built using pandas and Streamlit. The application allows users to input their book ratings and receive personalized book recommendations.

## Features
User Ratings Input: Users can input book titles along with their ratings.

Collaborative Filtering: The system uses collaborative filtering to compare the user's ratings with those of other users to find similar preferences.

Personalized Recommendations: Based on the calculated similarities, the system provides personalized book recommendations with predicted ratings.

## How It Works
User Input: Enter the book titles you’ve read along with your ratings in the provided text area. Each entry should be on a new line in the format: Book Title Rating (e.g., Frankenstein 4).

To test it out, you may copy and paste this example:

> The Bluest Eye 5
> 
> Frankenstein 3
>
> The Picture of Dorian Gray 5
>
> Persepolis: The Story of a Childhood 4
>
> Passing 5
>
> The Awakening and Selected Short Stories 3
>
> King Lear 4
>
> The Metamorphosis 4
>
> The Great Gatsby 4
>
> The Crucible 3
>
> Macbeth 4
>
> The Idiot 3
>
> One Flew Over the Cuckoo's Nest 3
>
> A Wild Sheep Chase 4
>
> Colorless Tsukuru Tazaki And His Years Of Pilgrimage 4
>
> Kafka on the Shore 5
>
> Dance Dance Dance (The Rat, #4) 5
>
> Norwegian Wood 4
>
> White Nights 2
>
> To Kill a Mockingbird 5
>
> Brave New World 4
>
> The Stranger 5
>
> In the Penal Colony 4
>
> One Hundred Years of Solitude 4
>
> Play It as It Lays 5
>
> The Catcher in the Rye 4

Submit: Once you’ve entered at least 10 book ratings, click the "Generate!" button.

Processing: The system will process your ratings, compare them with other users, and generate a user-item interaction matrix.

Recommendations: The system will provide a list of top book recommendations based on your input.

## Installation
Clone the repository:
```
git clone https://github.com/ayhung0/book_recs.git
```

Navigate to the project directory:
```
cd book_recs
```

Install the required Python packages:
```
pip install -r requirements.txt
```

Run the Streamlit app:
```
streamlit run book_recs.py
```

## Project Structure
book_recs.py: Main Streamlit application file.

books.csv: Dataset containing book details such as book_id, title, and authors.

ratings.csv: Dataset containing user ratings with user_id, book_id, and rating.

requirements.txt: List of Python packages required to run the project.


Books and ratings datasets taken from this repo: https://github.com/zygmuntz/goodbooks-10k
