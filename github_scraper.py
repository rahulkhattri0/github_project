import streamlit as st
import requests
from bs4 import BeautifulSoup
def get_url(brand):
        domain='https://github.com/'
        keyword=brand
        url=domain+keyword.replace(' ','%20')
        return url
def fetchdata(url):
    try:
        data=requests.get(url)
        return data
    except Exception as e:
        print("some error")
        print(e)
def parseData(text):
    try:
        soup=BeautifulSoup(text,features='html.parser')
        return soup
    except Exception as e:
        print('error while parsing')
        print(e)
def users(usernames):
    soup=None 
    try:
        data=fetchdata(get_url(usernames))
        if data.status_code==200:
            soup=parseData(data.text)
                    
        elif data.status_code==404:
            st.error('invalid username')
    except Exception as e:
        print(e)
    
    user_details=soup.find('div',attrs={'class':"h-card mt-md-n5"})
    
    st.image(user_details.find('img').attrs.get('src'),caption="profile photo")
    st.header("FULL NAME")
    st.write(user_details.find('span',attrs={'class':'p-name vcard-fullname d-block overflow-hidden'}).text)
    try:
        st.title('user status')
        st.image(soup.find('g-emoji').attrs.get('fallback-src'),)
        st.write(soup.find('div',attrs={'class':'user-status-message-wrapper f6 color-text-primary ws-normal lh-condensed'}).find('div').text)
    except Exception as e:
        st.info("sorry no status found!!")
    try:
        st.title("USER BIO")
        st.write(soup.find('div',attrs={'class':'p-note user-profile-bio mb-3 js-user-profile-bio f4'}).find('div').text)
    except Exception as e:
        st.info("sorry no bio found!!!")
    url2="https://github.com/"+usernames+"?tab=repositories"
    try:
        data2=fetchdata(url2)
        if data.status_code==200:
            soup2=parseData(data2.text)
                    
        else:
            print('no data found')
    except Exception as e:
        print(e)
    st.title("Repositories")
    name=soup2.find_all('div',attrs={'class':'col-10 col-lg-9 d-inline-block'})
    for r in name:
        st.header(r.find('a',attrs={'itemprop':'name codeRepository'}).text)
        # st.subheader(r.find('span',attrs={'itemprop':'programmingLanguage'}).text)
        st.write("URL : "+"https://github.com/"+r.find('a',attrs={'itemprop':'name codeRepository'}).get('href'))
    
    
st.title("GITHUB SCRAPER")

us=st.text_input("enter username")
btn=st.button("enter")

if btn:
    with st.spinner('loading output...'):
        users(us)
