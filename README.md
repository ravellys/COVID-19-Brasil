# COVID-19-Brasil

Este trabalho tem como objetivo modelar os casos do COVID-19 no Brasil por meio do modelo SUCQ. O modelo foi proposto por Zhao e Chen (2020)- https://doi.org/10.1007/s40484-020-0199-0, e foi utilizado para modelar os casos de COVID-19 Wuhan, Hubei (excluindo Wuhan) e a China (excluindo Hubei). O modelo leva em consideração o número de pessoas suscetíveis (S), pessoas infectadas em não quarentena (U), pessoas infectadas em quarentena (Q) e número total de confirmações dos casos (C) do COVID-19. Abaixo são demonstradas as EDOs que compõem o modelo: 

![Image of EDOSUCQ](https://octodex.github.com/images/yaktocat.png)

onde:
* alfa é a taxa de infecção
* gamma1 é a taxa de quarentena de um infectado não em quarentena sendo colocado em quarentena
* e R = alfa/gamma1 é o número de reprodução vírus


