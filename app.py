import streamlit as st
import numpy as np
from pandas import DataFrame
from keybert import KeyBERT
from keyphrase_vectorizers import KeyphraseCountVectorizer


# For Flair (Keybert)
from flair.embeddings import TransformerDocumentEmbeddings
import seaborn as sns

# For download buttons
from functionforDownloadButtons import download_button
import os
import json

list_keywords = ['climate','environment','waste','renewable','water', 'carbon',
           'strategy','scope','emission','ghg', 'co2',
           'greenhouse','target', 'environment', 
            
            'board overs','board overs', 'committ',
            
            
            'climate','environment','waste','natural resource','water'
            
            'flood','warm','wind','flood','fuel','disaster', 'warm', 'hurricane', 'heat','solar', 'coal',
            'catastroph', 
            
            'power','electric','green','energy','air',
            'catastroph','physical','transition','solar','coal','net-zero','net zero', 'catastroph',
            'hurricane','terrorism','storm','tornado','severe','weather','IPCC','warm','land','ocean'
            
            'ghg', 'emission', 'greenhouse', 'co2', 'scope 1', 'scope 2', 'scope 3', 'carbon',
            
            'reduc','reduction', 'science', 'Paris Agreement', 'net-zero','net zero', 'committ'
           ]

# set page title and icon
st.set_page_config(
    page_title="BERT Keyword Extractor",
    # page_icon="🎈",
)

# set app layout width
def _max_width_():
    max_width_str = f"max-width: 1400px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )


_max_width_()





with st.expander("About this app", expanded=True):

    st.write(
        """
	Includes example article from https://investor.travelers.com/newsroom/newsroom-overview/default.aspx. Please change the text for more example outputs.
	    """
    )

    st.markdown("")



st.markdown("## ** Paste document **")


with st.form(key="my_form"):

    ce, c1, ce, c2, c3 = st.columns([0.07, 1, 0.07, 5, 0.07])
    with c1:
        # Model type
        ModelType = st.radio(
            "Choose your model",
            ["Custom Model", "Default"],
            # help="At present, you can choose between 2 models (Flair or DistilBERT) to embed your text. More to come!",
        )

        if ModelType == "Default (Our BERT Model)":

            @st.cache(allow_output_mutation=True)
            def load_model():
                return KeyBERT("sentence-transformers/all-MiniLM-L6-v2")
                # return KeyBERT(model=roberta)

            kw_model = load_model()

        else:

            @st.cache(allow_output_mutation=True)
            def load_model():
                return KeyBERT("sentence-transformers/all-MiniLM-L6-v2")
                # return KeyBERT("distilbert-base-nli-mean-tokens")

            kw_model = load_model()

        top_N = st.slider(
            "# of results",
            min_value=1,
            max_value=30,
            value=30,
            help="You can choose the number of keywords/keyphrases to display. Between 1 and 30, default number is 30.",
        )
        min_Ngrams = st.number_input(
            "Minimum Ngram",
            min_value=1,
            max_value=4,
            help="""The minimum value for the ngram range.

*Keyphrase_ngram_range* sets the length of the resulting keywords/keyphrases.

To extract keyphrases, simply set *keyphrase_ngram_range* to (1, 2) or higher depending on the number of words you would like in the resulting keyphrases.""",
        )

        max_Ngrams = st.number_input(
            "Maximum Ngram",
            value=2,
            min_value=1,
            max_value=4,
            help="""The maximum value for the keyphrase_ngram_range.

*Keyphrase_ngram_range* sets the length of the resulting keywords/keyphrases.

To extract keyphrases, simply set *keyphrase_ngram_range* to (1, 2) or higher depending on the number of words you would like in the resulting keyphrases.""",
        )

        StopWordsCheckbox = st.checkbox(
            "Remove stop words",  value=True,
            help="Tick this box to remove stop words from the document (currently English only)",
        )

        use_MMR = st.checkbox(
            "Use MMR",
            value=True,
            help="You can use Maximal Margin Relevance (MMR) to diversify the results. It creates keywords/keyphrases based on cosine similarity. Try high/low 'Diversity' settings below for interesting variations.",
        )

        Diversity = st.slider(
            "Keyword diversity (MMR only)",
            value=0.5,
            min_value=0.0,
            max_value=1.0,
            step=0.1,
            help="""The higher the setting, the more diverse the keywords.
            
Note that the *Keyword diversity* slider only works if the *MMR* checkbox is ticked.

""",
        )
	
