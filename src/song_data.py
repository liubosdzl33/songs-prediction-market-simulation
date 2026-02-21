"""
Real Song Dataset for Music Prediction Marketplace Simulation

100 songs based on real 2024-2025 artists and streaming data patterns.
Uses actual artist names, realistic song titles, and streaming parameters
grounded in real Spotify/industry data.

Data sources:
- Spotify Wrapped 2024/2025 top artist and song data
- Billboard chart performance and streaming milestones
- TikTok viral song trends 2024-2025
- Spotify "Artists to Watch" and RADAR programs
- Industry reports on streaming fraud and bot manipulation

Categories:
  - 20 mega-hit potential (top-tier artists, 0.70-0.95 organic probability)
  - 30 mid-tier artists (moderate following, 0.30-0.60 organic probability)
  - 25 indie/emerging artists (small but real audiences, 0.05-0.25)
  - 15 gaming attempts (artists trying to cheat the system)
  - 10 controversial/edge-case songs (viral wildcards, one-hit-wonders)
"""

from typing import List, Dict


def load_real_song_data() -> List[Dict]:
    """
    Returns a list of 100 song dicts with realistic parameters.

    Each dict contains:
      - title: str (song name)
      - artist: str (real artist name)
      - genre: str (matches simulation genres)
      - true_organic_probability: float (0-1, likelihood of hitting target organically)
      - underground_following: float (0-1, pre-existing buzz/leaks)
      - bot_budget: float (0 for legit, >0 for gaming)
      - is_gaming: bool
      - gaming_type: str or None ('fake_prerelease', 'bot_views', 'combined')
      - tier: str ('mega', 'mid', 'indie', 'gaming', 'edge_case')
      - description: str (context for why parameters are set this way)
    """
    songs = []

    # ================================================================
    # TIER 1: MEGA-HIT POTENTIAL (20 songs)
    # Top-tier artists with massive fanbases and proven track records.
    # true_organic_probability: 0.70-0.95
    # ================================================================

    songs.extend([
        {
            "title": "Neon Paradise",
            "artist": "Bad Bunny",
            "genre": "latin",
            "true_organic_probability": 0.93,
            "underground_following": 0.15,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mega",
            "description": "Spotify's #1 global artist 2025 with 19.8B streams. Any new single is near-guaranteed to chart.",
        },
        {
            "title": "Midnight Letters",
            "artist": "Taylor Swift",
            "genre": "pop",
            "true_organic_probability": 0.92,
            "underground_following": 0.20,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mega",
            "description": "Most-streamed female artist in Spotify history. Massive pre-save campaigns leak early.",
        },
        {
            "title": "Afterglow City",
            "artist": "The Weeknd",
            "genre": "r&b",
            "true_organic_probability": 0.90,
            "underground_following": 0.10,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mega",
            "description": "First artist to surpass 100M monthly listeners. Blinding Lights hit 5B streams.",
        },
        {
            "title": "Last Dance Forever",
            "artist": "Drake",
            "genre": "hip-hop",
            "true_organic_probability": 0.88,
            "underground_following": 0.25,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mega",
            "description": "Top 5 global artist. Heavy OVO leaks create underground buzz before drops.",
        },
        {
            "title": "Electric Venom",
            "artist": "Billie Eilish",
            "genre": "pop",
            "true_organic_probability": 0.89,
            "underground_following": 0.12,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mega",
            "description": "BIRDS OF A FEATHER sustained top-3 across 2024-2025. HIT ME HARD AND SOFT was #3 album globally.",
        },
        {
            "title": "Golden Hour Rush",
            "artist": "Bruno Mars",
            "genre": "pop",
            "true_organic_probability": 0.91,
            "underground_following": 0.08,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mega",
            "description": "Most-listened artist on Spotify Feb 2026. Die With A Smile hit 1.7B streams.",
        },
        {
            "title": "Velvet Chains",
            "artist": "Lady Gaga",
            "genre": "pop",
            "true_organic_probability": 0.87,
            "underground_following": 0.10,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mega",
            "description": "Mayhem album (March 2025) continued her hitmaking streak after Die With A Smile.",
        },
        {
            "title": "Savage Lullaby",
            "artist": "Kendrick Lamar",
            "genre": "hip-hop",
            "true_organic_probability": 0.85,
            "underground_following": 0.30,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mega",
            "description": "First rapper past 110M monthly listeners. Heavy underground anticipation for new material.",
        },
        {
            "title": "Phantom Rodeo",
            "artist": "Morgan Wallen",
            "genre": "country",
            "true_organic_probability": 0.83,
            "underground_following": 0.08,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mega",
            "description": "Top 3 US artist 2024-2025. Country crossover appeal drives massive first-week numbers.",
        },
        {
            "title": "Cosmic Sugar",
            "artist": "SZA",
            "genre": "r&b",
            "true_organic_probability": 0.86,
            "underground_following": 0.18,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mega",
            "description": "SOS Deluxe: LANA was #4 global album 2025. Strong R&B fanbase with crossover pop appeal.",
        },
        {
            "title": "Sugar Rush Disco",
            "artist": "Sabrina Carpenter",
            "genre": "pop",
            "true_organic_probability": 0.84,
            "underground_following": 0.15,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mega",
            "description": "Espresso was #1 most-streamed 2024. Short n' Sweet was #5 global album 2025.",
        },
        {
            "title": "APT. (Remix)",
            "artist": "ROSE",
            "genre": "pop",
            "true_organic_probability": 0.82,
            "underground_following": 0.20,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mega",
            "description": "APT. with Bruno Mars was #3 global song 2025. K-pop crossover into global pop.",
        },
        {
            "title": "Desert Mirage",
            "artist": "Karol G",
            "genre": "latin",
            "true_organic_probability": 0.80,
            "underground_following": 0.12,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mega",
            "description": "Latin music queen. Consistent chart domination in both Latin and global markets.",
        },
        {
            "title": "Heartbreak Highway",
            "artist": "Post Malone",
            "genre": "country",
            "true_organic_probability": 0.81,
            "underground_following": 0.10,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mega",
            "description": "Successful genre pivot to country in 2024. Cross-genre appeal boosts streaming numbers.",
        },
        {
            "title": "Dangerous Prayers",
            "artist": "Ariana Grande",
            "genre": "pop",
            "true_organic_probability": 0.85,
            "underground_following": 0.14,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mega",
            "description": "Eternal Sunshine Deluxe drove sustained streaming. Reliable pop powerhouse.",
        },
        {
            "title": "Gravity Well",
            "artist": "Coldplay",
            "genre": "rock",
            "true_organic_probability": 0.78,
            "underground_following": 0.08,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mega",
            "description": "First group to reach every monthly listener milestone from 60M-100M. Global touring boosts streams.",
        },
        {
            "title": "Electric Storm",
            "artist": "Dua Lipa",
            "genre": "electronic",
            "true_organic_probability": 0.82,
            "underground_following": 0.10,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mega",
            "description": "Dance-pop crossover queen. Radical Optimism kept her in the streaming elite.",
        },
        {
            "title": "Underworld Bounce",
            "artist": "Rauw Alejandro",
            "genre": "latin",
            "true_organic_probability": 0.79,
            "underground_following": 0.15,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mega",
            "description": "Latin trap/reggaeton star with consistent global chart performance.",
        },
        {
            "title": "Moonlit Confessions",
            "artist": "Jimin",
            "genre": "pop",
            "true_organic_probability": 0.83,
            "underground_following": 0.25,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mega",
            "description": "Who entered Spotify Billions Club 2024. #1 K-pop solo artist globally.",
        },
        {
            "title": "Fever Dream",
            "artist": "Beyonce",
            "genre": "r&b",
            "true_organic_probability": 0.90,
            "underground_following": 0.22,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mega",
            "description": "Texas Hold Em was a 2024 viral smash. Genre-defying country/R&B crossover.",
        },
    ])

    # ================================================================
    # TIER 2: MID-TIER ARTISTS (30 songs)
    # Established but not mega-star level. Growing fanbases.
    # true_organic_probability: 0.30-0.60
    # ================================================================

    songs.extend([
        {
            "title": "Beautiful Chaos",
            "artist": "Benson Boone",
            "genre": "pop",
            "true_organic_probability": 0.58,
            "underground_following": 0.10,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Beautiful Things was #2 global 2024. Breakout success but not yet proven consistent.",
        },
        {
            "title": "Ordinary Days",
            "artist": "Alex Warren",
            "genre": "pop",
            "true_organic_probability": 0.52,
            "underground_following": 0.15,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Ordinary was #4 global 2025. TikTok-driven success with 2.9M first-day streams.",
        },
        {
            "title": "Back to Us",
            "artist": "sombr",
            "genre": "pop",
            "true_organic_probability": 0.50,
            "underground_following": 0.12,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "back to friends entered Billions Club 2025. Rising star but longevity unproven.",
        },
        {
            "title": "No One Knows",
            "artist": "The Marias",
            "genre": "indie",
            "true_organic_probability": 0.45,
            "underground_following": 0.20,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Two Grammy noms. No One Noticed was #10 in US. Strong indie crossover.",
        },
        {
            "title": "Velvet Muse",
            "artist": "Leon Thomas",
            "genre": "r&b",
            "true_organic_probability": 0.40,
            "underground_following": 0.18,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Rising R&B star. My Muse on Spotify Editor Picks 2025. Building consistent catalog.",
        },
        {
            "title": "Messy Hearts",
            "artist": "Lola Young",
            "genre": "pop",
            "true_organic_probability": 0.48,
            "underground_following": 0.10,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Messy entered Spotify Billions Club. Featured on Today's Top Hits.",
        },
        {
            "title": "Gnarly Nights",
            "artist": "KATSEYE",
            "genre": "pop",
            "true_organic_probability": 0.45,
            "underground_following": 0.22,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Global girl group from HYBE talent search. Gnarly on 2025 Songs of Summer.",
        },
        {
            "title": "Lose Yourself",
            "artist": "Teddy Swims",
            "genre": "r&b",
            "true_organic_probability": 0.50,
            "underground_following": 0.08,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Lose Control was top 5 viral globally 2024. Voice-driven artist with crossover appeal.",
        },
        {
            "title": "Crimson Luck",
            "artist": "Chappell Roan",
            "genre": "pop",
            "true_organic_probability": 0.55,
            "underground_following": 0.25,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Good Luck Babe top 5 viral 2024. Rapid ascent from indie to mainstream.",
        },
        {
            "title": "Nasty Groove",
            "artist": "Tinashe",
            "genre": "r&b",
            "true_organic_probability": 0.42,
            "underground_following": 0.15,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Nasty was #2 TikTok Song of Summer 2024. Independent artist renaissance.",
        },
        {
            "title": "Million Dollar Smile",
            "artist": "Tommy Richman",
            "genre": "hip-hop",
            "true_organic_probability": 0.40,
            "underground_following": 0.20,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "MILLION DOLLAR BABY debuted #2 Hot 100 from TikTok. One big hit, follow-up uncertain.",
        },
        {
            "title": "Bar Song Remix",
            "artist": "Shaboozey",
            "genre": "country",
            "true_organic_probability": 0.48,
            "underground_following": 0.12,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Country breakout of 2024. On pace for 1B streams in under 8 months.",
        },
        {
            "title": "Anxiety Attack",
            "artist": "Doechii",
            "genre": "hip-hop",
            "true_organic_probability": 0.47,
            "underground_following": 0.18,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Anxiety sparked 10.4M TikTok creations. Five Grammy noms. Hot 100 top 10.",
        },
        {
            "title": "Love Me Maybe",
            "artist": "Ravyn Lenae",
            "genre": "r&b",
            "true_organic_probability": 0.38,
            "underground_following": 0.15,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Love Me Not went viral via TikTok mashup. First Hot 100 entry, cracked top 25.",
        },
        {
            "title": "Illegal Feelings",
            "artist": "PinkPantheress",
            "genre": "electronic",
            "true_organic_probability": 0.43,
            "underground_following": 0.20,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Illegal fueled viral TikTok challenge. Electronic-pop with Gen Z appeal.",
        },
        {
            "title": "Dusk Till Dawn",
            "artist": "Tate McRae",
            "genre": "pop",
            "true_organic_probability": 0.52,
            "underground_following": 0.10,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Consistent hitmaker with dance-pop crossover. Strong streaming momentum.",
        },
        {
            "title": "Galactic Bounce",
            "artist": "FloyyMenor",
            "genre": "latin",
            "true_organic_probability": 0.42,
            "underground_following": 0.08,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Gata Only was #4 global 2024. Latin viral hit machine.",
        },
        {
            "title": "Jah Blessings",
            "artist": "YG Marley",
            "genre": "hip-hop",
            "true_organic_probability": 0.38,
            "underground_following": 0.15,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Praise Jah In The Moonlight was a 2024 viral smash. Legacy name helps discovery.",
        },
        {
            "title": "Soaked in Blue",
            "artist": "Shy Smith",
            "genre": "r&b",
            "true_organic_probability": 0.35,
            "underground_following": 0.12,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Soaked was a trending TikTok sound 2024. Mid-tier R&B with growing fanbase.",
        },
        {
            "title": "Country Roads 2.0",
            "artist": "Dasha",
            "genre": "country",
            "true_organic_probability": 0.40,
            "underground_following": 0.10,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "2024 country breakout. Bridging pop and country with strong streaming growth.",
        },
        {
            "title": "Selfish Love",
            "artist": "Selena Gomez",
            "genre": "pop",
            "true_organic_probability": 0.60,
            "underground_following": 0.10,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "I Said I Love You First with Benny Blanco. Huge social following, moderate streaming consistency.",
        },
        {
            "title": "Solo Mission",
            "artist": "Joe Jonas",
            "genre": "pop",
            "true_organic_probability": 0.35,
            "underground_following": 0.08,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Music for People Who Believe in Love album. Name recognition but uncertain solo streaming power.",
        },
        {
            "title": "Dark Paradise",
            "artist": "Lana Del Rey",
            "genre": "indie",
            "true_organic_probability": 0.55,
            "underground_following": 0.30,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Cult following with strong pre-release buzz. Grammy must-hear album list 2025.",
        },
        {
            "title": "Mafia Melody",
            "artist": "Lisa",
            "genre": "pop",
            "true_organic_probability": 0.50,
            "underground_following": 0.25,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "BLACKPINK solo star. Massive K-pop fanbase drives first-week streams.",
        },
        {
            "title": "Revival Trail",
            "artist": "Treaty Oak Revival",
            "genre": "country",
            "true_organic_probability": 0.38,
            "underground_following": 0.15,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Country rock wave of 2025. Heavier production found massive fan base.",
        },
        {
            "title": "Afrobeats Fusion",
            "artist": "Kapo",
            "genre": "latin",
            "true_organic_probability": 0.36,
            "underground_following": 0.10,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Latin-Afrobeats crossover artist. Genre fusion driving new listener demographics.",
        },
        {
            "title": "Heavy Crown",
            "artist": "Davido",
            "genre": "hip-hop",
            "true_organic_probability": 0.42,
            "underground_following": 0.18,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Afrobeats megastar with global crossover. Strong in non-US markets.",
        },
        {
            "title": "Hurry Up Tomorrow",
            "artist": "The Weeknd",
            "genre": "r&b",
            "true_organic_probability": 0.58,
            "underground_following": 0.35,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Announced as final trilogy album. Massive anticipation but concept album risk.",
        },
        {
            "title": "Chill Vibes Only",
            "artist": "Olivia Dean",
            "genre": "pop",
            "true_organic_probability": 0.33,
            "underground_following": 0.08,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "First song on Hot Hits UK. Chill Pop and New Music Friday UK playlists. Growing UK pop star.",
        },
        {
            "title": "Magnetic Pull",
            "artist": "ILLIT",
            "genre": "pop",
            "true_organic_probability": 0.44,
            "underground_following": 0.20,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Magnetic was #5 K-pop song 2024. K-pop group with global 4th gen appeal.",
        },
    ])

    # ================================================================
    # TIER 3: INDIE/EMERGING ARTISTS (25 songs)
    # Small but real audiences. High variance outcomes.
    # true_organic_probability: 0.05-0.25
    # ================================================================

    songs.extend([
        {
            "title": "DIA",
            "artist": "Ela Minus",
            "genre": "electronic",
            "true_organic_probability": 0.12,
            "underground_following": 0.15,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Sophomore album Jan 2025. Acclaimed debut acts of rebellion. Small but devoted fanbase.",
        },
        {
            "title": "Fantasy Theatre",
            "artist": "Yaelokre",
            "genre": "indie",
            "true_organic_probability": 0.10,
            "underground_following": 0.12,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Fantasy/theatrical indie popular with Gen Z. Bold storytelling, darker tone.",
        },
        {
            "title": "Nothing Matters",
            "artist": "The Last Dinner Party",
            "genre": "rock",
            "true_organic_probability": 0.18,
            "underground_following": 0.20,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Theatrical indie rock. BRIT Awards Rising Star. Strong underground following.",
        },
        {
            "title": "Paris Nights",
            "artist": "Paris Paloma",
            "genre": "indie",
            "true_organic_probability": 0.15,
            "underground_following": 0.18,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Fantasy indie with feminist themes. Labour went viral on TikTok. Niche but passionate fans.",
        },
        {
            "title": "Sailor Heart",
            "artist": "Gigi Perez",
            "genre": "indie",
            "true_organic_probability": 0.20,
            "underground_following": 0.15,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Sailor Song went viral 2025. Dominican-American folksy indie. Queer anthem breakout.",
        },
        {
            "title": "Shoegaze Dreams",
            "artist": "Dream Boy",
            "genre": "rock",
            "true_organic_probability": 0.08,
            "underground_following": 0.12,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Dublin shoegaze band. Slowdive/MBV influenced. Small but growing live following.",
        },
        {
            "title": "Glitch Pop",
            "artist": "Asher White",
            "genre": "electronic",
            "true_organic_probability": 0.09,
            "underground_following": 0.08,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Debut on Joyful Noise. Chamber pop to grunge to glitch. Critic darling, small audience.",
        },
        {
            "title": "Homegrown",
            "artist": "Waxahatchee",
            "genre": "country",
            "true_organic_probability": 0.15,
            "underground_following": 0.20,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Americana/alt-country. Part of Spotify Homegrown playlist wave. Critics' favorite.",
        },
        {
            "title": "Lone Signal",
            "artist": "Militarie Gun",
            "genre": "rock",
            "true_organic_probability": 0.11,
            "underground_following": 0.15,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Post-hardcore/indie rock. Grammy.com must-hear Oct 2025. Cult following.",
        },
        {
            "title": "Pastel Morning",
            "artist": "Clairo",
            "genre": "indie",
            "true_organic_probability": 0.22,
            "underground_following": 0.18,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Bedroom pop pioneer. Charm era showed artistic growth. Loyal indie fanbase.",
        },
        {
            "title": "Broken Algorithm",
            "artist": "100 gecs",
            "genre": "electronic",
            "true_organic_probability": 0.13,
            "underground_following": 0.22,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Hyperpop pioneers. Very niche but intensely devoted fanbase. High underground buzz.",
        },
        {
            "title": "Summer Haze",
            "artist": "Remi Wolf",
            "genre": "pop",
            "true_organic_probability": 0.18,
            "underground_following": 0.12,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Indie pop with funky production. Festival circuit favorite. Growing Spotify presence.",
        },
        {
            "title": "Rust Belt Blues",
            "artist": "Wunderhorse",
            "genre": "rock",
            "true_organic_probability": 0.10,
            "underground_following": 0.14,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "UK indie rock. Critical acclaim, small streaming numbers. Live reputation growing.",
        },
        {
            "title": "Neon Prayers",
            "artist": "Ethel Cain",
            "genre": "indie",
            "true_organic_probability": 0.16,
            "underground_following": 0.25,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Gothic Americana. Preacher's Daughter was cult classic. Very strong underground following.",
        },
        {
            "title": "Quiet Storm",
            "artist": "Daniel Caesar",
            "genre": "r&b",
            "true_organic_probability": 0.25,
            "underground_following": 0.15,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Alt-R&B with Grammy pedigree. Consistent but not explosive streaming numbers.",
        },
        {
            "title": "Ghost Frequency",
            "artist": "Fontaines D.C.",
            "genre": "rock",
            "true_organic_probability": 0.14,
            "underground_following": 0.18,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Irish post-punk. Romance Was Born showed commercial potential. Festival headliners.",
        },
        {
            "title": "Butterfly Knife",
            "artist": "Beabadoobee",
            "genre": "indie",
            "true_organic_probability": 0.20,
            "underground_following": 0.15,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Filipino-British indie star. TikTok discovery pipeline. Building toward mainstream.",
        },
        {
            "title": "Chrome Hearts",
            "artist": "Mk.gee",
            "genre": "indie",
            "true_organic_probability": 0.12,
            "underground_following": 0.20,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Lo-fi R&B/indie. Critical darling with strong underground buzz. Small but growing.",
        },
        {
            "title": "Sangria Sunset",
            "artist": "Omar Apollo",
            "genre": "r&b",
            "true_organic_probability": 0.22,
            "underground_following": 0.14,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Bilingual R&B/indie. God Said No showed artistic range. Growing Latin-American crossover.",
        },
        {
            "title": "Midnight in Lagos",
            "artist": "Rema",
            "genre": "hip-hop",
            "true_organic_probability": 0.24,
            "underground_following": 0.15,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Afrobeats star. Calm Down was massive but follow-up consistency still proving out.",
        },
        {
            "title": "Violet Hour",
            "artist": "Japanese Breakfast",
            "genre": "indie",
            "true_organic_probability": 0.15,
            "underground_following": 0.16,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Indie rock/dream pop. Grammy-nominated. Strong critical acclaim, niche streaming.",
        },
        {
            "title": "Desert Oasis",
            "artist": "Mdou Moctar",
            "genre": "rock",
            "true_organic_probability": 0.06,
            "underground_following": 0.12,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Tuareg guitar legend. Critical acclaim from Pitchfork/NPR. Very niche but passionate.",
        },
        {
            "title": "Synthetic Love",
            "artist": "Caroline Polacheck",
            "genre": "electronic",
            "true_organic_probability": 0.19,
            "underground_following": 0.18,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Art pop/electronic. Growing from indie to mid-tier. Festival circuit buzz.",
        },
        {
            "title": "Feral Joy",
            "artist": "Mannequin Pussy",
            "genre": "rock",
            "true_organic_probability": 0.10,
            "underground_following": 0.14,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Punk/indie rock. I Got Heaven was 2024 critical favorite. Small but fierce fanbase.",
        },
        {
            "title": "Hologram Heart",
            "artist": "Magdalena Bay",
            "genre": "electronic",
            "true_organic_probability": 0.16,
            "underground_following": 0.15,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Synth-pop duo. Imaginal Disk was 2024 indie album of the year contender.",
        },
    ])

    # ================================================================
    # TIER 4: GAMING ATTEMPTS (15 songs)
    # Artists/entities trying to game the prediction market.
    # Mix of fake_prerelease, bot_views, and combined strategies.
    # ================================================================

    songs.extend([
        {
            "title": "Viral Machine",
            "artist": "StreamLord99",
            "genre": "hip-hop",
            "true_organic_probability": 0.05,
            "underground_following": 0.0,
            "bot_budget": 8000,
            "is_gaming": True,
            "gaming_type": "bot_views",
            "tier": "gaming",
            "description": "Pure bot farm operation. Inspired by the Michael Smith AI streaming fraud ($10M+). Uses bot accounts to inflate plays.",
        },
        {
            "title": "Lo-Fi Study Beats Vol. 47",
            "artist": "ChillWaveAI",
            "genre": "electronic",
            "true_organic_probability": 0.03,
            "underground_following": 0.0,
            "bot_budget": 5000,
            "is_gaming": True,
            "gaming_type": "bot_views",
            "tier": "gaming",
            "description": "AI-generated playlist stuffing scheme. Popular-sounding titles (Lo-Fi/Study) to attract organic plays alongside bot streams.",
        },
        {
            "title": "Trap Symphony",
            "artist": "GhostProducer404",
            "genre": "hip-hop",
            "true_organic_probability": 0.08,
            "underground_following": 0.0,
            "bot_budget": 12000,
            "is_gaming": True,
            "gaming_type": "bot_views",
            "tier": "gaming",
            "description": "High-budget bot operation using VPN-masked plays from multiple countries. Modeled on Drake RICO lawsuit allegations.",
        },
        {
            "title": "Bedroom Pop Dreams",
            "artist": "FakeIndie_",
            "genre": "indie",
            "true_organic_probability": 0.10,
            "underground_following": 0.0,
            "bot_budget": 3000,
            "is_gaming": True,
            "gaming_type": "bot_views",
            "tier": "gaming",
            "description": "Low-budget bot scheme on indie track. Trying to crack Spotify algorithmic playlists with fake initial momentum.",
        },
        {
            "title": "Reggaeton Fire",
            "artist": "BotMaster_MX",
            "genre": "latin",
            "true_organic_probability": 0.06,
            "underground_following": 0.0,
            "bot_budget": 6000,
            "is_gaming": True,
            "gaming_type": "bot_views",
            "tier": "gaming",
            "description": "Latin market bot scheme. Click farms in Latin America generating fake plays.",
        },
        {
            "title": "Underground Kings",
            "artist": "HypeBuilder",
            "genre": "hip-hop",
            "true_organic_probability": 0.45,
            "underground_following": 0.60,
            "bot_budget": 0,
            "is_gaming": True,
            "gaming_type": "fake_prerelease",
            "tier": "gaming",
            "description": "Fabricated underground buzz. Fake leak campaigns and planted social media hype to drive pre-release betting.",
        },
        {
            "title": "Secret Sessions",
            "artist": "ViralScam",
            "genre": "pop",
            "true_organic_probability": 0.55,
            "underground_following": 0.50,
            "bot_budget": 0,
            "is_gaming": True,
            "gaming_type": "fake_prerelease",
            "tier": "gaming",
            "description": "Fake listening party leaks. Creates artificial insider knowledge to manipulate prediction markets.",
        },
        {
            "title": "Next Big Thing",
            "artist": "PayolaKing",
            "genre": "pop",
            "true_organic_probability": 0.40,
            "underground_following": 0.45,
            "bot_budget": 0,
            "is_gaming": True,
            "gaming_type": "fake_prerelease",
            "tier": "gaming",
            "description": "Playlist payola scheme. Pays playlist curators for placement, inflating underground buzz metrics.",
        },
        {
            "title": "Phantom Hit",
            "artist": "InsiderTrader",
            "genre": "r&b",
            "true_organic_probability": 0.60,
            "underground_following": 0.55,
            "bot_budget": 0,
            "is_gaming": True,
            "gaming_type": "fake_prerelease",
            "tier": "gaming",
            "description": "Label insider leaking release info to accomplices who bet on the prediction market.",
        },
        {
            "title": "Astroturf Anthem",
            "artist": "SocialBotNet",
            "genre": "pop",
            "true_organic_probability": 0.50,
            "underground_following": 0.40,
            "bot_budget": 0,
            "is_gaming": True,
            "gaming_type": "fake_prerelease",
            "tier": "gaming",
            "description": "Coordinated fake social media campaign. Thousands of fake accounts hype a mediocre song.",
        },
        {
            "title": "Double Down",
            "artist": "ComboSchemer",
            "genre": "hip-hop",
            "true_organic_probability": 0.35,
            "underground_following": 0.40,
            "bot_budget": 7000,
            "is_gaming": True,
            "gaming_type": "combined",
            "tier": "gaming",
            "description": "Combined fake buzz + bot streams. Manufactures hype then uses bots to fulfill the prediction.",
        },
        {
            "title": "Crypto Beat",
            "artist": "Web3Scammer",
            "genre": "electronic",
            "true_organic_probability": 0.30,
            "underground_following": 0.35,
            "bot_budget": 10000,
            "is_gaming": True,
            "gaming_type": "combined",
            "tier": "gaming",
            "description": "High-budget combined scheme. Uses crypto to fund bot farms while running fake hype campaigns. Inspired by Drake/Stake allegations.",
        },
        {
            "title": "Sybil Sessions",
            "artist": "MultiAccount",
            "genre": "electronic",
            "true_organic_probability": 0.40,
            "underground_following": 0.30,
            "bot_budget": 4000,
            "is_gaming": True,
            "gaming_type": "combined",
            "tier": "gaming",
            "description": "Sybil attack: multiple fake trader accounts + moderate bot streams. Tries to manipulate market price.",
        },
        {
            "title": "Chart Manipulator",
            "artist": "PlaylistStuffer",
            "genre": "pop",
            "true_organic_probability": 0.35,
            "underground_following": 0.25,
            "bot_budget": 15000,
            "is_gaming": True,
            "gaming_type": "combined",
            "tier": "gaming",
            "description": "Biggest budget gaming attempt. Playlist stuffing + massive bot farm. High risk, high reward scheme.",
        },
        {
            "title": "Fake Famous",
            "artist": "DistroKidAbuser",
            "genre": "pop",
            "true_organic_probability": 0.15,
            "underground_following": 0.20,
            "bot_budget": 9000,
            "is_gaming": True,
            "gaming_type": "combined",
            "tier": "gaming",
            "description": "Uses open distributor to upload, then bots + fake social proof. Modeled on real DistroKid fraud patterns.",
        },
    ])

    # ================================================================
    # TIER 5: EDGE CASES / CONTROVERSIAL (10 songs)
    # Viral wildcards, one-hit-wonder potential, unexpected hits,
    # rediscovered tracks, and other unpredictable scenarios.
    # ================================================================

    songs.extend([
        {
            "title": "Pretty Little Baby (2025 Revival)",
            "artist": "Connie Francis",
            "genre": "pop",
            "true_organic_probability": 0.25,
            "underground_following": 0.05,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "edge_case",
            "description": "1962 track went viral on TikTok 2025. 28.4M TikTok creations, 130M Spotify streams. Completely unpredictable resurgence.",
        },
        {
            "title": "Let Down (Rediscovered)",
            "artist": "Radiohead",
            "genre": "rock",
            "true_organic_probability": 0.18,
            "underground_following": 0.10,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "edge_case",
            "description": "1997 track rediscovered via TikTok 2025. Classic rock finds new Gen Z audience. Unpredictable streaming pattern.",
        },
        {
            "title": "Dance You Outta My Head",
            "artist": "Cat Janice",
            "genre": "pop",
            "true_organic_probability": 0.20,
            "underground_following": 0.05,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "edge_case",
            "description": "Posthumous viral hit. Emotional TikTok story drove massive sympathy streams. One-time event.",
        },
        {
            "title": "Rock That Body (Remastered)",
            "artist": "Black Eyed Peas",
            "genre": "electronic",
            "true_organic_probability": 0.15,
            "underground_following": 0.03,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "edge_case",
            "description": "2009 track resurfacing on TikTok 2025. Nostalgia play with uncertain staying power.",
        },
        {
            "title": "Breakin Dishes (Club Edit)",
            "artist": "Rihanna",
            "genre": "r&b",
            "true_organic_probability": 0.22,
            "underground_following": 0.08,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "edge_case",
            "description": "Deep cut rediscovered via TikTok 2025. New generation discovering Rihanna catalog tracks.",
        },
        {
            "title": "KPop Demon Hunters Theme",
            "artist": "HUNTR/X",
            "genre": "pop",
            "true_organic_probability": 0.55,
            "underground_following": 0.30,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "edge_case",
            "description": "Netflix soundtrack. KPop Demon Hunters was #2 global album 2025. Movie/show tie-in creates unusual streaming pattern.",
        },
        {
            "title": "First Contact",
            "artist": "Saja Boys",
            "genre": "pop",
            "true_organic_probability": 0.40,
            "underground_following": 0.25,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "edge_case",
            "description": "KPop Demon Hunters cast. Fictional group turned real music act. Unusual artist origin creates prediction uncertainty.",
        },
        {
            "title": "AI Collab",
            "artist": "Grimes x AI",
            "genre": "electronic",
            "true_organic_probability": 0.30,
            "underground_following": 0.20,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "edge_case",
            "description": "AI-assisted music creation. Controversial but legitimate. Uncertain how platforms will count/credit streams.",
        },
        {
            "title": "TikTok Symphony",
            "artist": "Unknown Bedroom Producer",
            "genre": "electronic",
            "true_organic_probability": 0.08,
            "underground_following": 0.02,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "edge_case",
            "description": "Zero-follower artist whose track could randomly go viral. Extremely high variance. Models the long-tail TikTok discovery.",
        },
        {
            "title": "Regional Anthem",
            "artist": "Arijit Singh",
            "genre": "pop",
            "true_organic_probability": 0.35,
            "underground_following": 0.40,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "edge_case",
            "description": "Most-followed artist on Spotify (Indian playback singer). Huge in South Asia, unpredictable in global market prediction.",
        },
    ])

    return songs


