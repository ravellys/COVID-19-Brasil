# COVID-19-Brasil

Este trabalho tem como objetivo modelar os casos do COVID-19 no Brasil por meio do modelo SUCQ. O modelo foi proposto por Zhao e Chen (2020)- https://doi.org/10.1007/s40484-020-0199-0, e foi utilizado para modelar os casos de COVID-19 Wuhan, Hubei (excluindo Wuhan) e a China (excluindo Hubei). 

O modelo leva em consideração o número de pessoas suscetíveis (S), pessoas infectadas em não quarentena (U), pessoas infectadas em quarentena (Q) e número total de confirmações dos casos (C) do COVID-19. Abaixo são demonstradas as EDOs que compõem o modelo: 

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/eq_SUCQ.JPG)
onde:
* alfa é a taxa de infecção
* gamma1 é a taxa de quarentena de um infectado não em quarentena sendo colocado em quarentena
* e R = alfa/gamma1 é o número de reprodução vírus

## Output do modelo 

<imagem>
  
## Avaliação da mudança de tendência após as medidas de contenção social

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

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/total de mortes.png)





