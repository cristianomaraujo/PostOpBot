import streamlit as st
import openai
from streamlit_chat import message as msg

import os

SENHA_OPEN_AI = os.getenv("SENHA_OPEN_AI")

openai.api_key = SENHA_OPEN_AI

# URL da imagem do logo no repositório do GitHub
logo_url = "https://github.com/cristianomaraujo/PostOpBot/blob/main/eng.jpg?raw=true"
logo_url3 = "https://github.com/cristianomaraujo/PostOpBot/blob/main/capa3.jpg?raw=true"

# Exibindo a imagem de logo na barra lateral
st.sidebar.image(logo_url3, use_column_width=True, width=800)
# Exibindo a imagem de logo central
st.image(logo_url, use_column_width=True, width=800)

# Texto de abertura
abertura = st.write("Hello! I'm PostOpBot, an AI-powered chatbot here to assist you with post-operative care following dental extraction surgery. To begin our conversation, simply type 'hello' in your native language (for example: Hi, Oi, Holá, Salut, Hallo, 你好, привет) or enter any questions you have about your recovery in the field below.")

# Título da barra lateral
st.sidebar.title("References")

# Campo de entrada de texto central
text_input_center = st.chat_input("Chat with me by typing in the field below")

condicoes = (
    "Your name is PostOpBot and you are programmed to provide guidance only for dental extractions. For other cases, inform that you are not programmed for that."
    "Act as a chatbot, initiating the conversation with just one question, and ask for the user's name to make the conversation more personalized."
    "Do not prescribe anything that is not based on the recommendations below. Whenever necessary, respond that a dentist should be consulted."
    "Lead the conversation as if you were a healthcare professional, providing guidance to the patient on how to proceed after dental extraction surgery."
    "Be interactive, conducting the conversation with questions and answers, rather than just passing on all the guidance at once."
    "Provide guidance one at a time, asking questions about the topic before giving the information (for example: When discussing not smoking, ask if the patient is a smoker first)."
    "In cases of dental extraction, the following recommendations should be given throughout the conversation:"
    "Apply a folded gauze for 30 minutes after the tooth extraction."
    "Avoid spitting for the first 24 hours."
    "Avoid rinsing (gargling) with any liquids for the first 24 hours."
    "Avoid suction. Do not use straws."
    "Consume a soft or semi-liquid diet, opting for foods at a low or moderate temperature."
    "You may apply ice wrapped in cloth to the outer part of the face where the extraction was performed for the first 24 hours."
    "Maintain proper oral hygiene (clean the surgical site very gently)."
    "Avoid smoking postoperatively (7 days after surgery) and refrain from consuming alcoholic beverages during the following week."
    "Avoid carbonated drinks."
    "Take antibiotics, pain relievers, and anti-inflammatories according to the surgeon's recommendations (pay attention to the prescription for each medication and observe the indicated times)."
    "Do warm water rinses after 48 hours of extraction. Avoid vigorous rinsing."
    "Use 0.12% chlorhexidine mouthwash starting from 24 hours (3 times a day / 10 days) from the day after surgery, as directed by your dentist."
    "Perform mouth opening exercises after 48 hours of extraction."
    "Avoid physical activities or intense activities for 7 days."
    "Be as informative as possible."
    "Whenever the user requests any inquiries outside the protocol, remind them that you are just a virtual assistant, and that a dentist should be consulted."
    "Reply to the user based on the language the conversation started, creating communication in the user's native language."
    "Do not discuss anything unrelated to your main objective. Whenever the user asks for something outside the scope, respond that you are not programmed for that."
)

st.sidebar.markdown(
    """
    <style>
    .footer {
        font-size: 12px;
        text-align: justify;
    }
    </style>
    <div class="footer">1) Aloy-Prósper, A., Pellicer-Chover, H., Balaguer-Martínez, J., Llamas-Monteagudo, O., & Peñarrocha-Diago, M. (2020). Patient compliance to postoperative instructions after third molar surgery comparing traditional verbally and written form versus the effect of a postoperative phone call follow-up a: a randomized clinical study. Journal of Clinical and Experimental Dentistry, 12(10), e909.<br></div>
    <div class="footer">2) Alvira-González, J., & Gay-Escoda, C. (2015). Compliance of postoperative instructions following the surgical extraction of impacted lower third molars: a randomized clinical trial. Medicina Oral, Patología Oral y Cirugía Bucal, 20(2), e224.</div>
    <div class="footer">3) Shenoi, R. S., Rajguru, J. G., Parate, S. R., Ingole, P. D., Khandaitkar, S. R., & Karmarkar, J. S. (2021). Compliance of postoperative instructions following the surgical extraction of impacted lower third molars. Indian Journal of Dental Research, 32(1), 87-91.<br><br><br><br></div>
    <div class="footer"><b>PostOpBot may make mistakes. Always remember to verify all information with your dental surgeon.</b></div>
    """,
    unsafe_allow_html=True
)

# Criação da função para renderizar a conversa com barra de rolagem
def render_chat(hst_conversa):
    for i in range(1, len(hst_conversa)):
        if i % 2 == 0:
            msg("**PostOpBot**:" + hst_conversa[i]['content'], key=f"bot_msg_{i}")
        else:
            msg("**You**:" + hst_conversa[i]['content'], is_user=True, key=f"user_msg_{i}")

    # Código para a barra de rolagem
    st.session_state['rendered'] = True
    if st.session_state['rendered']:
        script = """
        const chatElement = document.querySelector('.streamlit-chat');
        chatElement.scrollTop = chatElement.scrollHeight;
        """
        st.session_state['rendered'] = False
        st.write('<script>{}</script>'.format(script), unsafe_allow_html=True)

st.write("***")

if 'hst_conversa' not in st.session_state:
    st.session_state.hst_conversa = [{"role": "user", "content": condicoes}]

if text_input_center:
    st.session_state.hst_conversa.append({"role": "user", "content": text_input_center})
    retorno_openai = openai.ChatCompletion.create(
        model="gpt-4o-2024-08-06",
        messages=st.session_state.hst_conversa,
        max_tokens=500,
        n=1
    )
    st.session_state.hst_conversa.append({"role": "assistant", "content": retorno_openai['choices'][0]['message']['content']})

# RENDERIZAÇÃO DA CONVERSA
if len(st.session_state.hst_conversa) > 1:
    render_chat(st.session_state.hst_conversa)
