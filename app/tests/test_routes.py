from flask import Flask
import os.path
import datetime
from app.handlers.routes import configure_routes
from app.handlers.routes import create_dataframe


def test_get_answers_root():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/'

    response = client.get(url)
    assert response.get_data(
    ) == b'D\xc3\xa9sol\xc3\xa9, il y a eu un soucis avec votre requete.'
    assert response.status_code == 200


#http://localhost:5000/?answeryes=1&answerno=0


def test_get_answers_yes():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/?answeryes=1&answerno=0'

    response = client.get(url)
    assert response.get_data(
    ) == b"Merci d'avoir particip\xc3\xa9 \xc3\xa0 ce sondage. Resultats: reponses:1 oui:1 non:0"
    assert response.status_code == 200


    # answeryes= request.args.get('answeryes')
    # answerno=request.args.get('answerno')
    # hash=request.args.get('hash')
    # if (answeryes=="1" and answerno=="0") or (answeryes=="0" and answerno=="1"):
    #         n_rep+=int(answeryes)+int(answerno)
    #         n_yes+=int(answeryes)
    #         n_no+=int(answerno)
    #         return "Merci d'avoir participé à ce sondage"
    # else:
    #     return "Désolé, il y a eu un soucis avec votre requete."
def test_get_answers_no():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/?answeryes=0&answerno=1'

    response = client.get(url)
    assert response.get_data(
    ) == b"Merci d'avoir particip\xc3\xa9 \xc3\xa0 ce sondage. Resultats: reponses:2 oui:1 non:1"
    assert response.status_code == 200


def test_get_answers_wronginput():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/?answeryes=1&answerno=1'

    response = client.get(url)
    assert response.get_data(
    ) == b'D\xc3\xa9sol\xc3\xa9, il y a eu un soucis avec votre requete.'
    assert response.status_code == 200


def test_dataframe():
    df = create_dataframe(1, 0, 1, 100)
    assert df.loc[0, 'oui'] == 1
    assert df.loc[0, 'non'] == 0
    assert df.loc[0, 'reponses'] == 1
    assert df.loc[0, 'envois'] == 100


def test_result():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/results.png'

    response = client.get(url)
    assert response.status_code == 200
    assert os.path.exists('media/results.png')
    file_timestamp = os.path.getmtime('media/results.png')
    now_timestamp = datetime.datetime.timestamp(datetime.datetime.now())
    assert now_timestamp - file_timestamp < 1
