
import pandas as pd 
import numpy as np
import streamlit as st
from PIL import Image
import os

class StreamlitApp:
    
    def __init__(self):
        self.model = load_model('model/final_model_boxoffice') 
        self.save_fn = 'path.csv'     
        
    def predict(self, input_data): 
        return predict_model(self.model, data=input_data)
    
    def store_prediction(self, output_df): 
        if os.path.exists(self.save_fn):
            save_df = pd.read_csv(self.save_fn)
            save_df = save_df.append(output_df, ignore_index=True)
            save_df.to_csv(self.save_fn, index=False)
            
        else: 
            output_df.to_csv(self.save_fn, index=False)  
            
    
    def run(self):
        image = Image.open('assets/box.jpg')
        st.image(image, use_column_width=False)
    
    
        add_selectbox = st.sidebar.selectbox('How would you like to predict?', ('Online', 'Batch')) #bruke batch for aa predikere paa alle bildene. 
        st.sidebar.info('This app is created to predict box office revenue' )
        st.sidebar.success('DAT158*')
        st.title('Box office prediction')
        
       
        if add_selectbox == 'Online': 
            budget = st.number_input('Budget', min_value=10000, max_value=1000000000, value=50000) #remember trained on age between ...
            genres = st.selectbox('Genres', ['Drama', 'Comedy', 'Thriller', 'Action', 'Romance', 'Crime', 'Adventure', 'Horro', 'ScienceFiction', 'Family', 'Fantasy', 'Mystery', 'Animation', 'History', 'War', 'Music', 'Documentary', 'Western', 'Foreign', 'TVMovie'])
            popularity = st.number_input('Popularity in %', min_value=0, max_value=100, value=10)
            runtime = st.number_input('Runtime in min', min_value=10, max_value=200, value=90)            

            output=''
            input_dict = {'Budget':budget, 'Genres':genres, 'Popularity':popularity, 'Runtime':runtime}
            input_df = pd.DataFrame(input_dict, index=[0])
        
            if st.button('Predict'): 
                output = self.predict(input_df)
                self.store_prediction(output)
                
                output = str(output['Label'][0]) 
                
            
            st.success('Predicted output: {}'.format(output))
            
        if add_selectbox == 'Batch': 
            fn = st.file_uploader("Upload csv file for predictions") #st.file_uploader('Upload csv file for predictions, type=["csv"]')
            if fn is not None: 
                input_df = pd.read_csv(fn)
                predictions = self.predict(input_df)
                st.write(predictions)
            
sa = StreamlitApp()
sa.run()