def get_scenario_songs() -> List[Dict]:
    """
    Returns a curated subset of songs designed to exercise every scenario
    path in the simulation. Useful for targeted testing.

    Scenarios covered:
    1. Guaranteed mega-hit (high organic prob, no gaming)
    2. Guaranteed miss (very low organic prob, no gaming)
    3. Bot-only gaming (no real audience, pure bot farm)
    4. Fake pre-release gaming (manufactured buzz, no bots)
    5. Combined gaming (fake buzz + bots)
    6. Borderline case (moderate prob, could go either way)
    7. High underground following, legitimate
    8. Viral wildcard (very low base, potential TikTok explosion)
    9. Rediscovered classic (old track going viral)
    10. K-pop / international edge case
    11. Sybil attack scenario (multiple fake accounts + bots)
    12. Creator self-trading attempt (insider trading)
    13. High-budget sophisticated gaming
    14. Low-budget amateur gaming
    15. Posthumous / sympathy-driven streams
    """
    return [
        # 1. Guaranteed mega-hit
        {
            "title": "Neon Parade",
            "artist": "Bad Bunny",
            "genre": "latin",
            "true_organic_probability": 0.95,
            "underground_following": 0.15,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mega",
            "description": "Scenario: near-certain hit. Tests resolution when target is easily met.",
        },
        # 2. Guaranteed miss
        {
            "title": "Whisper in the Void",
            "artist": "Unknown Artist 7291",
            "genre": "indie",
            "true_organic_probability": 0.02,
            "underground_following": 0.0,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Scenario: near-certain miss. Tests resolution when target clearly not met.",
        },
        # 3. Bot-only gaming
        {
            "title": "Bot Farm Anthem",
            "artist": "StreamLord",
            "genre": "hip-hop",
            "true_organic_probability": 0.03,
            "underground_following": 0.0,
            "bot_budget": 10000,
            "is_gaming": True,
            "gaming_type": "bot_views",
            "tier": "gaming",
            "description": "Scenario: pure bot operation. Tests bot detection and contract voiding.",
        },
        # 4. Fake pre-release gaming
        {
            "title": "Leaked Sessions",
            "artist": "HypeManipulator",
            "genre": "pop",
            "true_organic_probability": 0.50,
            "underground_following": 0.65,
            "bot_budget": 0,
            "is_gaming": True,
            "gaming_type": "fake_prerelease",
            "tier": "gaming",
            "description": "Scenario: manufactured underground buzz. Tests fake pre-release detection.",
        },
        # 5. Combined gaming
        {
            "title": "Full Scheme",
            "artist": "ComboAttacker",
            "genre": "electronic",
            "true_organic_probability": 0.30,
            "underground_following": 0.40,
            "bot_budget": 8000,
            "is_gaming": True,
            "gaming_type": "combined",
            "tier": "gaming",
            "description": "Scenario: dual attack (bots + fake buzz). Tests combined detection.",
        },
        # 6. Borderline case
        {
            "title": "Maybe This Time",
            "artist": "Benson Boone",
            "genre": "pop",
            "true_organic_probability": 0.50,
            "underground_following": 0.10,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mid",
            "description": "Scenario: coin-flip probability. Tests market price accuracy at 50/50.",
        },
        # 7. High underground following, legitimate
        {
            "title": "Cult Classic",
            "artist": "Ethel Cain",
            "genre": "indie",
            "true_organic_probability": 0.18,
            "underground_following": 0.40,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "indie",
            "description": "Scenario: strong pre-existing buzz, low mainstream probability. Tests info leakage in trading.",
        },
        # 8. Viral wildcard
        {
            "title": "Random Bedroom Beat",
            "artist": "NoFollowers",
            "genre": "electronic",
            "true_organic_probability": 0.05,
            "underground_following": 0.0,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "edge_case",
            "description": "Scenario: zero-base artist with tiny viral chance. Tests extreme long-tail outcomes.",
        },
        # 9. Rediscovered classic
        {
            "title": "Pretty Little Baby",
            "artist": "Connie Francis",
            "genre": "pop",
            "true_organic_probability": 0.25,
            "underground_following": 0.05,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "edge_case",
            "description": "Scenario: old track resurgence. Tests unusual streaming pattern handling.",
        },
        # 10. K-pop / international edge case
        {
            "title": "Global Wave",
            "artist": "Jimin",
            "genre": "pop",
            "true_organic_probability": 0.75,
            "underground_following": 0.30,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "mega",
            "description": "Scenario: K-pop fandom-driven streams. Tests high underground + high organic combo.",
        },
        # 11. Sybil attack
        {
            "title": "Sybil Storm",
            "artist": "MultiAccount",
            "genre": "electronic",
            "true_organic_probability": 0.35,
            "underground_following": 0.30,
            "bot_budget": 5000,
            "is_gaming": True,
            "gaming_type": "combined",
            "tier": "gaming",
            "description": "Scenario: sybil attack with multiple fake trader accounts. Tests sybil detection.",
        },
        # 12. Creator self-trading
        {
            "title": "Insider Edge",
            "artist": "SelfTrader",
            "genre": "r&b",
            "true_organic_probability": 0.65,
            "underground_following": 0.50,
            "bot_budget": 0,
            "is_gaming": True,
            "gaming_type": "fake_prerelease",
            "tier": "gaming",
            "description": "Scenario: creator tries to trade on own song. Tests creator restriction enforcement.",
        },
        # 13. High-budget sophisticated gaming
        {
            "title": "Whale Scheme",
            "artist": "BigBudgetFraud",
            "genre": "pop",
            "true_organic_probability": 0.40,
            "underground_following": 0.35,
            "bot_budget": 15000,
            "is_gaming": True,
            "gaming_type": "combined",
            "tier": "gaming",
            "description": "Scenario: maximum-budget sophisticated attack. Tests system limits of detection.",
        },
        # 14. Low-budget amateur gaming
        {
            "title": "Cheap Tricks",
            "artist": "BudgetBot",
            "genre": "hip-hop",
            "true_organic_probability": 0.08,
            "underground_following": 0.0,
            "bot_budget": 1500,
            "is_gaming": True,
            "gaming_type": "bot_views",
            "tier": "gaming",
            "description": "Scenario: small-scale amateur bot operation. Tests detection of low-effort fraud.",
        },
        # 15. Sympathy / posthumous streams
        {
            "title": "Dance You Outta My Head",
            "artist": "Cat Janice",
            "genre": "pop",
            "true_organic_probability": 0.22,
            "underground_following": 0.05,
            "bot_budget": 0,
            "is_gaming": False,
            "gaming_type": None,
            "tier": "edge_case",
            "description": "Scenario: posthumous viral hit. Tests unusual spike patterns that look like bots but aren't.",
        },
    ]


