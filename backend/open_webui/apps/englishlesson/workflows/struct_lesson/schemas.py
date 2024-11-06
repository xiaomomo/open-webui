class LessonUnit():
    """Struct the unit"""
    unit: str
    objectives: str
    lesson_story: str
    vocabulary: str
    key_sentences: str
    origin_content: str

    def __init__(self, unit, objectives, lesson_story, vocabulary, key_sentences):
        self.unit = unit
        self.objectives = objectives
        self.lesson_story = lesson_story
        self.vocabulary = vocabulary
        self.key_sentences = key_sentences
        self.origin_content = ""


    @classmethod
    def from_dict(cls, data):
        return cls(
            unit=data.get('unit', ''),
            objectives=data.get('objectives', ''),
            lesson_story=data.get('lesson_story', ''),
            vocabulary=data.get('vocabulary', ''),
            key_sentences=data.get('key_sentences', '')
        )

    def to_dict(self):
        # 将对象属性转换为字典
        return self.__dict__