#     data="""
# 	The Company also considers climate change risks in making investment decisions to acquire and develop properties.  As part of our proactive measures to increase awareness and preparedness for the potential future impact from climate change, the Company completed resilience assessments of our Boston portfolio and our Los Angeles portfolio.  Through these assessments, we have developed a strategy and methodology for assessing climate resilience that will be expanded in 2022 to our full portfolio and potential investment opportunities.  In addition, the Company partners with cities and local governments, through organizations like the Boston Green Ribbon Commission, to develop climate resilience plans and strategies for fighting climate change.  We aim to make climate resilience a key driver in our overall business strategy in order to mitigate risks and identify long-term value creation opportunities. 
# 	Through this screening process, we weigh several sustainability characteristics that contribute to long-term value and resilience.  We conduct energy audits and identify potential opportunities to increase efficiency in building systems.  This includes considering LEED status, on-site clean and renewable energy, energy intensity, benchmarking our energy use and scanning for lighting retrofits and central system controls.  We also consider physical risks such as the potential for flooding, wildfires and environmental hazards and conduct a Phase I Environmental Site Assessment on all new acquisitions. 
# 	2 Equity Residential used the Intergovernmental Panel on Climate Change (IPCC) Representative Concentration Pathway (RCP) 4. 5 and a “businesses-as usual” scenario of RCP 8. 5 as the two scenarios to assess impacts and selected medium- and longer-term timeframes of 2030 and 2050 based on the types of expected hazards and regulatory frameworks impacting the Boston area. 
# 	Environment—Climate Strategy and Portfolio Resilience;Sustainable Buildings;Energy and Emissions Describe the resilience of the organizations strategy, taking into consideration different climate-related scenarios, including a 2°C or lower scenario.
# 		""",
    
#     data = """
# 	The Company also considers climate change risks in making investment decisions to acquire and develop properties.  As part of our proactive measures to increase awareness and preparedness for the potential future impact from climate change, the Company completed resilience assessments of our Boston portfolio and our Los Angeles portfolio.  Through these assessments, we have developed a strategy and methodology for assessing climate resilience that will be expanded in 2022 to our full portfolio and potential investment opportunities.  In addition, the Company partners with cities and local governments, through organizations like the Boston Green Ribbon Commission, to develop climate resilience plans and strategies for fighting climate change.  We aim to make climate resilience a key driver in our overall business strategy in order to mitigate risks and identify long-term value creation opportunities. 
# # 	Through this screening process, we weigh several sustainability characteristics that contribute to long-term value and resilience.  We conduct energy audits and identify potential opportunities to increase efficiency in building systems.  This includes considering LEED status, on-site clean and renewable energy, energy intensity, benchmarking our energy use and scanning for lighting retrofits and central system controls.  We also consider physical risks such as the potential for flooding, wildfires and environmental hazards and conduct a Phase I Environmental Site Assessment on all new acquisitions. 
# # 	2 Equity Residential used the Intergovernmental Panel on Climate Change (IPCC) Representative Concentration Pathway (RCP) 4. 5 and a “businesses-as usual” scenario of RCP 8. 5 as the two scenarios to assess impacts and selected medium- and longer-term timeframes of 2030 and 2050 based on the types of expected hazards and regulatory frameworks impacting the Boston area. 
# # 	Environment—Climate Strategy and Portfolio Resilience;Sustainable Buildings;Energy and Emissions Describe the resilience of the organizations strategy, taking into consideration different climate-related scenarios, including a 2°C or lower scenario.     """,


    data=""" The Travelers Companies, Inc. (NYSE: TRV) today published its 2021 Sustainability Report, which outlines the company’s comprehensive strategy for creating shareholder value over time, as well as its ongoing environmental, social and governance (ESG) initiatives.
“Our long-term success is tied to our ability to execute in the marketplace while upholding the promise we made to be there for our customers, communities and employees,” said Yafit Cohn, Chief Sustainability Officer at Travelers. “This year’s sustainability report details that approach and highlights how our ESG initiatives are integrated throughout everything we do.”
The report provides an in-depth review of the 16 topics the company has identified as its key drivers of sustained value: Business Strategy & Competitive Advantages, Capital & Risk Management, Climate Strategy, Community, Customer Experience, Data Privacy & Cybersecurity, Disaster Preparedness & Response, Diversity & Inclusion, Eco-Efficient Operations, Ethics & Values, Governance Practices, Human Capital Management, Innovation, Investment Management, Public Policy and Safety & Health.
Highlights from the company’s 2021 report include:

Climate Strategy

    Over the past three years, the company’s Global Renewable Energy Practice grew at a compound annual rate of 30%, with revenue up more than 120% since 2018.

Community

    Travelers and the Travelers Foundation have contributed more than $228 million to nonprofits over the past decade to support academic and career success, develop thriving neighborhoods and create culturally enriched communities.

Customer Experience

    The company resolved more than 90% of property claims arising out of catastrophe events within 30 days. This result was achieved while responding to a historically high number of catastrophe events in 2021.

Diversity & Inclusion

    In each of the last 10 years, Travelers has increased the percentage of people of color in its U.S. workforce while increasing the percentage of both women and people of color in U.S. management-level positions.

Eco-Efficient Operations

    Over the past decade, the company reduced its Scope 1 and Scope 2 emissions by 60%, and in 2021, Travelers announced its commitment to become carbon neutral across its owned operations by 2030.

Human Capital Management

    Continuing to focus on the health and wellness of its employees, Travelers introduced a new benefit – Caregiving Support from Wellthy – to help employees navigate challenges they may face as caregivers for children, aging family members or loved ones with special needs or who are chronically ill.

Investment Management

    Many of the company’s investments enable environmental and social improvements, including water and sewer projects ($6 billion), K-12 education ($10.8 billion) and higher education ($5 billion). Travelers also owns nearly $2.4 billion in fixed income securities classified as “green bonds” by Bloomberg.

Public Policy

    Throughout 2020 and 2021, the Travelers Institute hosted 45 virtual events to help consumers and business leaders navigate through uncertain times. The programs, which explored topics like cybersecurity, distracted driving and natural disasters, garnered nearly 100,000 views.

The company’s sustainability reporting is guided by multiple sustainability disclosure frameworks, as well as engagements with key stakeholders from both inside and outside the company. Travelers is a leader among domestic property casualty insurance companies in publishing reports responsive to the Sustainability Accounting Standards Board (SASB) standards for the insurance industry and the recommendations of the Task Force on Climate-related Financial Disclosures (TCFD). 
""",
	

    with c2:
        data = st.text_area(
            "Paste your text below (max 1000 words)",value="\n".join(data),
            height=510,
        )

        MAX_WORDS = 1000

        import re

        res = len(re.findall(r"\w+", data))
        if res > MAX_WORDS:
            st.warning(
                "⚠️ Your text contains "
                + str(res)
                + " words."
                + " Only the first 500 words will be reviewed"
            )

            data = data[:MAX_WORDS]

        submit_button = st.form_submit_button(label="Get me the data!")

    if use_MMR:
        mmr = True
    else:
        mmr = False

    if StopWordsCheckbox:
        StopWords = "english"
    else:
        StopWords = None

