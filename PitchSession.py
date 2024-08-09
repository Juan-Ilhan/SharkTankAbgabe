class PitchSession:
    def __init__(self, candidate, sharks):
        self.candidate = candidate
        self.sharks = sharks

    def run_session(self):
        print(self.candidate.introduce())
        product_description = self.candidate.product_description

        for shark in self.sharks:
            print("\n")  # Fügt eine Leerzeile für bessere Lesbarkeit ein
            question = shark.ask_question(product_description, self.candidate.sector)
            print(f"{shark.name} asks: {question}")
            answer = self.candidate.answer_question(question)
            print(f"{self.candidate.name} answers: {answer}")

            offer = shark.make_offer(product_description, self.candidate.valuation, self.candidate.asking_amount)
            print(f"{shark.name} decides: {offer}")
            if "invest" in offer.lower() or "accept" in offer.lower():  # Check, ob ein Investitionsangebot gemacht wurde
                self.candidate.add_offer((shark.name, offer))

        # Rufe die Methode auf dem Candidate-Objekt auf
        self.candidate.choose_best_offer()
        self.candidate.generate_feedback()  # Angenommen, diese Methode existiert zur Generierung von Feedback
