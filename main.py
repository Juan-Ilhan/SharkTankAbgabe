from openai import OpenAI
from Shark import Shark
from Candidate import Candidate
from PitchSession import PitchSession
from ScrapeGraphAgent import ScrapeGraphAgent

def main():
    # API-Schlüssel einlesen und Client instanziieren
    api_key_path = "api_key"  # Pfad zur API-Key-Datei
    api_key = open(api_key_path, "r").read().strip()
    client = OpenAI(api_key=api_key)

    # Web-Scraping-Agent initialisieren
    scraping_agent = ScrapeGraphAgent(api_key=api_key)

    # Erstellen des Kandidaten
    candidate = Candidate(
        name="Seneca Hampton",
        startup_idea="Hampton Adams",
        sector="sports medicine and athletic equipment",
        product_description="I present athletic tape. But not just any athletic tape. Sharks, this is Hampton Adams, baby. Watch this. It's 45 pounds here and the tape can lift the plate without tearing. But wait, there's more. You know that tape that's so strong that you gotta use the jaws of life or be a bodybuilder to tear it? Not here, baby. We fixed that. Watch this, it tears apart effortlessly, like butter, baby. Listening to athletes. We've developed an entire line of sports medicine products specifically for the athlete, trainer and physical therapist. ",
        valuation=5000000,
        asking_amount=500000,
        equity_offered=10,
        client=client,
        scraping_agent=scraping_agent
    )

    # Liste der Haie/Juroren erstellen, inklusive ihrer Expertise
    sharks = [
        Shark("Kevin O'Leary", "tough negotiator, focused on royalties, values clear financials, and prefers businesses with predictable cash flow", "finance and royalties", client),
        #Shark("Mark Cuban", "tech guru, seeks high-growth potential, values innovation, and prefers businesses with scalable models", "technology and startups", client),
        Shark("Lori Greiner", "queen of QVC, loves consumer products, values uniqueness, and prefers products with mass appeal", "consumer products and retail", client),
        #Shark("Robert Herjavec", "cybersecurity expert, values strong defenses, prefers businesses with technological advantages, and is keen on market disruptors", "technology and cybersecurity", client),
        #Shark("Daymond John", "branding expert, specializes in fashion, values brand potential, and prefers businesses with strong social media presence", "fashion and branding", client),
        #Shark("Barbara Corcoran", "real estate mogul, looks for unique propositions, values grit and determination in entrepreneurs, and prefers businesses with a personal touch", "real estate and small business", client)
    ]

    # Session initialisieren und durchführen
    session = PitchSession(candidate, sharks)
    session.run_session()

if __name__ == "__main__":
    main()