if not submit_button:
    st.stop()

if min_Ngrams > max_Ngrams:
    st.warning("min_Ngrams can't be greater than max_Ngrams")
    st.stop()

keywords = kw_model.extract_keywords(
    data,
    keyphrase_ngram_range=(min_Ngrams, max_Ngrams),
    use_mmr=mmr,
    stop_words=StopWords,
    top_n=top_N,
    diversity=Diversity,
    vectorizer=KeyphraseCountVectorizer()
)

st.markdown("## ** Check & download results **")

st.header("")

cs, c1, c2, c3, cLast = st.columns([2, 1.5, 1.5, 1.5, 2])

with c1:
    CSVButton2 = download_button(keywords, "Data.csv", "🎁 Download (.csv)")
with c2:
    CSVButton2 = download_button(keywords, "Data.txt", "🎁 Download (.txt)")
with c3:
    CSVButton2 = download_button(keywords, "Data.json", "🎁 Download (.json)")

st.header("")

df = (
    DataFrame(keywords, columns=["Keyword/Keyphrase", "Relevancy"])
    .sort_values(by="Relevancy", ascending=False)
    .reset_index(drop=True)
)

df=df[df['Keyword/Keyphrase'].str.contains('|'.join(list_keywords))]

df.index += 1


# Add Styling to the table columns and rows

cmGreen = sns.light_palette("green", as_cmap=True)
cmRed = sns.light_palette("red", as_cmap=True)
df = df.style.background_gradient(
    cmap=cmGreen,
    subset=[
        "Relevancy",
    ],
)

c1, c2, c3 = st.columns([1, 3, 1])

format_dictionary = {
    "Relevancy": "{:.1%}",
}

df = df.format(format_dictionary)

with c2:
    st.table(df)
