#from ssl import ALERT_DESCRIPTION_BAD_CERTIFICATE_STATUS_RESPONSE
import time
import streamlit as st
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account	
from specklepy.objects import Base
from specklepy.transports.server import ServerTransport
from specklepy.api import operations
#from streamlit_autorefresh import st_autorefresh
#vo=st_autorefresh(interval=5000, limit=1e6, key="fizzbuzzcounter")
#ep=st_autorefresh(interval=5000, limit=1e6, key="fizzbuzzcounter")


#st.title("FIATLUX: un cas d'école")
st.markdown("<h1 style='text-align: center; color: Maroon;'>FIATLUX: cas minimalise</h1>", unsafe_allow_html=True)
st.markdown("""
L'objectif est d'illustrer les possibilités de mise en oeuvre pratique de FIATLUX dans le cloud, avec trois acteurs :
* Un script python qui génère le site utilisateur et qui assure les échanges avec les autres acteurs,
* un script julia qui assure l'optimisation
* Un script grasshopper qui assure la génération de l'objet 3D

Des applications plus complexes pourront être réalisées en partant de cet exemple "***hello world***" 
""" )  
st.write("Le cas d'école retenu consiste à calculer les caractéristiques d'un verre ayant le volume et l'épaisseur de paroi requis tout en minimisant la matière employée pour sa réalisation")

st.markdown("<h2 style='text-align: left; color: Maroon;'>Le modèle</h2>", unsafe_allow_html=True)

st.write("""Le rayon du verre est R, l'épaisseur de la paroi et du socle e, H est sa hauteur

**Volume du verre (intérieur):** *V= π(R-e)²*(H-e)* 

**Volume de la part matière**: *πR²e* (pour le socle du verre) *+ πR²(H-e)-π(R-e)²(H-e)*
(pour la paroi latérale). 
C'est cette quantité qu'il faut minimiser
""")

st.markdown("<h2 style='text-align: left; color: Maroon;'>Méthode de résolution</h2>", unsafe_allow_html=True)

st.markdown("""
* L'optimisation sous contraintes sera réalisée par un programme Julia. Ce programme minimisant la part matière pour atteindre le volume requis fournira les valeurs optimales pour R et H
* Un modèle paramétrique du verre, réalisé sous Grasshopper, fournira la représentation 3D du verre.
* Les échanges de données entre les divers logiciels mis en œuvre se feront de façon asynchrone à l'aide de Speckle 
* Le site sera réalisé à partir du logiciel streamlit


""")


#st.write("V=",V," e=",e)
st.markdown("""
On installe specklepy via le terminal:

```console
pip install specklepy
```

""")





class Block1(Base):
    volume: float
    epaisseur: float
    

    def __init__(self, volume, epaisseur, **kwargs) -> None:
        super().__init__(**kwargs)
        # mark the origin as a detachable attribute
        self.volume = volume
        self.epaisseur = epaisseur
 


st.markdown("<h2 style='text-align: left; color: Maroon;'>Envoi des données</h2>", unsafe_allow_html=True)


with st.form("my_form"):
    #st.write("Inside the form")
   
    V=st.number_input('Volume V du verre souhaité (cm ³)', 0, 1000,value=300)
    e=st.number_input('épaisseur e paroi (mm )', 0.10,5.0,value=1.5)
    
    #slider_val = st.slider("Form slider")
    #checkbox_val = st.checkbox("Form checkbox")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        #st.write("slider", slider_val, "checkbox", checkbox_val)
        # here's the data you want to send
#block = Block(length=2, height=4)
        block = Block1(volume=V, epaisseur=e)	


        # next create a server transport - this is the vehicle through which you will send and receive
        client = SpeckleClient(host="https://speckle.xyz/")
        new_stream_id="36b6a4554d"  # spécifique au projet ToyExampleV2_APIJulia

        account = get_default_account()
        client.authenticate_with_account(account)
        transport = ServerTransport(client=client, stream_id=new_stream_id)

        # this serialises the block and sends it to the transport
        hash = operations.send(base=block, transports=[transport])
        commid_id = client.commit.create(
            stream_id=new_stream_id, 
            object_id=hash, 
            message="V and e transmission",
            )
        st.write("Les nouvelles données ont été envoyées")
        
        
        
        
        #time.sleep(20)
        #"c9b24bc2de" -> fromGH
        #my_glass="""<iframe src="https://speckle.xyz/embed?stream=c9b24bc2de" width="600" height="400" frameborder="0"></iframe>"""
        
        #stream="https://speckle.xyz/embed?stream=c9b24bc2de"
        #if vo not in st.session_state:
        #  st.session_state.vo=300
        #  st.write(st.session_state.stream)
        #if V != st.session_state.vo: 
        #  st.session_state.vo=V
        #  st.write(st.session_state.vo)

        #if ep not in st.session_state:
        #  st.session_state.ep=0.5
        #  st.write(st.session_state.ep)
        #if e != st.session_state.ep: 
        #  st.session_state.ep=e
        #  st.write(st.session_state.ep)
        
        

#st.write("Outside the form")
st.markdown("<h2 style='text-align: left; color: Maroon;'>Récupération des données optimisées</h2> <par>  Puis rafraîchir la page</par> ", unsafe_allow_html=True)
view = st.button("view 3D")
if view:
    my_glass="""<iframe src="https://speckle.xyz/embed?stream=c9b24bc2de" width="600" height="400" frameborder="0"></iframe>"""
    st.markdown(my_glass, unsafe_allow_html=True)

refreshed = st.button("refresh")
if refreshed:
    ""


