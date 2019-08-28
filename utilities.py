import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.api import search
from models import User, Tweet


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


_TWEET_INDEX = 'search_tweet'
_USERNAME_INDEX = 'search_username'


def render_page(self, template_link, template_values):
    template = JINJA_ENVIRONMENT.get_template(template_link)
    self.response.write(template.render(template_values))


def tokenize_text(query_string):
    a = []
    for word in query_string.split():
        j = 1
        while True:
            for i in range(len(word) - j + 1):
                a.append(word[i:i + j])
            if j == len(word):
                break
            j += 1
    return a


def add_document_to_search_tweet_index(tweet):
    index = search.Index(_TWEET_INDEX)
    tweet_text = ','.join(tokenize_text(tweet.tweet_text))
    tweet_key_safe = tweet.key.urlsafe()
    document = search.Document(
        doc_id=tweet_key_safe,
        fields=[
            search.TextField(name='tweet', value=tweet_text)
        ]
    )
    index.put(document)


def add_document_to_search_username_index(user):
    index = search.Index(_USERNAME_INDEX)
    username_text = ','.join(tokenize_text(user.username))
    username_key_safe = user.key.urlsafe()
    document = search.Document(
        doc_id=username_key_safe,
        fields=[
            search.TextField(name='username', value=username_text)
        ]
    )
    index.put(document)


def process_search(search_type, query_text):
    if search_type == 'username':
        index = search.Index(_USERNAME_INDEX)
        query_string = 'username:{}'.format(query_text.strip())
    else:
        index = search.Index(_TWEET_INDEX)
        query_string = 'tweet:{}'.format(query_text.strip())
    try:
        compiled_query = search.Query(
            query_string=query_string,
            options=search.QueryOptions(
                limit=100,
            )
        )
        results = index.search(compiled_query).results
    except search.Error:
        results = None
    return results


def get_search_model_keys(search_results):
    model_keys = [
        ndb.Key(urlsafe=document.doc_id)
        for document
        in search_results
    ]

    return model_keys


def clear_db():
    ndb.delete_multi(
        User.query().fetch(keys_only=True)
    )
    ndb.delete_multi(
        Tweet.query().fetch(keys_only=True)
    )


def clear_index(index_name):
    index = search.Index(index_name)
    while True:
        # Use ids_only to get the list of document IDs in the index without
        # the overhead of getting the entire document.
        document_ids = [
            document.doc_id
            for document
            in index.get_range(ids_only=True)]

        # If no IDs were returned, we've deleted everything.
        if not document_ids:
            break

        # Delete the documents for the given IDs
        index.delete(document_ids)

    # delete the index schema
    index.delete_schema()
