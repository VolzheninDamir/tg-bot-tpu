import wikipedia

def search_wikipedia(query: str, language: str = 'ru') -> tuple:
    try:
        wikipedia.set_lang(language)
        search_results = wikipedia.search(query)
        
        if not search_results:
            return None, None
            
        page = wikipedia.page(search_results[0])
        return page.summary[:1500], page.url
        
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Уточните запрос. Возможные варианты:\n{', '.join(e.options[:5])}", None
    except wikipedia.exceptions.PageError:
        return "Статья не найдена.", None
    except Exception as e:
        return f"Произошла ошибка: {str(e)}", None