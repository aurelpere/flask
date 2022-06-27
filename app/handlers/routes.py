from flask import request, make_response
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import io

matplotlib.use('Agg')  #to avoid gui

n_sent = 100
n_yes = 0
n_no = 0
n_rep = 0


# GET requests will be blocked
#http://localhost:5000/?answeryes=1&answerno=0
def create_dataframe(yes, no, rep, sent):
    df = pd.DataFrame({
        'oui': [yes],
        'non': [no],
        'reponses': [rep],
        'envois': [sent]
    })
    return df


def configure_routes(app):

    @app.route('/')
    def get_answers():
        # pylint: disable=global-statement
        global n_yes
        global n_no
        global n_rep
        answeryes = request.args.get('answeryes')
        answerno = request.args.get('answerno')
        if (answeryes == "1" and answerno == "0") or (answeryes == "0"
                                                      and answerno == "1"):
            n_rep += int(answeryes) + int(answerno)
            n_yes += int(answeryes)
            n_no += int(answerno)
            return f"Merci d'avoir participé à ce sondage. Resultats: reponses:{n_rep} oui:{n_yes} non:{n_no}"
        else:
            return "Désolé, il y a eu un soucis avec votre requete."

    @app.route('/results.png')
    def get_result():
        df = create_dataframe(n_yes, n_no, n_rep, n_sent)
        snsplot = sns.barplot(data=df)
        fig = snsplot.get_figure()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.savefig('media/results.png')
        buffer.seek(0)
        response = make_response(buffer.getvalue())
        response.mimetype = "image/png"
        return response
