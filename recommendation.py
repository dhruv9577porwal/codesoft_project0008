import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Movie data
movies = {
    'title': [
        'The Matrix', 'John Wick', 'Inception', 'The Dark Knight',
        'Interstellar', 'Avengers: Endgame', 'The Prestige', 'Tenet',
        'Memento', 'Dunkirk', '3 Idiots', 'PK', 'Dangal', 'Chak De! India',
        'Zindagi Na Milegi Dobara', 'Taare Zameen Par', 'Barfi!', 'Queen',
        'Lagaan', 'Swades'
    ],
    'description': [
        'A computer hacker learns about the true nature of reality and his role in the war against its controllers.',
        'An ex-hitman comes out of retirement to track down the gangsters that killed his dog.',
        'A thief steals corporate secrets through dream-sharing technology.',
        'Batman faces the Joker in a battle for Gotham\'s soul.',
        'Explorers travel through a wormhole in space to save humanity.',
        'The Avengers assemble once more to reverse Thanos\' snap and restore balance.',
        'Two magicians engage in a dangerous rivalry full of tricks.',
        'A secret agent manipulates time to prevent global disaster.',
        'A man with short-term memory loss uses tattoos to hunt his wife\'s killer.',
        'Allied soldiers are surrounded during WWII evacuation.',
        'Three engineering students learn life lessons while dealing with academic pressure.',
        'An alien lands on Earth and questions religious dogma in India.',
        'A former wrestler trains his daughters to become world-class wrestlers.',
        'A hockey coach trains a women\'s team to prove his loyalty to the nation.',
        'Three friends take a road trip across Spain discovering themselves.',
        'A teacher helps a dyslexic child discover his potential through art.',
        'A mute man with autism falls in love in a bittersweet journey.',
        'A woman rediscovers herself on a solo honeymoon trip.',
        'A small village team takes on the British in a game of cricket.',
        'A NASA scientist returns to rural India to bring development.'
    ]
}

# Create DataFrame
df = pd.DataFrame(movies)

# Vectorization and similarity calculation
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['description'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def get_recommendations(title, top_n=3):
    """Get movie recommendations based on cosine similarity."""
    if title not in df['title'].values:
        return []
    idx = df[df['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n + 1]
    movie_indices = [i[0] for i in sim_scores]
    return df.iloc[movie_indices][['title', 'description']].values.tolist()

# GUI setup
root = tk.Tk()
root.title("🌟 Movie Recommendation System")
root.geometry("800x600")
root.configure(bg="#2c3e50")

# Fonts
TITLE_FONT = ('Arial', 24, 'bold')
LABEL_FONT = ('Arial', 14)
RESULT_FONT = ('Arial', 12)

# Title label
title_label = tk.Label(root, text="🎬 Movie Recommendation System", font=TITLE_FONT, bg="#2c3e50", fg="#ecf0f1")
title_label.pack(pady=20)

# Dropdown for movie selection
dropdown_label = tk.Label(root, text="🎯 Select a movie you like:", font=LABEL_FONT, bg="#2c3e50", fg="#ecf0f1")
dropdown_label.pack()

selected_movie = tk.StringVar()
movie_dropdown = ttk.Combobox(root, textvariable=selected_movie, values=df['title'].tolist(), state="readonly", width=60)
movie_dropdown.pack(pady=10)
movie_dropdown.current(0)

# Result frame
result_frame = tk.Frame(root, bg="#34495e", bd=4, relief="ridge")
result_frame.pack(pady=25, padx=30, fill="both", expand=True)

result_title = tk.Label(result_frame, text="🍿 Top 3 Recommendations", font=('Arial', 16, 'bold'), bg="#34495e", fg="#ecf0f1")
result_title.pack(pady=(15, 10))

result_label = tk.Text(result_frame, wrap='word', font=RESULT_FONT, bg="#ecf0f1", fg="#2c3e50", height=15, width=70)
result_label.pack(padx=10, pady=5)

def show_recommendations():
    """Display movie recommendations."""
    movie = selected_movie.get()
    recommendations = get_recommendations(movie)
    result_label.delete("1.0", tk.END)
    if recommendations:
        for i, (title, desc) in enumerate(recommendations, 1):
            result_label.insert(tk.END, f"⭐ {i}. {title}\n📖 {desc}\n\n")
    else:
        messagebox.showinfo("⚠️ Not Found", "Movie not found in database.")

# Button frame
button_frame = tk.Frame(root, bg="#2c3e50")
button_frame.pack()

recommend_button = ttk.Button(button_frame, text="🎥 Recommend Movies", command=show_recommendations)
recommend_button.grid(row=0, column=0, padx=15, pady=10)

def reset():
    """Reset the dropdown and results."""
    movie_dropdown.current(0)
    result_label.delete("1.0", tk.END)

reset_button = ttk.Button(button_frame, text="🔄 Reset", command=reset)
reset_button.grid(row=0, column=1, padx=15, pady=10)

# Run the application
root.mainloop()
