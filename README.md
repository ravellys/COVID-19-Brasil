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

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/plot_sucp/COVID-19%20Brasil.png)
  
## Avaliação da mudança de tendência após as medidas de contenção social

A partir do dia 18 de março, em busca de conter a disseminação do COVID-19, a maior parte dos estados brasileiros adotaram medidas de isolamento social. Desse modo a Figura abaixo busca demonstrar o impacto  das medidas de isolamento na tendência do aumento de Casos no Brasil e nos estados Ceará e Pernambuco. Nota-se um grande impacto no crescimento de casos, no Brasil houve uma diminuição de cerca de 10 vezes, e nos estados houve uma diminuição de quase 1000 vezes. É importante salientar que o estados, CE e PE, tomaram medidas de restrição social na primeira semana de epidemia, esse fato mostrou-se primordial no combate a disseminação do vírus.

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/cum_cases.png)

## Simulação do pico de infectados

Com o modelo também foi possível simular o pico dos casos. É possível notar que houve um grande achatamento da curva no estado de Pernambuco, do qual apresenta o pico no mês de dezembro. No Ceará o pico foi simulado para entre o mês de maio e junho, também é possível notar que o mesmo apresenta uma curva com grande incidências diárias.

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/daily_cases.png)

## Simulação do número de Reprodutividade (R0)

Um dos índices mais importande no combate a disseminação viral é o número de Reprodutividade. o R0 nos indica a taxa média de contaminação de pessoas por um infectado. Na Figura abaixo é apresentado o R0 em no Brasil e nos seus estados. Nota-se que o Amapá (AP) é o que apresenta maior R0 (próximo a 6), nesse estado o número de casos tem uma grande taxa de crescimento, na qual tende a dobrar entre 2 e 3 dias.

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/R0.png)

## Avaliação da Letalidade 

Na Figura abaixo é demonstrada a letalidade atual do vírus, do qual foi calculada a partir da razão entre o número total de óbitos e o número total de casos confirmados. Nota-se que o estado com a maior letalidade é o Piauí (PI) (com cerca de 17%), contudo o estado só apresentou até agora cerca de 23 casos confirmados. o Brasil apresenta cerca de 4.4% de taxa de letalidade, índice próximo ao apresentado na China (país de origem da doença). Até agora, os estados do Acre e Tocantins não apresentaram óbitos pelo COVID-19.

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/mortality.png)

No geral, três aspectos são os de maior influência na Letalidade do vírus em uma nação/estado:

1. A pirâmide etária do país, da qual indicará o número de pessoas acima de 60 anos (que fazem parte do grupo de risco);
2. O número de pessoas com comorbidades que as tornem mais sensiveis ao vírus;
3. O número de testes para detecção do vírus no país.

O primeiro aspecto pode ser observado em países Europeus como a Itália e a Espanha, dos quais apresentam uma grande quantidade de óbitos por terem um país com uma grande quantidade de Idosos. Atualmente, a motalidade desses páises são aproximadamente de 12% e 9%, o que é de 2 a 3 vezes maior que a apresentada atualmente pelo Brasil. Além disso, no Brasil cerca de 85% dos óbitos estão relacionados com pessoas com algum tipo de comorbidade (o que corrobora com o segundo aspecto). Devido a isso, além de aumentar o número de óbitos no grupo de idosos, as comorbidades acabam levandofacilitando o óbito de pessoas mais jovens também.

Os dois primeiros aspectos aumentam a letalidade por aumentar o número vítimas do vírus, contudo, o terceiro aspecto se diferencia por aumentar o monitoramento do número de casos, que por consequência diminui a letalidade. Países como a Alemanha e a Corea do Sul estão ganhando grande destaque no combate a ploriferação do vírus pelo grande número de teste que estão sendo realizados. Graças a isso, esses países estão conseguindo detectar um grande número de pessoas pré-sintomáticas resultando em taxas de letalidade de cerca de 1%. Esse fato, além de "contribuir" para a diminuição da letalidade,

Contrário a isso, o Brasil, até o momento, não possui capidade estrutual de realizar um grande quantitativo de teste. Esse fato dificulta a visualização do real cenário de infectados no país, o que por sua vez fornece estimativas errôneas da capacidade ploriferação do vírus. Contudo, o modelo SUQC é capaz de fornecer uma estimativa do total de infectados (I). Com isso, podemos estimar a verdadeira letalidade do vírus, como demonstrado na Figura abaixo:

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/mortality_real_estimada.png)

Nota-se que, em relação a letalidade calcula a partir dos casos confirmados, houve uma redução de cerca de três vezes para o Brasil. Nessa nova avaliação o país apresentou de 1.5% de letalidade, deixando bem próximo da taxa de letalidade de países com maior potencial de detecção de pessoas pré-sintomáticas como a Alemanha (cerca de 1%). Isso indica que o modelo apresenta grande capacidade em estimar o número de pessoas pré-sintomáticas que não estão em confinamento (U). Isso o torna uma ferramenta crucial para a tomada de decisões a respeito da intensificação ou não do isolamento social. 

## Estimativa do total de Mortes

A partir das taxas de letalidade obtidas pelo modelo SUQC, foi possível estimar a quantidade total de óbitos ao fim da simulação (dia 18/03/2021). Estimasse um total de 544 mil mortes no Brasil ao final desse período, na qual a maior parte será do estado de São Paulo (144 mil) seguido pela Bahia (59.5 mil). 

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/total%20de%20mortes.png)

É importante lembrar que o Brasil atualmente tem poucos centros de ploriferação do vírus (como São Paulo) o que pode levar a subestimativa dos valores totais de mortes. Além disso, com a chegada dos novos testes ( dia 2 de abril) é possível que a dinâmica de casos confirmados seja alterada o que irá alterar significativamente as estimativas de reprodutividade do vírus e, por consequência, o número total de mortos. 





