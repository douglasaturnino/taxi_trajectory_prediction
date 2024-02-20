Este é um projeto fictício. A empresa, o contexto e as perguntas de negócios não são reais.
O painel com os produtos de dados pode ser acessado via [streamlit](https://taxitrajectoryprediction.streamlit.app/)
O notebook com todos os passos realizados está disponivel [aqui](https://github.com/douglasaturnino/taxi_trajectory_prediction/blob/main/notebooks/taxi.ipynb).
O dataset está disponivel no [Kaggle](https://www.kaggle.com/competitions/pkdd-15-predict-taxi-service-trajectory-i).



## 1. O problema de negócio
### 1.1 Problema

A indústria de táxis está evoluindo rapidamente. Novos concorrentes e tecnologias estão mudando a forma como os serviços de táxi tradicionais fazem negócios. Embora esta evolução tenha criado novas eficiências, também criou novos problemas.

Uma mudança importante é a adoção generalizada de sistemas de despacho eletrônico que substituíram os sistemas de despacho de rádio VHF de tempos passados. Esses terminais móveis de dados são instalados em cada veículo e normalmente fornecem informações sobre localização GPS e estado do taxímetro. Os sistemas de despacho eletrônico facilitam a visualização de onde um táxi esteve, mas não necessariamente para onde está indo. Na maioria dos casos, os taxistas que operam com sistema de despacho eletrônico não indicam o destino final da viagem atual.

Outra mudança recente é a mudança de mensagens de rádio baseadas em transmissão (um para muitos) para despacho de serviço para mensagens baseadas em unicast (um para um). Com mensagens unicast, o despachante precisa identificar corretamente qual táxi deve despachar para o local de coleta. Como os táxis que utilizam sistemas de despacho eletrônico geralmente não informam o local de entrega, é extremamente difícil para os despachantes saber qual táxi contatar.

Para melhorar a eficiência dos sistemas electrónicos de despacho de táxis é importante ser capaz de prever o destino final de um táxi enquanto este está em serviço. Particularmente durante períodos de alta demanda, muitas vezes há um táxi cuja corrida atual terminará próximo ou exatamente no local de retirada solicitado por um novo passageiro. Se um despachante soubesse aproximadamente onde seus motoristas de táxi terminariam suas viagens atuais, ele seria capaz de identificar qual táxi atribuir a cada solicitação de coleta.


### 1.2 Desafio 
Neste desafio, pedimos-lhe que construa uma estrutura preditiva que seja capaz de inferir o destino final das corridas de táxi no Porto, Portugal, com base nas suas trajetórias parciais (iniciais). A saída desse quadro deve ser o destino final da viagem (coordenadas WGS84).

### 1.2 Motivação
Como os táxis que utilizam sistemas de despacho eletrônico geralmente não informan o local de entrega, é extremamente difícil para os despachantes saber qual táxi contatar.

### 1.3 Demandas de negócio
Produto de dados solicitado:
- inferir o destino final das corridas de táxi

## 2. Premissas de negócio
O despachante gostaria de saber aproximadamente onde seus motoristas de táxi terminariam suas viagens atuais.

As variáveis do dataset são:

| Variável     | Descrição                                                                                               |
|--------------|---------------------------------------------------------------------------------------------------------|
| TRIP_ID      | (String) Contém um identificador único para cada viagem;                                                |
| CALL_TYPE    | (char) Identifica a forma utilizada para demandar este serviço. Pode conter um dos três valores possíveis: 
|              |  'A' se esta viagem foi despachada da central;                                                          |
|              |  'B' se esta viagem foi solicitada diretamente a um taxista em ponto específico;                       |
|              |  'C' caso contrário (ou seja, uma viagem exigida em uma rua aleatória).                                 |
| ORIGIN_CALL  | (inteiro) Contém um identificador único para cada número de telefone que foi utilizado para demandar, pelo menos, um serviço. Identifica o cliente da viagem se CALL_TYPE='A'. Caso contrário, assume um valor NULL; |
| ORIGIN_STAND | (inteiro): Contém um identificador único do ponto de táxi. Identifica o ponto inicial da viagem se CALL_TYPE='B'. Caso contrário, assume um valor NULL; |
| TAXI_ID      | (inteiro): Contém um identificador único do taxista que realizou cada viagem;                           |
| TIMESTAMP    | (inteiro) carimbo de data/hora Unix (em segundos). Identifica o início da viagem;                       |
| DAYTYPE      | (char) Identifica o tipo de dia de início da viagem. Ele assume um dos três valores possíveis:          |
|              | - 'B' se esta viagem começou num feriado ou em qualquer outro dia especial (ou seja, feriados prolongados, feriados flutuantes, etc.); |
|              | - 'C' se a viagem começou um dia antes de um dia tipo B;                                                  |
|              | - 'A' caso contrário (ou seja, um dia normal, dia útil ou fim de semana).                                |
| MISSING_DATA | (Booleano) É FALSE quando o fluxo de dados GPS está completo e TRUE sempre que um (ou mais) locais estão faltando; |
| POLYLINE     | (String): Contém uma lista de coordenadas GPS (ou seja, formato WGS84) mapeadas como uma string. O início e o fim da string são identificados entre colchetes (ou seja, [ e ], respectivamente). Cada par de coordenadas também é identificado pelos mesmos colchetes que [LONGITUDE, LATITUDE]. Esta lista contém um par de coordenadas para cada 15 segundos de viagem. O último item da lista corresponde ao destino da viagem enquanto o primeiro representa o seu início; |

### 3.1 Produto final
O que será entregue efetivamente?
- Um painel mostrando o ponto de inicio e a previsão do taxi.

 ### 3.2 Ferramentas
 Quais ferramentas serão usadas no processo?
- Visual Studio code;
- Jupyter Notebook;
- Git, Github;
- Python;
- Cloud Render.

 ## 4. Os 3 principais insights dos dados

#### 1 Viagens em diferentes horários do dia têm Distancia médias diferentes.
**Verdadeira**: As distancias médias nos horarios entre 3 e 7 tem uma distancia média maior.

#### 2 O tipo de chamada ('call_type') influencia na distância média das viagens ao longo dos meses.
**False** O tipo de chamada durante os meses sempre ficam na ordem C > A > B

#### 3 A quantidade de viagens entre o ponto de origem e o ponto de destino (distance) é inferior a 5 km.
**Verdadeira**: A quantidade de viagens inferior a 5km é maior.

## 5. E quanto da isso em R$

- Carros a gasolina: Cerca de 6 a 10 litros por 100 km, dependendo do modelo.
- Gasolina: Cerca de 1,60 a 1,80 euros por litro.
- Suponha um carro a gasolina com um consumo médio de 8 litros/100 km.
- Se o preço da gasolina for 1,70 euros por litro, o custo por quilômetro seria aproximadamente 0,136 euros

Quantidade de viagens: 1.710.670
- Km ate passageiro: 1,5km
- Quantidade gasta com gasolina: 1.710.670 * 0,136 * 1,5 = 348.976,68


Com 1 km
- 1.710.670 * 0,136 * 1 = 232.651,12
- 348.976,68 - 232.651,12 = 116.325,56

Levando em consideração um diminuição de 500m em um periodo de um ano poderia ter uma economia de 116 mil euros

## 6. Resultados para o negócio
De acordo com os critérios definidos, foi feita uma previsão do destino final da viagem. Como resultado para o negócio foram criados:

* Uma API onde será feita a previsão do destino final da viagem.

* Um painel com um mapa com os marcadores de inicio da viagem e um marcador com a previsão do destino.


## 5. Conclusão
O objetivo ainda não foi alcançado, pois as previsões estão muito distantes do destino real.