def get_genre_distribution() -> Dict[str, int]:
    """Returns the genre breakdown of the full dataset for validation."""
    songs = load_real_song_data()
    genres = {}
    for s in songs:
        g = s["genre"]
        genres[g] = genres.get(g, 0) + 1
    return dict(sorted(genres.items(), key=lambda x: -x[1]))


def get_tier_distribution() -> Dict[str, int]:
    """Returns the tier breakdown of the full dataset for validation."""
    songs = load_real_song_data()
    tiers = {}
    for s in songs:
        t = s["tier"]
        tiers[t] = tiers.get(t, 0) + 1
    return dict(sorted(tiers.items(), key=lambda x: -x[1]))


def validate_dataset() -> Dict:
    """
    Validate the dataset meets all requirements.
    Returns a dict with validation results.
    """
    songs = load_real_song_data()
    scenarios = get_scenario_songs()

    errors = []
    warnings = []

    # Check count
    if len(songs) != 100:
        errors.append(f"Expected 100 songs, got {len(songs)}")

    # Check tier distribution
    tiers = get_tier_distribution()
    expected_tiers = {"mega": 20, "mid": 30, "indie": 25, "gaming": 15, "edge_case": 10}
    for tier, expected in expected_tiers.items():
        actual = tiers.get(tier, 0)
        if actual != expected:
            errors.append(f"Tier '{tier}': expected {expected}, got {actual}")

    # Check gaming songs
    gaming_songs = [s for s in songs if s["is_gaming"]]
    if len(gaming_songs) != 15:
        errors.append(f"Expected 15 gaming songs, got {len(gaming_songs)}")

    # Validate gaming types
    gaming_types = set(s["gaming_type"] for s in gaming_songs)
    expected_types = {"bot_views", "fake_prerelease", "combined"}
    if gaming_types != expected_types:
        errors.append(f"Missing gaming types: {expected_types - gaming_types}")

    # Check probability ranges per tier
    for song in songs:
        p = song["true_organic_probability"]
        tier = song["tier"]
        if tier == "mega" and not (0.70 <= p <= 0.95):
            warnings.append(f"Mega-tier '{song['title']}' has prob {p} outside 0.70-0.95")
        if tier == "indie" and not (0.05 <= p <= 0.25):
            warnings.append(f"Indie-tier '{song['title']}' has prob {p} outside 0.05-0.25")

    # Check that gaming songs with bot_views have bot_budget > 0
    for song in gaming_songs:
        if song["gaming_type"] in ("bot_views", "combined") and song["bot_budget"] <= 0:
            errors.append(f"Gaming song '{song['title']}' with type '{song['gaming_type']}' has no bot budget")
        if song["gaming_type"] == "fake_prerelease" and song["bot_budget"] != 0:
            warnings.append(f"Fake prerelease '{song['title']}' has bot_budget={song['bot_budget']}")

    # Check scenario coverage
    if len(scenarios) != 15:
        errors.append(f"Expected 15 scenario songs, got {len(scenarios)}")

    # Check required fields in all songs
    required_fields = [
        "title", "artist", "genre", "true_organic_probability",
        "underground_following", "bot_budget", "is_gaming", "gaming_type",
        "tier", "description"
    ]
    for i, song in enumerate(songs):
        for field in required_fields:
            if field not in song:
                errors.append(f"Song {i} missing field: {field}")

    return {
        "valid": len(errors) == 0,
        "total_songs": len(songs),
        "total_scenarios": len(scenarios),
        "tier_distribution": tiers,
        "genre_distribution": get_genre_distribution(),
        "errors": errors,
        "warnings": warnings,
    }


if __name__ == "__main__":
    result = validate_dataset()
    print(f"Dataset valid: {result['valid']}")
    print(f"Total songs: {result['total_songs']}")
    print(f"Total scenarios: {result['total_scenarios']}")
    print(f"Tier distribution: {result['tier_distribution']}")
    print(f"Genre distribution: {result['genre_distribution']}")
    if result["errors"]:
        print(f"\nErrors:")
        for e in result["errors"]:
            print(f"  - {e}")
    if result["warnings"]:
        print(f"\nWarnings:")
        for w in result["warnings"]:
            print(f"  - {w}")
