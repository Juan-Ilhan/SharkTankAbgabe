
from openai import OpenAI

class Candidate:
    def __init__(self, name, startup_idea, product_description, sector, valuation, asking_amount, equity_offered, client, scraping_agent):
        self.name = name
        self.startup_idea = startup_idea
        self.product_description = product_description
        self.valuation = valuation
        self.sector = sector
        self.asking_amount = asking_amount
        self.equity_offered = equity_offered
        self.client = client
        self.scraping_agent = scraping_agent
        self.offers = []

    def introduce(self):
        introduction = (
            f"Sharks, what is up? My name is {self.name} I'm from Las Vegas, Nevada, baby. And today I'm seeking ${self.asking_amount:,} "
            f"in exchange for {self.equity_offered}% of my company {self.startup_idea}."
            f"Okay, sharks, if you've played sports, then, you know there is one product, one piece of equipment that almost every athlete uses without fail. Some people just won't perform without it. Allow me to introduce you to one of the greatest creations on planet Earth."
        )
        product_explanation = (
            f" {self.product_description} So, sharks, who wants to roll with me to take the world by storm?"
        )
        return introduction + "\n" + product_explanation


    def answer_question(self, question):

        # Step 1: Webscraping für aktuelle Informationen
        search_results = self.scraping_agent.search_web(question)
        if "product" in question.lower() or "feedback" in question.lower() or "reviews" in question.lower():
            feedback_results = self.scraping_agent.scrape_feedback()
            analyzed_results = self.scraping_agent.analyze_results(search_results, feedback_results)
        else:
            analyzed_results = self.scraping_agent.analyze_results(search_results)

        # Step 1: Abstraktion - Allgemeine Step-Back-Frage
        abstraction_prompt = [
            {"role": "system", "content": "You are an expert in startup pitches and investor relations."},
            {"role": "user", "content": "When responding to investor questions during a startup pitch, it is important to be clear, concise, and informative. "
                                        "summarize the best practices for answering investor questions during a pitch."
                                        f"Also, consider the following information obtained from recent data: {analyzed_results}"}
        ]

        abstraction_response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=abstraction_prompt,
            max_tokens=150,
            temperature=0.5,
            stop=["\n"]
        )

        general_information = abstraction_response.choices[0].message.content.strip()


        print(f"Analyzed search results for '{question}': {analyzed_results}")

        # Step 2: Reasoning - Originalfrage mit allgemeiner Information
        reasoning_prompt = [
            {"role": "system", "content": "You are the candidate in the TV-Show SharkTank."},
            {"role": "user", "content": f"{question} Based on the general considerations: {general_information} and the specific data: {analyzed_results}, how would you respond to this question in just a few sentences.?"},
        ]

        reasoning_response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=reasoning_prompt,
            max_tokens=250,
            temperature=0.5
        )

        return reasoning_response.choices[0].message.content.strip()

    def add_offer(self, offer):
        self.offers.append(offer)


    def choose_best_offer(self):
        if not self.offers:
            print("\nNo valid offers were made.")
            return

        offers_summary = "Here are the offers made:\n"
        for shark_name, offer in self.offers:
            offers_summary += f"{shark_name} offered: {offer}\n"

        # Step 1: Abstraktion - Allgemeine Step-Back-Frage
        abstraction_prompt = [
            {"role": "system", "content": "You are an expert in evaluating startup investments."},
            {"role": "user", "content": (
                "Consider the following general factors for evaluating offers: "
                "1. Financial value: The amount of money offered in exchange for equity. "
                "2. Strategic value: The expertise, connections, and support the investor can bring to the startup. "
                "3. Long-term potential: The potential for growth and future funding opportunities. "
                "Based on these general considerations, summarize the key points to evaluate startup investment offers."
            )}
        ]

        abstraction_response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=abstraction_prompt,
            max_tokens=150,
            temperature=0.5,
            stop=["\n"]
        )

        general_information = abstraction_response.choices[0].message.content.strip()

        # Step 2: Reasoning - Originalfrage mit allgemeiner Information
        reasoning_prompt = [
            {"role": "system", "content": "You are the candidate in the TV-Show SharkTank."},
            {"role": "user", "content": f"Given these offers: {offers_summary}. Based on the general considerations: {general_information}, which one would you accept based on the best financial and strategic value for your startup? "
                                        f"Consider the expertise and value each Shark can bring to your company."
                                        f"Choose the best offer or explain why none of the offers are satisfactory."}
        ]

        reasoning_response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=reasoning_prompt,
            max_tokens=250,
            temperature=0.5,
            stop=["\n"]
        )

        if reasoning_response.choices:
            decision = reasoning_response.choices[0].message.content.strip()
            print(f"\nThe candidate's decision: {decision}")
        else:
            print("\nThe AI was unable to determine the best offer. Please review manually.")

    def generate_feedback(self):
        # Generiere Feedback basierend auf der gesamten Session
        feedback_prompt = [
            {"role": "system", "content": "You are an AI providing feedback in a startup investment simulation."},
            {"role": "user", "content": "Based on the entire pitch session, including the questions asked, the answers given, and the final decision made, provide comprehensive feedback to the candidate on their performance and areas for improvement."}
        ]

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=feedback_prompt,
            max_tokens=300,
            temperature=0.5,
            stop=["\n"]
        )

        if response.choices:
            feedback = response.choices[0].message.content.strip()
            print(f"\nFeedback for the candidate: {feedback}")
        else:
            print("\nUnable to generate feedback at this time.")
