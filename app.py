import streamlit as st
import google.generativeai as genai
import time
from streamlit_extras.let_it_rain import rain
from datetime import datetime

def auto_season_theme():
    month = datetime.now().month
    
    # November: Thanksgiving (Subtle Mode)
    if month == 11:
        rain(
            emoji="🍂", 
            font_size=30,       # Much smaller
            falling_speed=5,    # Slower
            animation_length="3", # Stops after 3 seconds
        )
        return "🦃 Gobble gobble! Find the perfect Thanksgiving host gift."

    # December: Christmas (Subtle Mode)
    elif month == 12:
        rain(
            emoji="❄️", 
            font_size=20, 
            falling_speed=3, 
            animation_length="3",
        )
        return "🎄 Season's Greetings! Let's find a magical gift."
        
    else:
        return "🎁 Find the perfect gift for the person who has everything."

# Store the seasonal subheader in a variable to use later
seasonal_subheader = auto_season_theme()

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Creator Gear Guide",
    page_icon="📹",
    layout="centered"
)

# Replace with your actual ID
AMAZON_TAG = st.secrets["AMAZON_AFFILIATE_TAG"]

# --- CUSTOM CSS (The "Professional" Polish) ---
st.markdown("""
<style>
    /* Make the main header look elegant */
    h1 {
        color: #FF4B4B;
        font-weight: 700;
    }
    /* subtle border for the results area */
    .stContainer {
        border-radius: 10px;
    }
    /* Hide the default Streamlit menu for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (The "Control Panel") ---
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Secure Key Handling
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("✅ API Key Loaded")
    else:
        api_key = st.text_input("Enter Google API Key", type="password")
        st.caption("Get your key from Google AI Studio")

    st.divider()
    st.markdown("### 💡 How it works")
    st.info("Describe the person in detail. The AI will browse its knowledge base to find unique, physical gifts tailored to them.")

# --- MAIN APP INTERFACE ---
st.title("📹 The Creator Gear Guide")
st.subheader("Essential Gear for Streamers, Podcasters, & Vloggers.")

# The Input Form
with st.form("gift_form"):
    user_input = st.text_area(
        "Who are we buying for?", 
        height=100,
        placeholder="Describe the content creator you're buying for: Podcaster, Twitch Gamer, Vlogger, etc."
    )
    # A big primary button
    submitted = st.form_submit_button("✨ Generate Gift Ideas", type="primary")

# --- THE LOGIC ---
if submitted:
    if not api_key:
        st.error("⚠ Please enter an API Key in the sidebar to continue.")
    elif not user_input:
        st.warning("Please describe the person first!")
    else:
        # Configure Gemini
        genai.configure(api_key=api_key)
        # Using the new, fast model
        model = genai.GenerativeModel('gemini-2.5-flash') 

        prompt = f"""
Suggest 5 specific, physical products available on Amazon for this person: '{user_input}'.

---

## CRITICAL OUTPUT INSTRUCTIONS:
1.  **DO NOT use any introduction, conversation, code fences (```), numbering, or extra characters.**
2.  **ONLY** return the raw data string.
3.  **Output Format MUST be EXACTLY:** Name || Description | Name || Description | ...
4.  Example Format: Studio Microphone || Clear, crisp audio for beginner podcasters | Boom Arm Stand || Keeps the mic off the desk to reduce vibrations | USB Audio Interface || Essential to connect professional mics for pristine sound | ...
"""

        # Visual Feedback while waiting
        with st.status("🔍 Analyzing interests...", expanded=True) as status:
            time.sleep(0.5)
            st.write("🧠 Brainstorming unique angles...")
            time.sleep(0.5)
            st.write("🎁 Selecting the best 5 items...")
            
            try:
                response = model.generate_content(prompt)
                # --- SAFETY NET: Strip common AI formatting issues ---
                raw_text = response.text.replace("```", "").replace("json", "").strip() 
                # 1. Split by single pipe '|' to get 5 separate product strings
                gift_items = [item.strip() for item in raw_text.split('|') if item.strip()]

                # Status update remains, but we don't collapse it with expanded=False
                status.update(label="✅ Ideas Found!", state="complete")
                
                st.divider()
                st.markdown("### 🎯 Top 5 Recommendations (Expert Analysis)")
                
                # 2. Iterate through each product string and split by double pipe '||'
                for item in gift_items:
                    parts = item.split('||')
                    
                    # Ensure we have a Name and a Description before proceeding
                    if len(parts) == 2:
                        name = parts[0].strip()
                        description = parts[1].strip()
                        
                        search_term = name.replace(" ", "+")
                        link = f"https://www.amazon.com/s?k={search_term}&tag={AMAZON_TAG}"
                        
                        # The Card Container (Enriched)
                        with st.container(border=True):
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.markdown(f"**{name}**")
                                # Show the expert description below the title
                                st.caption(description) 
                            with col2:
                                st.link_button("👉 View Item", link, use_container_width=True)
                                
            except Exception as e:
                status.update(label="❌ Error", state="error")
                st.error(f"Oops! Something went wrong: {e}")

# Footer
st.markdown("---")
st.caption(f"© 2025 Gift Whisperer. As an Amazon Associate, I earn from qualifying purchases.")