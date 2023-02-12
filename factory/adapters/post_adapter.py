from factory.adapters.adapter import Adapter


class PostAdapter(Adapter):
    @staticmethod
    def adapt(entity: dict) -> dict: 
        mongo_query = {"$set": {}, "$unset": {}}
        if "text" in entity:
           mongo_query["$set"]["text"] = entity["text"].strip()
        if "title" in entity:
            mongo_query["$set"]["title"] = entity["title"].strip()
        update_like = [key for key in entity.keys() if key.startswith('likes.')]

        if len(update_like) == 1:
            update_like_key = update_like[0]
            update_like_value = entity[update_like_key]

            if update_like_value == True:
                mongo_query["$set"][update_like_key] = True

            if update_like_value == False:
                mongo_query["$unset"][update_like_key] = 1
            
        return mongo_query