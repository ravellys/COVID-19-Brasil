# COVID-19-Brasil

Este trabalho tem como objetivo modelar os casos do COVID-19 no Brasil por meio do modelo SUCQ. O modelo foi proposto por Zhao e Chen (2020)- https://doi.org/10.1007/s40484-020-0199-0, e foi utilizado para modelar os casos de COVID-19 Wuhan, Hubei (excluindo Wuhan) e a China (excluindo Hubei).

## Por que o modelo SUQC?

Dentre os modelos epidemiológicos (como SEIR, SIR, etc.) o modelo SUQC leva em consideração todas as particularidades do COVID-19:

* A epidemia tem uma probabilidade de infecção durante o período de incubação (pré-sintomático);
* Várias medidas de isolamento são usadas para controlar o desenvolvimento da epidemia; 
* A principal fonte de dados é o número diário de infecções confirmadas divulgadas no relatório oficial, afetado pelo método de detecção e com um atraso entre o número real infectado e o número infectado confirmado. 


O modelo leva em consideração o número de pessoas suscetíveis (S), pessoas infectadas em não quarentena (U), pessoas infectadas em quarentena (Q) e número total de confirmações dos casos (C) do COVID-19, e com eles, ainda pode ser estimado o número total de infectados (I = U + Q + C). Abaixo são demonstradas as EDOs que compõem o modelo: 

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/eq_SUCQ.JPG)
onde:
* alfa é a taxa de infecção
* gamma1 é a taxa de quarentena de um infectado não em quarentena sendo colocado em quarentena
* e R = alfa/gamma1 é o número de reprodução vírus

## Output do modelo 
Na Figura abaixo são demonstrados as variavéis de saída do modelo em uma simulação de 365 dias a partir do dia 18.

<imagem>
  
## Avaliação da mudança de tendência após as medidas de contenção social

A partir do dia 18 de março, em busca de conter a disseminação do COVID-19, a maior parte dos estados brasileiros adotaram medidas de isolamento social. Desse modo a Figura abaixo busca demonstrar o impacto  das medidas de isolamento na tendência do aumento de Casos no Brasil e nos estados Ceará e Pernambuco.  

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/cum_cases.png)

## Simulação do pico de infectados

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/daily_cases.png)

## Simulação do número de Reprodutividade (R0)

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/R0.png)



## Avaliação da Letalidade 

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/mortality.png)

## Avaliação da Letalidade (com o número total de infectados estimados pelo SUQC)

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/mortality_real_estimada.png)

## Estimativa do total de Mortes

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/total%20de%20mortes.png)





