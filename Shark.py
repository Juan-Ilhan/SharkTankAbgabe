class Shark:
    def __init__(self, name, personality, expertise, client):
        self.name = name
        self.personality = personality
        self.expertise = expertise
        self.client = client

    def ask_question(self, product_description, sector):
        # Step 1: Abstraktion - Allgemeine Step-Back-Frage
        abstraction_prompt = [
            {"role": "system",
             "content": f"{self.name} is a shark known for their {self.personality} in {self.expertise}."},
            {"role": "user",
             "content": f"The company offers {product_description} in the {sector} sector. "
                        f"What are the general considerations for evaluating the potential and viability of a startup in this sector?"}
    ]

        abstraction_response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=abstraction_prompt,
            max_tokens=150,
            temperature=0.6,
            stop=["\n"]
        )

        general_information = abstraction_response.choices[0].message.content.strip()

        # Step 2: Reasoning - Originalfrage mit allgemeiner Information
        reasoning_prompt = [
            {"role": "system",
             "content": f"{self.name} is a shark known for their {self.personality} in {self.expertise}."},
            {"role": "user",
             "content": f"The company offers {product_description} in the {sector} sector. "
                        f"Based on the general considerations: {general_information}, what would you as {self.name} ask to understand the potential and viability of the business better? "
                        f"Just ask one question and don't try to explain why you asked that question. Only the question should be asked."}
    ]

        reasoning_response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=reasoning_prompt,
            max_tokens=150,
            temperature=0.6,
            stop=["\n"]
        )

        if reasoning_response.choices:
            return reasoning_response.choices[0].message.content.strip()
        else:
            return "Could not generate a question, please try again."

    def make_offer(self, product_description, valuation, asking_amount):
        # Step 1: Abstraktion - Allgemeine Step-Back-Frage
        abstraction_prompt = [
            {"role": "system",
             "content": f"{self.name} is known for their {self.personality} and expertise in {self.expertise}."},
            {"role": "user",
             "content": f"The company offers {product_description} and is valued at ${valuation}. "
                        f"What are the general considerations for evaluating the investment potential in this sector?"}
        ]

        abstraction_response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=abstraction_prompt,
            max_tokens=150,
            temperature=0.7,
            stop=["\n"]
        )

        general_information = abstraction_response.choices[0].message.content.strip()

        # Step 2: Reasoning - Originalfrage mit allgemeiner Information
        reasoning_prompt = [
            {"role": "system",
             "content": f"{self.name} is known for their {self.personality} and expertise in {self.expertise}. They are considering an investment. "
                        f"A decision must be made. If the decision is negative, it must be explained in one sentence. "
                        f"If they decide to invest, they must state how much they will invest and for what percentage of the company. "
                        f"They also have the option to accept the candidate's offer."},
            {"role": "user",
             "content": f"The company is valued at ${valuation} and is asking ${asking_amount} for equity. {self.name}, what's your decision?"}
        ]

        reasoning_response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=reasoning_prompt,
            max_tokens=150,
            temperature=0.7,
            stop=["\n"]
        )

        if reasoning_response.choices:
            return reasoning_response.choices[0].message.content.strip()
        else:
            return "Unable to make a decision, please try again."
