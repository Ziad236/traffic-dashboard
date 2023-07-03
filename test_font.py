import matplotlib.font_manager
import numpy as np

font_list = matplotlib.font_manager.findSystemFonts()
# for font in font_list:
#     print(font)
# w np.array([10,20,20,50])

wide = 10  # Example value for the range of random integers

random_int = np.random.randint(low=0, high=wide)
print(np.arange(wide))
print(np.array(10*[10]))


    # fig_bar.update_layout(
    #     xaxis_title={
    #     'text': 'Metrics',
    #     'font': {
    #         'family': 'Arial',
    #         'size': 24,
    #         'color': 'blue'
    #     }
    # }

    # )
    
    
    # def Forcast_Benshmark(df, forcast_time='SVARMAX_60'):

    # df_filtered=df_filtered.loc[:,'SVARMAX_60']
    # df_melted = pd.melt(df_filtered, id_vars='Unnamed: 0', var_name='Model', value_name='Value')

    # # Sort the DataFrame by the 'Value' column in ascending order
    # df_melted_sorted = df_melted.sort_values('Value', ascending=True)

    # # Define a homogeneous color palette for the models
    # #color_palette = ['#00A7E2', '#808080', '#000000']
    # fig_bar = px.bar(df_melted_sorted, x='Unnamed: 0', y='Value', color='Model', barmode='group')
    #                 #  color_discrete_sequence=color_palette)

    # fig_bar.update_layout(
    #     # title='Bar Plot',
    #     xaxis_title='Metrics',
    #     yaxis_title='ERROR',
    #     plot_bgcolor='rgba(0,0,0,0)',
    #     paper_bgcolor='rgba(0,0,0,0)'
    # )

    # return fig_bar
def size_inferance(factor='time',data="RFR_metra"):
    if factor == 'time' :
        data = {
            'factor': ['Inference time'],
            'RFR_metra': [16],
            'RFR_pems': [12],
            'varmax_metra': [16],
            'varmax_pems': [480]
        }
        df = pd.DataFrame(data)
        df_melted = pd.melt(df, id_vars='factor', var_name='Model', value_name='Value')

        fig_bar = px.bar(df_melted, y='factor', x='Value', color='Model', barmode='group')

        fig_bar.update_layout(
            title='Bar Plot',
            xaxis_title='Time',
            yaxis_title='Values',
            plot_bgcolor='#A0C49D',
            paper_bgcolor='#A0C49D'
        )
        return fig_bar
    elif factor == 'size':
        data = {
            'time': ['Size'],
            'RFR_metr': [193],
            'varmax_metr': [985.6],
            'RFR_pems': [1331.2],
            'SVARMAX_pems': [34816]
        }
        df = pd.DataFrame(data)
        df_melted = pd.melt(df, id_vars='time', var_name='Model', value_name='Value')

        fig_bar = px.bar(df_melted, y='time', x='Value', color='Model', barmode='group')

        fig_bar.update_layout(
            title='Bar Plot',
            xaxis_title='Size',
            yaxis_title='Time in seconds',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig_bar