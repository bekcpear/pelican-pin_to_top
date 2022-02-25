"""
Pin to top plugin for Pelican
================================

Adds .pin variable to article's context and pins the article to the top
 even if it is older than the other articles
"""
from pelican import signals
from datetime import datetime
from zoneinfo import ZoneInfo

def update_pinned_articles(generator):
    new_order = []

    # pin articles by slug in the setting PIN_TO_TOP with the list's order
    pin_articles = {}
    pin_articles_slugs = generator.settings.get('PIN_TO_TOP')

    last_modified_date = 0

    for article in generator.articles:

        # get the last modified date of all articles
        try:
            if article.modified.timestamp() > last_modified_date:
                last_modified_date = article.modified.timestamp()
        except:
            if article.date.timestamp() > last_modified_date:
                last_modified_date = article.date.timestamp()

        # pin articles
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
    # add a new global item
    generator.context['last_modified_date_of_all'] = datetime\
            .fromtimestamp(last_modified_date, \
                    ZoneInfo(generator.settings.get('TIMEZONE')))#\
            #.strftime('%Y-%m-%d %H:%M %Z')

def register():
    signals.article_generator_finalized.connect(update_pinned_articles)
