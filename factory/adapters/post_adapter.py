from factory.adapters.adapter import Adapter


class PostAdapter(Adapter):
    @staticmethod
    def adapt(entity):
        entity["text"] = entity["text"].strip()
        entity["title"] = entity["title"].strip()
