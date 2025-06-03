import streamlit as st
import requests
from camel_agent import Agent  

def get_multiple_books(book_name, max_results=5):
    url = f"https://www.googleapis.com/books/v1/volumes?q={book_name}&maxResults={max_results}"
    response = requests.get(url)
    books = []

    if response.status_code == 200:
        books_data = response.json()
        for item in books_data.get('items', []):
            volume_info = item.get('volumeInfo', {})
            books.append({
                "title": volume_info.get("title", "N/A"),
                "author": ', '.join(volume_info.get("authors", ["N/A"])),
                "release_date": volume_info.get("publishedDate", "N/A"),
                "genre": ', '.join(volume_info.get("categories", ["N/A"])),
                "description": volume_info.get("description", "No description available."),
                "moral": "Learn valuable lessons" if volume_info.get("description") else "No moral found",
                "image_url": volume_info.get("imageLinks", {}).get("thumbnail", "").replace("http://", "https://"),
                "preview_link": volume_info.get("previewLink", "#")
            })
    return books

agent = Agent()

# Configure page
st.set_page_config(
    page_title="Universal Pages | AI-Powered Book Discovery", 
    page_icon="📚", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Optimized CSS with reduced blur effects
st.markdown("""
<style>
:root {
    --primary: #7B2CBF;
    --primary-dark: #5A189A;
    --secondary: #00BBF9;
    --accent: #FF9E00;
    --dark: #0D0A1A;
    --darker: #070510;
    --light: #F8F9FA;
    --gray: #ADB5BD;
    --card-bg: #1A1429;
    --glass: rgba(123, 44, 191, 0.15);
    --success: #38B000;
    --gold: #FFD700;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap');

body, .stApp {
    background-color: var(--dark);
    color: var(--light);
    font-family: 'Montserrat', sans-serif;
    min-height: 100vh;
    background-image: 
        radial-gradient(circle at 10% 20%, rgba(123, 44, 191, 0.1) 0%, transparent 20%),
        radial-gradient(circle at 90% 80%, rgba(0, 187, 249, 0.1) 0%, transparent 20%);
}

/* Cosmic Header */
.header-container {
    background: linear-gradient(135deg, rgba(13, 10, 26, 0.9), rgba(26, 20, 41, 0.9));
    padding: 3rem 0;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.header-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        radial-gradient(circle at 20% 30%, rgba(123, 44, 191, 0.2) 0%, transparent 40%),
        radial-gradient(circle at 80% 70%, rgba(0, 187, 249, 0.2) 0%, transparent 40%);
    z-index: -1;
}

.header-content {
    text-align: center;
    position: relative;
    z-index: 2;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

.header-title {
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    letter-spacing: -1px;
    text-shadow: 0 2px 10px rgba(123, 44, 191, 0.3);
}

.header-subtitle {
    font-size: 1.2rem;
    color: var(--gray);
    font-weight: 300;
    max-width: 700px;
    margin: 0 auto;
    line-height: 1.6;
    opacity: 0.9;
}

/* Holographic Search Section */
.search-container {
    background: linear-gradient(135deg, rgba(26, 20, 41, 0.8), rgba(13, 10, 26, 0.9));
    padding: 2.5rem;
    border-radius: 24px;
    margin: 0 auto 4rem;
    max-width: 900px;
    box-shadow: 
        0 10px 30px rgba(0, 0, 0, 0.3),
        inset 0 0 20px rgba(123, 44, 191, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.05);
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.search-container::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(
        to bottom right,
        transparent 0%,
        transparent 45%,
        rgba(123, 44, 191, 0.05) 50%,
        transparent 55%,
        transparent 100%
    );
    transform: rotate(30deg);
    animation: shine 6s infinite linear;
    z-index: 1;
}

@keyframes shine {
    0% { transform: translateX(-100%) rotate(30deg); }
    100% { transform: translateX(100%) rotate(30deg); }
}

.search-container:hover {
    transform: translateY(-5px);
    box-shadow: 
        0 15px 40px rgba(0, 0, 0, 0.4),
        inset 0 0 30px rgba(123, 44, 191, 0.2);
}

.search-title {
    font-size: 1.5rem;
    color: var(--light);
    margin-bottom: 2rem;
    text-align: center;
    font-weight: 500;
    position: relative;
    z-index: 2;
}

.search-title::after {
    content: '';
    display: block;
    width: 80px;
    height: 3px;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    margin: 0.8rem auto 0;
    border-radius: 3px;
}

/* Cyberpunk Book Cards */
.book-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 2.5rem;
    margin: 3rem 0;
    position: relative;
    z-index: 2;
}

.book-card {
    background: linear-gradient(135deg, rgba(26, 20, 41, 0.8), rgba(13, 10, 26, 0.9));
    border-radius: 16px;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
    border: 1px solid rgba(255, 255, 255, 0.05);
    height: 100%;
    position: relative;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.book-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        135deg,
        rgba(123, 44, 191, 0.1) 0%,
        rgba(0, 187, 249, 0.05) 100%
    );
    opacity: 0;
    transition: opacity 0.3s ease;
    z-index: -1;
}

.book-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 
        0 15px 40px rgba(0, 0, 0, 0.3),
        0 0 30px rgba(123, 44, 191, 0.2);
}

.book-card:hover::before {
    opacity: 1;
}

/* Neon Book Cover */
.book-cover-container {
    height: 250px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.3);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    overflow: hidden;
    position: relative;
}

.book-cover-container::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.4s ease;
}

.book-card:hover .book-cover-container::after {
    transform: scaleX(1);
}

.book-cover {
    height: 100%;
    width: auto;
    max-width: 100%;
    object-fit: contain;
    padding: 20px;
    transition: all 0.4s ease;
    filter: drop-shadow(0 5px 15px rgba(0, 0, 0, 0.3));
}

.book-card:hover .book-cover {
    transform: scale(1.05) rotate(1deg);
}

.book-details {
    padding: 2rem;
}

.book-title {
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 0.6rem;
    color: white;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

.book-author {
    color: var(--secondary);
    font-size: 0.95rem;
    margin-bottom: 1rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.book-author::before {
    content: '✍️';
}

.book-meta {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.2rem;
    flex-wrap: wrap;
}

.meta-item {
    background: rgba(123, 44, 191, 0.2);
    padding: 0.4rem 1rem;
    border-radius: 20px;
    font-size: 0.85rem;
    color: var(--secondary);
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.meta-item:nth-child(1)::before {
    content: '📅';
}

.meta-item:nth-child(2)::before {
    content: '🏷️';
}

.book-description {
    color: var(--gray);
    font-size: 0.95rem;
    line-height: 1.7;
    margin-bottom: 1.8rem;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    opacity: 0.9;
}

.preview-btn {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    color: white;
    border: none;
    padding: 0.8rem 1.5rem;
    border-radius: 10px;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.8rem;
    font-weight: 600;
    box-shadow: 0 5px 15px rgba(123, 44, 191, 0.3);
    position: relative;
    overflow: hidden;
}

.preview-btn::after {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(
        to bottom right,
        transparent 0%,
        transparent 45%,
        rgba(255, 255, 255, 0.2) 50%,
        transparent 55%,
        transparent 100%
    );
    transform: rotate(30deg);
    animation: shine 3s infinite linear;
}

.preview-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(123, 44, 191, 0.4);
}

/* AI Hologram Panel */
.ai-recs {
    background: linear-gradient(135deg, rgba(26, 20, 41, 0.8), rgba(13, 10, 26, 0.9));
    padding: 2.5rem;
    border-radius: 24px;
    margin: 4rem 0;
    border: 1px solid rgba(255, 255, 255, 0.05);
    box-shadow: 
        0 10px 30px rgba(0, 0, 0, 0.3),
        inset 0 0 20px rgba(0, 187, 249, 0.1);
    position: relative;
    overflow: hidden;
}

.ai-recs::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        radial-gradient(circle at 20% 30%, rgba(0, 187, 249, 0.05) 0%, transparent 40%),
        radial-gradient(circle at 80% 70%, rgba(123, 44, 191, 0.05) 0%, transparent 40%);
    z-index: -1;
}

.ai-title {
    font-size: 1.6rem;
    font-weight: 700;
    margin-bottom: 2rem;
    color: white;
    display: flex;
    align-items: center;
    gap: 1rem;
    position: relative;
}

.ai-title::before {
    content: '🤖';
    font-size: 1.8rem;
}

.ai-title::after {
    content: '';
    display: block;
    width: 100px;
    height: 3px;
    background: linear-gradient(90deg, var(--secondary), var(--primary));
    position: absolute;
    bottom: -10px;
    left: 0;
    border-radius: 3px;
}

.rec-card {
    background: rgba(0, 187, 249, 0.05);
    padding: 2rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    border-left: 4px solid var(--secondary);
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
}

.rec-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        135deg,
        rgba(0, 187, 249, 0.05) 0%,
        transparent 100%
    );
    z-index: -1;
}

.rec-card:hover {
    transform: translateX(10px);
    background: rgba(0, 187, 249, 0.1);
    box-shadow: 0 5px 20px rgba(0, 187, 249, 0.1);
}

.rec-title {
    font-weight: 600;
    margin-bottom: 0.8rem;
    color: var(--secondary);
    font-size: 1.2rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.rec-content {
    color: var(--light);
    line-height: 1.7;
    font-size: 1rem;
    opacity: 0.9;
}

/* Cyber Orb Floating Button */
.fab {
    position: fixed;
    bottom: 3rem;
    right: 3rem;
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    width: 70px;
    height: 70px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 
        0 5px 20px rgba(123, 44, 191, 0.4),
        0 0 0 5px rgba(123, 44, 191, 0.2);
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
    z-index: 100;
    border: none;
    color: white;
    font-size: 1.8rem;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(123, 44, 191, 0.7); }
    70% { box-shadow: 0 0 0 15px rgba(123, 44, 191, 0); }
    100% { box-shadow: 0 0 0 0 rgba(123, 44, 191, 0); }
}

.fab:hover {
    transform: translateY(-5px) scale(1.1);
    box-shadow: 
        0 8px 25px rgba(123, 44, 191, 0.5),
        0 0 0 5px rgba(123, 44, 191, 0.3);
    animation: none;
}

/* Cyberpunk Footer */
.footer {
    text-align: center;
    padding: 3rem 0;
    margin-top: 4rem;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    color: var(--gray);
    font-size: 1rem;
    position: relative;
}

.footer::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--primary), var(--secondary), transparent);
}

.footer p:first-child {
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
    color: var(--light);
}

.footer p:last-child {
    font-size: 0.9rem;
    opacity: 0.7;
}

/* Streamlit Overrides - Cyberpunk Style */
.stTextInput>div>div>input {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: white !important;
    padding: 1rem 1.5rem !important;
    border-radius: 12px !important;
    font-size: 1.1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.2);
}

.stTextInput>div>div>input:focus {
    border-color: var(--secondary) !important;
    box-shadow: 
        0 0 0 2px rgba(0, 187, 249, 0.3),
        inset 0 0 10px rgba(0, 0, 0, 0.3) !important;
}

.stButton>button {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark)) !important;
    color: white !important;
    border: none !important;
    padding: 1rem 2rem !important;
    border-radius: 12px !important;
    font-size: 1.1rem !important;
    transition: all 0.3s ease !important;
    height: auto !important;
    box-shadow: 0 5px 15px rgba(123, 44, 191, 0.3) !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
}

.stButton>button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 20px rgba(123, 44, 191, 0.4) !important;
}

.stAlert {
    background: rgba(56, 176, 0, 0.15) !important;
    border: 1px solid var(--success) !important;
    border-radius: 16px !important;
}

.stSpinner>div>div {
    background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
    animation: pulse 1.5s infinite ease-in-out !important;
}

/* Responsive Adjustments */
@media (max-width: 992px) {
    .header-title {
        font-size: 2.8rem;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
    }
    
    .search-container {
        padding: 2rem;
    }
    
    .book-grid {
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    }
}

@media (max-width: 768px) {
    .header-title {
        font-size: 2.2rem;
    }
    
    .header-subtitle {
        font-size: 1rem;
    }
    
    .book-grid {
        grid-template-columns: 1fr;
    }
    
    .search-container {
        padding: 1.5rem;
    }
    
    .book-cover-container {
        height: 220px;
    }
    
    .fab {
        width: 60px;
        height: 60px;
        font-size: 1.5rem;
        bottom: 2rem;
        right: 2rem;
    }
}
</style>
""", unsafe_allow_html=True)

# Cosmic Header
st.markdown("""
<div class="header-container">
    <div class="header-content">
        <h1 class="header-title">Universal Pages</h1>
        <p class="header-subtitle">Explore the infinite universe of literature with our AI-powered quantum discovery engine</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Holographic Search Section
with st.container():
    st.markdown("""
    <div class="search-container">
        <h3 class="search-title">Quantum Book Search Interface</h3>
    """, unsafe_allow_html=True)
    
    with st.form(key='book_search_form'):
        col1, col2 = st.columns([3, 1])
        with col1:
            user_input = st.text_input(
                "Search for books", 
                placeholder="Enter book title, author, or genre...",
                label_visibility="collapsed"
            )
        with col2:
            submit_button = st.form_submit_button(
                "🚀 Launch Search", 
                use_container_width=True
            )
    
    st.markdown("</div>", unsafe_allow_html=True)

# Handle Search
if submit_button and user_input.strip():
    with st.spinner("🌌 Scanning the literary cosmos..."):
        response = agent.ask(user_input.strip())
        genre_pref = response.get("genre", "")
        author_pref = response.get("author", "")
        books = get_multiple_books(user_input.strip())

    if books:
        st.success(f"✨ Located {len(books)} literary artifacts matching '{user_input}'")
        
        # Cyberpunk Book Grid
        st.markdown('<div class="book-grid">', unsafe_allow_html=True)
        for book in books:
            cover_url = book["image_url"] or "https://via.placeholder.com/250x350/1A1429/FFFFFF?text=No+Cover"
            st.markdown(f"""
            <div class="book-card">
                <div class="book-cover-container">
                    <img src="{cover_url}" 
                         class="book-cover" 
                         alt="{book["title"]}"
                         onerror="this.src='https://via.placeholder.com/250x350/1A1429/FFFFFF?text=No+Cover'">
                </div>
                <div class="book-details">
                    <h3 class="book-title">{book["title"]}</h3>
                    <div class="book-author">{book["author"]}</div>
                    <div class="book-meta">
                        <span class="meta-item">{book["release_date"]}</span>
                        <span class="meta-item">{book["genre"]}</span>
                    </div>
                    <p class="book-description">{book["description"]}</p>
                    <a href="{book["preview_link"]}" target="_blank" class="preview-btn">
                        <span>Quantum Preview</span> ⚡
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # AI Hologram Panel
        if genre_pref or author_pref:
            st.markdown('<div class="ai-recs">', unsafe_allow_html=True)
            st.markdown('<h3 class="ai-title">Neural Network Recommendations</h3>', unsafe_allow_html=True)
            
            if genre_pref:
                st.markdown(f"""
                <div class="rec-card">
                    <h4 class="rec-title">📡 Genre Frequency Detected</h4>
                    <p class="rec-content">Our quantum algorithms suggest you'll resonate with <strong>{genre_pref}</strong> literature. This dimensional frequency aligns with your search parameters.</p>
                </div>
                """, unsafe_allow_html=True)
            
            if author_pref:
                st.markdown(f"""
                <div class="rec-card">
                    <h4 class="rec-title">🔍 Author Signature Match</h4>
                    <p class="rec-content">The creative waveform of <strong>{author_pref}</strong> matches your search harmonics. Explore their literary dimension.</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("⚠️ No literary artifacts detected in this dimensional plane. Try an alternate reality.")

# Cyber Orb Floating Button
st.markdown("""
<button class="fab" title="Activate Quantum Search">⚡</button>
""", unsafe_allow_html=True)

# Cyberpunk Footer
st.markdown("""
<div class="footer">
    <p>Tushar Singh © 2025</p>
    <p>Powered by Quantum Book API & CAMEL-AI</p>
</div>
""", unsafe_allow_html=True)
