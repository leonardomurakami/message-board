#!/usr/bin/env python3
import random
import sys
import time
import requests

REAL_BOARDS = [
    {"short_name": "tech", "name": "Technology", "description": "Computers and programming"},
    {"short_name": "art", "name": "Art", "description": "Digital and traditional artwork"},
    {"short_name": "lit", "name": "Literature", "description": "Books and writing"},
    {"short_name": "mus", "name": "Music", "description": "Music recommendations"},
    {"short_name": "mov", "name": "Movies", "description": "Film and cinema"},
    {"short_name": "gam", "name": "Games", "description": "Video games"},
    {"short_name": "sci", "name": "Science", "description": "Science and math"},
    {"short_name": "his", "name": "History", "description": "Historical events"},
    {"short_name": "fit", "name": "Fitness", "description": "Health and exercise"},
    {"short_name": "ck", "name": "Cooking", "description": "Food and cooking"},
]

ADJECTIVES = ["amazing", "terrible", "beautiful", "ugly", "brilliant", "stupid", "fantastic", "awful", "wonderful", "horrible", "excellent", "bad", "good", "great", "small", "large", "tiny", "huge", "fast", "slow", "quick", "old", "new", "ancient", "modern", "fresh", "stale", "bright", "dark", "light", "heavy", "soft", "hard", "smooth", "rough", "sharp", "dull", "hot", "cold", "warm", "cool"]
NOUNS = ["computer", "phone", "book", "movie", "song", "game", "car", "house", "tree", "dog", "cat", "bird", "fish", "person", "place", "thing", "idea", "thought", "dream", "nightmare", "story", "joke", "secret", "truth", "lie", "question", "answer", "problem", "solution", "mistake", "success", "failure", "victory", "defeat", "beginning", "end", "middle", "front", "back", "top", "bottom", "side", "center", "edge", "corner", "world", "universe", "galaxy", "planet"]
VERBS = ["think", "feel", "see", "hear", "say", "do", "make", "take", "get", "give", "know", "want", "like", "love", "hate", "need", "try", "find", "lose", "win", "run", "walk", "talk", "listen", "look", "watch", "read", "write", "draw", "paint", "sing", "dance", "play", "work", "sleep", "eat", "drink", "buy", "sell", "create", "destroy", "build", "break", "fix", "help", "hurt"]

TOPIC_WORDS = {
    "tech": ["python", "javascript", "linux", "windows", "mac", "ai", "coding", "bug", "feature", "server", "database", "api", "framework", "library"],
    "art": ["drawing", "painting", "digital", "sketch", "color", "canvas", "brush", "pixel", "design", "creative", "sculpture", "photography"],
    "lit": ["novel", "poetry", "author", "chapter", "plot", "character", "writing", "reading", "genre", "classic", "fiction", "fantasy"],
    "mus": ["album", "concert", "guitar", "piano", "lyrics", "melody", "rhythm", "band", "artist", "genre", "rock", "jazz", "classical"],
    "mov": ["film", "director", "actor", "cinema", "scene", "plot", "trailer", "review", "genre", "sequel", "remake", "documentary"],
    "gam": ["rpg", "fps", "strategy", "indie", "multiplayer", "level", "boss", "quest", "achievement", "stream", "esports", "modding"],
    "sci": ["theory", "experiment", "research", "physics", "chemistry", "biology", "space", "atom", "molecule", "evolution", "quantum"],
    "his": ["ancient", "medieval", "war", "empire", "revolution", "century", "historical", "archive", "era", "civilization", "dynasty"],
    "fit": ["workout", "gym", "running", "diet", "muscle", "cardio", "training", "exercise", "health", "protein", "yoga", "nutrition"],
    "ck": ["recipe", "ingredient", "kitchen", "cooking", "baking", "dish", "flavor", "spice", "meal", "chef", "cuisine", "dessert"],
}

