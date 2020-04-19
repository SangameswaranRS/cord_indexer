"""
API 's for top search.
"""

from connection_handler import ConnectionHandler


# If its not run in a multi threaded environment,
# Create static instance of ContentHandler and use it.
def update_count(index, title, abstract, url):
    if not isinstance(index, str):
        print('[ERROR] Wrong type')
        return
    db = ConnectionHandler().get_connection()
    cursor = db.cursor()
    rows_affected = cursor.execute('update indexToResultCounts set count = count+1 where docId=%s', (index,))
    if rows_affected == 0:
        print('[INFO] Creating entry')
        cursor.execute("insert into indexToResultCounts values(%s, %s, %s, %s, 1);", (index, title, '<>', url))
    db.commit()
    db.close()


def top_search_impl(start=0, end=10):
    db = ConnectionHandler().get_connection()
    cursor = db.cursor()
    cursor.execute('select * from indexToResultCounts order by count desc limit %s offset %s',
                   [(end - start), start])
    results = cursor.fetchall()
    res = []
    for result in results:
        dict = {
            "paperTitle": result[1],
            "paperUrl": result[3],
            "count": result[4]
        }
        res.append(dict)
    db.close()
    return res
