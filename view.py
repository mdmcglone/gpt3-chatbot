from flask import Flask, render_template
from flask_restful import Api, Resource
from flask_cors import CORS
import os
import openai

# Initialize Flask app
app = Flask(__name__)
api = Api(app)

# Enable CORS -> Cross Origin Resource Sharing -> Allow requests from other domains, importantly for frontend javascript
CORS(app)


#decorator function that specifies the url suffix
@app.route('/')
def home():
    return render_template('index.html')
#renders basic html landing page

#Restful API endpoint
class chatbot(Resource):
    #query is now usable variable from url suffix
    def get(self, query):
        #prefix is the prompt for the GPT-3 model, which has the query appended to it
        prefix='Below this paragraph is a conversation between an experienced Indian lawyer or Indian law student and an AI chatbot research assistant designed to answer question regarding Indian laws and court cases. The chatbot answers the question based exclusively on its knowledge of Indian legal precedent, Indian legislation, and Indian legal procedure. The chatbot is designed to optimize for being as accurate, informative, and professional as possible. When the chatbot answers, it provides proof or sources for its answers with citations of Indian precedents, Indian legislation, and Indian regulatory procedure. The chatbot will typically cite at least one case law (or legal precedent) from the Supreme Court of India or any of the High Courts of the states of India, and it will try to cite one central or state act (or legislation).  Try to continue the conversation and answer the question, but if you cannot find well-cited, accurate information, say "Sorry, I cannot help with that."\n\nLawyer or Law Student: "Are women always allowed to enter temples?"\nAI Chatbot: "In 2018, a Constitution Bench of the Supreme Court allowed the entry of women irrespective of age into the Sabarimala Temple on the grounds that the ban violated the fundamental right of freedom of religion as per Article 25 of the Constitution. Rule 3(b) of the Kerala Hindu Places of Public Worship Rules, 1965, the provision restricting entry of women in the state legislation was struck down and deemed unconstitutional. [Precedents: Indian Young Lawyers Association & Ors. vs. The State of Kerala & Ors [2018]; Acts: Article 25 (Clause 1), the Constitution of India. Rule 3(b), Kerala Hindu Places of Public Worship Rules [1965]]"\n\nLawyer or Law Student: "What was a relevant quote from the verdict in Indian Young Lawyers Association vs. The State of Kerala?"\nAI Chatbot: "The Court stated: "We have no hesitation in saying that such an exclusionary practice violates the right of [a woman] to visit and enter a temple, to freely practise Hindu religion and to exhibit her devotion towards Lord Ayyappa. The denial of this right to women significantly denudes them of their right to worship." [Precedents: Indian Young Lawyers Association & Ors. vs. The State of Kerala & Ors [2018]; Acts: Article 25 (Clause 1), the Constitution of India. Rule 3(b), Kerala Hindu Places of Public Worship Rules [1965]]"\n\nLawyer or Law Student: "Can spouse of deceased in accident caused by heart attack claim life insurance for the accident?"\nAI Chatbot: "In Smt. Alka Shukla vs Life Insurance Corporation of India, the Supreme Court held that only if both were affirmed that (i) the assured’s death was due to a bodily injury resulting from an accident caused by outward, violent and visible means, and (ii) the injury was proximately caused by the accident, the complainant would be entitled to claim under their policy. And in the absence of a post-mortem, the medical report that the insured suffered from an acute myocardial infraction while driving, the proximate cause of death was not the accident. [Precedents: Smt. Alka Shukla vs Life Insurance Corporation of India [2018], Union of India v Sunil Kumar Ghosh [1984]; Acts: Consumer Protection Act of India [1986]]"\n\nLawyer or Law Student: "Can schools be forced to give marksheets to students when they passed students without awarding them marks during the COVID lockdown period?"\nAI Chatbot: "In Nakshatra Bind A.K. vs The State Of Tamilnadu, the High Court of Madras rejected a plea from a State Board student to quash the Government Order requiring schools to pass all students without awarding them marks in order to be able to furnish marksheets needed to transfer to a school in the state of Kerala. [Precedents: Nakshatra Bind A.K. vs The State Of Tamilnadu [2021]; Acts: ]"\n\nLawyer or Law Student: "What is the weather like today?"\nAI Chatbot: "Sorry, I cannot help with that."\n\nLawyer or Law Student: "Can Hindu couples receive divorce before the minimum stipulated marriage period of 6 months ends?"\nAI Chatbot: "In Amardeep Singh vs. Harveen Kaur, the Supreme Court held that if there is no chance for a peaceful solution to restore cohabitation or any other alternative left, the court may go for an immediate solution, ignoring the provision of a minimum period of six months stipulated under Section 13B(2) of the Hindu Marriage Act, 1955. [Precedents: Amardeep Singh v. Harveen Kaur [2017]; Acts: Hindu Marriage Act of India [2955]]" \n\nLawyer or Law Student: "What are the Arnesh Kumar Guidelines?"\nAI Chatbot: "The Arnesh Kumar Guidelines are a set of Supreme Court of India guidelines that lay down the parameters within which an arrest can be made by the police. The guidelines were formulated in the case of Arnesh Kumar vs. State of Bihar, in which the Court held that the police must ensure that an arrest is not made merely on the basis of an accusation or an offence, but only after taking into account various factors such as the severity of the offence, the need to prevent further offences, etc. [Precedents: Arnesh Kumar vs. State of Bihar [2014]; Acts: Section 41, Code of Criminal Procedure of India (CrPC) [1973]]"\n\nLawyer or Law Student: "'
        query = prefix + query + '\n'
        try:
            #set api key for GPT-3 model 
            api_key = f'./secrets/API_KEY'
            api_key = open(api_key, 'r').read()
            openai.api_key = api_key

            #set parameters for gpt completion and pass query to model
            gpt = openai.Completion.create(
                prompt=query,
                engine="davinci",
                temperature=0.1, 
                max_tokens=256,
                top_p = 1,
                frequency_penalty=0,
                presence_penalty=0,
                stop = ['\n\nLawyer or Law Student:']
            )
            #return the response from the model
            pred = gpt.choices[0].text
            #format the response to remove the prefix and the prompt
            out = pred.split('Chatbot: ')[1]
            return {'response': out}
        except Exception as e:
            return {'error': str(e)}

#specifices name and url suffix of Restful API endpoint
api.add_resource(chatbot, '/<string:query>')

#this is the main function that runs the app
#THIS SHOULD NOT BE DEBUG MODE IN PRODUCTION
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)


