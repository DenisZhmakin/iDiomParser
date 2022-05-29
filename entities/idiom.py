from typing import Optional

from database import Database


class Idiom:
    def __init__(self, phrase: str, explanation: str, etymology: Optional[str] = None):
        self.phrase = phrase
        self.explanation = explanation
        self.etymology = etymology
        self.db = Database()

    def __str__(self):
        return f"""
        {self.phrase}
        {self.explanation}
        {self.etymology}
        """

    def write(self):
        idioms = self.db.idioms
        conn = self.db.engine.connect()

        conn.execute(
            idioms.insert().values(
                phrase=self.phrase,
                explanation=self.explanation,
                etymology=self.etymology
            )
        )
