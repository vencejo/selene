import ConfigParser
import tweepy
import os


class Noticias():
    
    def __init__(self):
        self.get_config()
        
    def get_config(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        config = ConfigParser.ConfigParser()
        config.read('datosCuentaTwitter.ini')
        APP_KEY = config.get('datosTwitter', 'APP_KEY')
        APP_SECRET = config.get('datosTwitter', 'APP_SECRET')
        OAUTH_TOKEN = config.get('datosTwitter', 'OAUTH_TOKEN')
        OAUTH_SECRET = config.get('datosTwitter', 'OAUTH_TOKEN_SECRET')
        auth = tweepy.OAuthHandler(APP_KEY, APP_SECRET)
        auth.set_access_token(OAUTH_TOKEN, OAUTH_SECRET)
        self.api = tweepy.API(auth)

    def daNoticias(self, numNoticias = 5):
        
        noticias = self.api.home_timeline(count=numNoticias) #Coge 6 tweets
        listaNoticias = []
        for tweet in noticias:
            #Elimina los enlaces
            indice = tweet.text.find("http")
            if indice != -1:
                noticia = tweet.text[:indice]
            else:
                noticia = tweet.text
            
            listaNoticias.append(noticia)
            
        return listaNoticias
        
if __name__ == "__main__":
    
    n = Noticias()
    print(n.daNoticias())
        
