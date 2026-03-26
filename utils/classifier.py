def classify_query(query):
    query = query.lower()

    if "wattmonk" in query:
        return "wattmonk"
    elif "nec" in query or "electrical" in query:
        return "nec"
    else:
        return "general"