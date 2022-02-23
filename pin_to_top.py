"""
Pin to top plugin for Pelican
================================

Adds .pin variable to article's context and pins the article to the top
 even if it is older than the other articles
"""
from pelican import signals

def update_pinned_articles(generator):
    new_order = []

    # pin articles by slug in the setting PIN_TO_TOP with the list's order
    pin_articles = {}
    pin_articles_slugs = generator.settings.get('PIN_TO_TOP')

    for article in generator.articles:
        pin_article = False
        for slug in pin_articles_slugs:
            if slug == article.slug:
                article.pin = True
                pin_articles[slug] = article
                pin_article = True
                break
        if not pin_article:
            new_order.append(article)

    pined = 0
    for slug in pin_articles_slugs:
        new_order.insert(pined, pin_articles[slug])
        pined += 1

    generator.articles = new_order
    # Update the context with the new list
    generator.context['articles'] = generator.articles

def register():
    signals.article_generator_finalized.connect(update_pinned_articles)
