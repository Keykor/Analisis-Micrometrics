import json 
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from pymongo import MongoClient
from bson.json_util import dumps

def execute():
    client = MongoClient('localhost')
    db = client['metrics']
    col = db['CastWithEvents']

    # se queda con eventos input por screencast 
    pipeline = [
        {
            '$unwind': {
                'path': '$logs'
            }
        }, {
            '$match': {
                'logs.type': 'input'
            }
        }, {
            '$sort': {
                'logs.timestamp': 1
            }
        }, {
            '$group': {
                '_id': '$_id', 
                'logs': {
                    '$push': '$logs'
                }
            }
        }
    ]

    cursor = col.aggregate(pipeline, allowDiskUse=True)
    screencasts = list(cursor)

    temp_col = db['tempcol']
    temp_col.drop()

    for cast in screencasts:
        previous = cast['logs'].copy()
        previous.pop()

        next = cast['logs'].copy()
        next.pop(0)

        newLogs = []
        saveFirst = True
        for previousEvent, nextEvent in zip(previous, next):
            ratio = fuzz.ratio(previousEvent["data"]["text"], nextEvent["data"]["text"])

            if (ratio > 66):
                if (saveFirst):
                    newLogs.append(previousEvent)
                    saveFirst = False
                newLogs.append(nextEvent)
            else:
                if (not saveFirst):
                    saveFirst = True
                    obj = {
                        "type": "inputEnd",
                        "timestamp": previousEvent["timestamp"] + 1
                    }
                    newLogs.append(obj)
            
        cast['logs'] = newLogs
        temp_col.insert_one(cast)

    pipeline = [
        {
            '$addFields': {
                'nextLogs': '$logs'
            }
        }, {
            '$project': {
                'logs': {
                    '$filter': {
                        'input': '$logs', 
                        'as': 'logs', 
                        'cond': {
                            '$ne': [
                                '$$logs', {
                                    '$arrayElemAt': [
                                        '$logs', -1
                                    ]
                                }
                            ]
                        }
                    }
                }, 
                'nextLogs': {
                    '$filter': {
                        'input': '$nextLogs', 
                        'as': 'logs', 
                        'cond': {
                            '$ne': [
                                '$$logs', {
                                    '$arrayElemAt': [
                                        '$logs', 0
                                    ]
                                }
                            ]
                        }
                    }
                }
            }
        }, {
            '$project': {
                'logs': {
                    '$map': {
                        'input': {
                            '$zip': {
                                'inputs': [
                                    '$logs', '$nextLogs'
                                ]
                            }
                        }, 
                        'as': 'el', 
                        'in': {
                            'a': {
                                '$arrayElemAt': [
                                    '$$el', 0
                                ]
                            }, 
                            'b': {
                                '$arrayElemAt': [
                                    '$$el', 1
                                ]
                            }
                        }
                    }
                }
            }
        }, {
            '$unwind': {
                'path': '$logs'
            }
        }, {
            '$match': {
                '$and': [
                    {
                        'logs.a.type': 'input'
                    }, {
                        'logs.b.type': 'input'
                    }
                ]
            }
        }, {
            '$project': {
                'a': '$logs.a.data.text', 
                'b': '$logs.b.data.text', 
                'cantBorrado': {
                    '$subtract': [
                        {
                            '$strLenCP': '$logs.a.data.text'
                        }, {
                            '$strLenCP': '$logs.b.data.text'
                        }
                    ]
                }
            }
        }, {
            '$match': {
                'cantBorrado': {
                    '$gt': -1
                }
            }
        }, {
            '$group': {
                '_id': '$_id', 
                'cantBorrado': {
                    '$sum': '$cantBorrado'
                }
            }
        }, {
            '$out': 'TotalBorrado'
        }
    ]

    temp_col.aggregate(pipeline, allowDiskUse=True)

    pipeline = [
        {
            '$addFields': {
                'nextLogs': '$logs'
            }
        }, {
            '$project': {
                'logs': {
                    '$filter': {
                        'input': '$logs', 
                        'as': 'logs', 
                        'cond': {
                            '$ne': [
                                '$$logs', {
                                    '$arrayElemAt': [
                                        '$logs', -1
                                    ]
                                }
                            ]
                        }
                    }
                }, 
                'nextLogs': {
                    '$filter': {
                        'input': '$nextLogs', 
                        'as': 'logs', 
                        'cond': {
                            '$ne': [
                                '$$logs', {
                                    '$arrayElemAt': [
                                        '$logs', 0
                                    ]
                                }
                            ]
                        }
                    }
                }
            }
        }, {
            '$project': {
                'logs': {
                    '$map': {
                        'input': {
                            '$zip': {
                                'inputs': [
                                    '$logs', '$nextLogs'
                                ]
                            }
                        }, 
                        'as': 'el', 
                        'in': {
                            'a': {
                                '$arrayElemAt': [
                                    '$$el', 0
                                ]
                            }, 
                            'b': {
                                '$arrayElemAt': [
                                    '$$el', 1
                                ]
                            }
                        }
                    }
                }
            }
        }, {
            '$unwind': {
                'path': '$logs'
            }
        }, {
            '$match': {
                '$and': [
                    {
                        'logs.a.type': 'input'
                    }, {
                        'logs.b.type': 'input'
                    }
                ]
            }
        }, {
            '$project': {
                'time': {
                    '$subtract': [
                        '$logs.b.timestamp', '$logs.a.timestamp'
                    ]
                }
            }
        }, {
            '$group': {
                '_id': '$_id', 
                'avgIntratecla': {
                    '$avg': '$time'
                }
            }
        }, {
            '$out': 'AvgIntratecla'
        }
    ]

    temp_col.aggregate(pipeline, allowDiskUse=True)

    temp_col.drop()