def generate_random_sentence(min_words=5, max_words=20):
    num_words = random.randint(min_words, max_words)
    words = []
    for i in range(num_words):
        word = random.choice(ADJECTIVES + NOUNS + VERBS)
        words.append(word.capitalize() if i == 0 else word)
    return " ".join(words) + "."

def generate_random_paragraph(min_sentences=2, max_sentences=8):
    return " ".join([generate_random_sentence() for _ in range(random.randint(min_sentences, max_sentences))])

def generate_thread_title(board_short_name):
    topic_words = TOPIC_WORDS.get(board_short_name, [])
    templates = [
        "Best way to learn {topic}?", "What do you think about {adj} {topic}?", "{topic} recommendations needed",
        "How do I get started with {topic}?", "{adj} {topic} discussion", "Share your {topic} experiences",
        "Is {topic} worth it?", "{topic} vs {topic2} - which is better?", "Help with {topic}",
        "Just discovered {adj} {topic}", "Why is {topic} so {adj}?", "Favorite {topic}?",
        "Thoughts on {adj} {topic}?", "{topic} advice needed", "Can someone explain {topic}?",
        "The future of {topic}", "{topic} problems", "My {topic} journey", "{topic} tips and tricks", "Weekly {topic} thread",
    ]
    word1 = random.choice(topic_words) if topic_words else random.choice(NOUNS)
    word2 = random.choice(topic_words) if topic_words and len(topic_words) > 1 else random.choice(NOUNS)
    adj = random.choice(ADJECTIVES)
    return random.choice(templates).format(topic=word1, topic2=word2, adj=adj)[:100]

def generate_post_content(board_short_name):
    content = generate_random_paragraph(3, 12)
    topic_words = TOPIC_WORDS.get(board_short_name, [])
    if topic_words and random.random() > 0.5:
        topic_word = random.choice(topic_words)
        intro = random.choice([f"Regarding {topic_word}: ", f"I think {topic_word} is ", f"{topic_word.capitalize()} matters because ", f"When it comes to {topic_word}, ", ""])
        if intro:
            content = intro + content[0].lower() + content[1:]
    return content

def create_boards(base_url):
    print("Creating boards...")
    boards = []
    for board_data in REAL_BOARDS:
        try:
            r = requests.post(f"{base_url}/api/boards/", json=board_data)
            if r.status_code == 200:
                boards.append(r.json())
                print(f"  + /{board_data['short_name']}/")
        except Exception as e:
            print(f"  ERR {board_data['short_name']}: {e}")
    return boards

def create_thread(base_url, board_id, board_short_name):
    try:
        r = requests.post(
            f"{base_url}/api/threads/?board_id={board_id}",
            json={"title": generate_thread_title(board_short_name), "content": generate_post_content(board_short_name), "owner": "mock"},
        )
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

def create_post(base_url, thread_id, board_short_name):
    try:
        r = requests.post(f"{base_url}/pages/threads/{thread_id}/posts", data={"content": generate_post_content(board_short_name)}, cookies={"mb_user": "mock"})
        return r.status_code == 200
    except Exception:
        return False

def main():
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8001"
    num_threads = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    avg_posts = int(sys.argv[3]) if len(sys.argv) > 3 else 10

    boards = create_boards(base_url)
    if not boards:
        print("No boards. Exiting.")
        sys.exit(1)

    print(f"Creating {num_threads} threads...")
    total_posts = 0
    start = time.time()

    for i in range(num_threads):
        board = random.choice(boards)
        thread = create_thread(base_url, board["id"], board["short_name"])
        if thread:
            num_posts = random.randint(avg_posts // 2, avg_posts * 2)
            for _ in range(num_posts):
                if create_post(base_url, thread["id"], board["short_name"]):
                    total_posts += 1
            if (i+1) % 10 == 0:
                print(f"  Progress: {i+1}/{num_threads} ({total_posts} posts)")
        if i % 5 == 0:
            time.sleep(0.05)

    print(f"Done in {time.time() - start:.1f}s. Threads: {num_threads}, Posts: {total_posts}")

if __name__ == "__main__":
    main()
