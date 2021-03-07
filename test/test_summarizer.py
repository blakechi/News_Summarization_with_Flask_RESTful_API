"""
    Reference from:
        https://levelup.gitconnected.com/simple-api-using-flask-bc1b7486af88
        https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html
        https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask
"""

import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), "src"))

import requests
import asyncio
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

from server_com import ServerCom


REST_API_URL = "http://localhost:5000/summarize"


async def query_data(url, gql_query):
    transport = AIOHTTPTransport(url=url)

    async with Client(
        transport=transport, fetch_schema_from_transport=True,
    ) as session:

        # Execute single query
        query = gql(gql_query)
        result = await session.execute(query)

        return result


if __name__ == "__main__":
    server_com = ServerCom()

    # Use your own query instead
    gql_query = """
        query getArticles {
            Article(order_by: {timestamp: asc}, where: {timestamp: {_gte: "2020-02-01T00:00:00", _lte: "2020-02-01T12:00:00"}}) {
                timestamp
                journal
                id
                headline
                content
            }
        }
    """
    result = asyncio.run(query_data(server_com.url, gql_query))

    news = result['Article'][1]
    payload = {
        # news' id
        "id": news["id"],
        # a string of the news
        "content": " ".join([news['content'], news['content'], news['content']])  # let it suspass the maximum length a Pegasus can accept
    }

    r = requests.post(REST_API_URL, json=payload).json()

    if r["success"]:
        print(r["summary"])
    else:
        print("Request failed")