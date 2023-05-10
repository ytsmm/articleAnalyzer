import json
import traceback
import vectorizer
import preprocessor
import pandas as pd
import clusterizator
import clusterKeywords


def getData():
    file = "data.csv"
    data = pd.read_csv(file, sep=';')
    title = data['Title'].to_numpy()
    authors = data['Authors'].to_numpy()
    doi = data['Doi'].to_numpy()
    keys = data['Keywords'].to_numpy()
    words = data[['Title', 'Keywords', 'Abstract']].agg(''.join, axis=1).to_numpy()
    return title, authors, doi, keys, words


def writeData(doi, key, title, authors, X, labels, n, clusterKeywords, weights, size):
    data = {'articles': [], 'clusters': []}
    for i in range(len(doi)):
        data['articles'].append({
            'doi': doi[i],
            'title': title[i],
            'authors': authors[i],
            'keywords': key[i],
            'axisX': str(X['X'].values[i]),
            'axisY': str(X['Y'].values[i]),
            'class': str(labels[i])
        })
    for i in range(n):
        data['clusters'].append({
            'number': i,
            'keywords': ', '.join(clusterKeywords[i]),
            'weights': weights[i],
            'quantity': size[i]
        })
    data['clusterQuantity'] = n
    with open('website/data.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)
        outfile.write('\n')
    return 1


def getVocabulary(keys, words):
    vocabulary = {}
    newKeys = keys.copy()
    for i in range(len(newKeys)):
        words[i].split(', ')
        for word in newKeys[i].split(', '):
            vocabulary[word.lower()] = word
        newKeys[i] = newKeys[i].lower().split(', ')
    return newKeys, vocabulary


def rubrication(clusterType):
    try:
        title, authors, doi, keys, words = getData()
        newKeys, vocabulary = getVocabulary(keys, words)
        keywords, model = preprocessor.preprocessor(words)
        vectors = vectorizer.vectorizeApi(keywords, model)
        labels, n, size = clusterizator.clusterization(vectors, clusterType)
        clusterKeys, weights = clusterKeywords.getKeywords(vocabulary, newKeys, labels, n)
        writeData(doi, keys, title, authors, vectors, labels, n, clusterKeys, weights, size)
        return 1
    except Exception as e:
        return traceback.format_exc()
