import streamlit as st
from textblob import TextBlob
import pandas as pd
import emoji
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import textblob.download_corpora

textblob.download_corpora.download_all()

st.set_page_config(page_title="Sentiment Analysis Web App",layout="centered")
@st.cache_data
def get_text(raw_url):
    req = Request(raw_url, headers={'User-Agent': 'Mozilla/5.0'})
    page=urlopen(req)
    soup=BeautifulSoup(page,'html.parser')
    fetched_text=" ".join(map(lambda p:p.text,soup.find_all('p')))
    return fetched_text

def main():
    """Sentiment Analysis Emoji App"""
    st.title("Sentiment Analysis Web App using NLP and ML! ")
    activities=["Sentiment","Text Analysis on URL","About"]
    choice=st.sidebar.selectbox("Choose Activity",activities)
    if choice=='Sentiment':
        st.subheader("Sentiment Analysis")
        raw_Text=st.text_area("Enter your Text","Type here....")
        if st.button("Analyze"):
            blob=TextBlob(raw_Text)
            result=blob.sentiment.polarity

            if result>0.0:
                custom_emoji=emoji.emojize(":smile:",language="alias")
            elif result<0.0:
                custom_emoji=emoji.emojize(":disappointed:",language="alias")
            else:
                custom_emoji=emoji.emojize(":neutral_face:",language="alias")
            st.write(custom_emoji)
            st.success(f" Polarity Score: {result}")
            
    elif choice=="Text Analysis on URL":
        st.subheader("Text Analysis from a Web URL")
        raw_url=st.text_input("Enter a URL","https://en.wikipedia.org/wiki/Natural_language_processing")
        text_preview_length=st.slider("Length to Preview",50,500)
        if st.button("Submit"):
            if raw_url:
                result=get_text(raw_url)
                blob=TextBlob(result)
                len_of_full_text=len(result)
                len_of_short_text=round(len(result)/text_preview_length)

                st.success(f"Length of Full Text:{len_of_full_text}") 
                st.success(f"Length of Short Text:{len_of_short_text}")
                st.info(result[:len_of_short_text])

                c_sentences=[str(sent) for sent in blob.sentences] 
                c_sentiment=[sent.sentiment.polarity for sent in blob.sentences]

                new_df=pd.DataFrame(zip(c_sentences,c_sentiment),columns=['Sentences','Sentiments'])
                st.dataframe(new_df)     

        else:
            st.subheader("About This App")
            st.info("this is a sentiment analysis web app that has been made using NLP and ML.We return the sentiment , emoji of the given text. We also perform web scraping to understand and analyse text of website. This is an interactive app . Enjoy !!!")

   
if __name__=="__main__":
    main()
