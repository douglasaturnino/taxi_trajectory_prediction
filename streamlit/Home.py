import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🚕"
)

st.write( "# Previsão de Trajetória de Táxi" )

st.markdown(
    """
        O projeto foi desenvolvido para prever destinos de táxis na cidade do Porto, em Portugal.

        ## Como usar o painel
        
        Para o campo "Call Type", que identifica a forma de solicitação do serviço, há três opções que influenciam nos campos "Origin Call" e "Origin Stand" abaixo:

        - 'A': se a viagem foi despachada da central, o campo Origin Stand não é permitido;
        
        - 'B': se a viagem foi solicitada diretamente a um taxista em um ponto específico, o campo Origin Call não é permitido;
        
        - 'C': caso contrário (ou seja, uma viagem solicitada em uma rua aleatória), os campos Origin Call e Origin Stand não são permitidos.

        Para inserir as coordenadas de latitude e longitude, existem duas formas de fazê-lo:

        Digitando a latitude e longitude nos campos;
        
        Clicando no mapa para buscar automaticamente a latitude e longitude.
        
        Após pressionar o botão de previsão, o resultado é exibido em uma tabela e em um mapa, onde a latitude e longitude inicial são marcadas com um marcador azul, e a latitude e longitude previstas pelo modelo são marcadas com um marcador vermelho.

        Limitações:
        
        O mapa é atualizado cada vez que o mouse passa sobre ele, o que faz com que o resultado da previsão desapareça.
    """
)
