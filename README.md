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
Na Figura abaixo são demonstrados as variavéis de saída do modelo em uma simulação de 365 dias.

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/imagens/plot_sucq/COVID-19%20Brazil.png)
  
## Avaliação da mudança de tendência após as medidas de contenção social

A partir do dia 18 de março, em busca de conter a disseminação do COVID-19, a maior parte dos estados brasileiros adotaram medidas de isolamento social. Desse modo a Figura abaixo busca demonstrar o impacto  das medidas de isolamento na tendência do aumento de Casos no Brasil e nos estados Ceará e Pernambuco. Nota-se um grande impacto no crescimento de casos, no Brasil houve uma diminuição de cerca de 10 vezes, e em ambos estados o impacto foi muito maior. 

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/imagens/cum_cases.png)

Nota-se também que o número de casos estimados com a tendência inicial em ambos estados superou o total de casos no Brasil, o que é fisicamente impossível já que esses casos estão inseridos dentro do total de casos brasileiros. Isso ocorreu pelo fato do número de casos totais (antes do dia 18 de março) do Brasil serem marjoritariamente composto por casos do estado de São Paulo (primeiro epicentro da doença) o que tornou a influencia dos outros estados mínimas na curva brasileira. Contudo, esses estados inicialmente apresentaram uma grande taxa de reprodução do vírus, na qual o mesmo dobrava a cada dia no Ceará e ficou cerca de oito vezes maior (após 5 dias) em Pernambuco. Por tanto, medidas de distânciamento social são primordiais no combate a disseminação do vírus, além disso, com essas medidas é possível retardar o número de epicentros.

## Projeção para o total de infectados no dia 14/04/2020

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/imagens/cases_7d_barplot.png)

## Simulação do pico de infectados

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/imagens/daily_cases/daily_cases.png)
![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/imagens/diamax_barplot.png)
![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/imagens/max_cases_barplot.png)

## Simulação do número de Reprodutividade (R0)

Um dos índices mais importande no combate a disseminação viral é o número de Reprodutividade. o R0 nos indica a taxa média de contaminação de pessoas por um infectado. Na Figura abaixo é apresentado o R0 no Brasil e nos seus estados.

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/imagens/R_barplot.png)

## Avaliação da Letalidade 

Na Figura abaixo é demonstrada a letalidade atual do vírus, do qual foi calculada a partir da razão entre o número total de óbitos e o número total de casos confirmados. 

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/imagens/mortality.png)

No geral, três aspectos são os de maior influência na Letalidade do vírus em uma nação/estado:

1. A pirâmide etária do país, da qual indicará o número de pessoas acima de 60 anos (que fazem parte do grupo de risco);
2. O número de pessoas com comorbidades que as tornem mais sensiveis ao vírus;
3. O número de testes para detecção do vírus no país.

O primeiro aspecto pode ser observado em países Europeus como a Itália e a Espanha, dos quais apresentam uma grande quantidade de óbitos por terem um país com uma grande quantidade de Idosos (cerca de 85% do total de óbitos no Brasil). Atualmente, a motalidade desses países são aproximadamente de 12% e 9%, o que é de 2 a 3 vezes maior que a apresentada atualmente pelo Brasil. Além disso, no Brasil cerca de 82% dos óbitos estão relacionados com pessoas com algum tipo de comorbidade (o que corrobora com o segundo aspecto). Devido a isso, além de aumentar o número de óbitos no grupo de idosos, as comorbidades também facilitam o óbito de pessoas mais jovens .

Os dois primeiros aspectos aumentam a letalidade por aumentar o número vítimas do vírus, contudo, o terceiro aspecto se diferencia por aumentar o monitoramento do número de casos, que por consequência diminui a letalidade. Países como a Alemanha e a Corea do Sul estão ganhando grande destaque no combate a ploriferação do vírus deivido ao grande número de teste que estão sendo realizados. Graças a isso, esses países estão conseguindo detectar um grande número de pessoas pré-sintomáticas resultando em taxas de letalidade de cerca de 1%. Esse fato, além de "contribuir" para a diminuição da letalidade, diminui as chances de uma pessoa assintomática transmitir o vírus pela falta de confinamento.

Contrário a isso, o Brasil, até o momento, não possui capacidade estrutual de realizar um grande quantitativo de teste. Esse fato dificulta a visualização do real cenário de infectados no país, o que por sua vez fornece estimativas errôneas da capacidade ploriferação do vírus. Contudo, o modelo SUQC é capaz de fornecer uma estimativa do total de infectados (I). Com isso, podemos estimar a verdadeira letalidade do vírus, como demonstrado na Figura abaixo:

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/imagens/mortality_real_estimada.png)

Nota-se que, em relação a letalidade calcula a partir dos casos confirmados, houve uma redução de cerca de três vezes para o Brasil. Nessa nova avaliação o país apresentou de 0.4% de letalidade, deixando bem próximo da taxa de letalidade de países com maior potencial de detecção de pessoas pré-sintomáticas como a Alemanha (menos de 1%). Isso indica que o modelo apresenta grande capacidade em estimar o número de pessoas pré-sintomáticas que não estão em confinamento (U). Isso o torna uma ferramenta crucial para a tomada de decisões a respeito da intensificação ou não do isolamento social. 

## Estimativa do total de Mortes

A partir das taxas de letalidade obtidas pelo modelo SUQC, foi possível estimar a quantidade total de óbitos ao fim da simulação (dia 01/04/2021). 

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/imagens/total%20de%20mortes.png)

É importante lembrar que o Brasil atualmente tem poucos centros de ploriferação do vírus (como São Paulo) o que pode levar a subestimativa dos valores totais de mortes. Além disso, com a chegada dos novos testes ( dia 2 de abril) é possível que a dinâmica de casos confirmados seja alterada o que irá alterar significativamente as estimativas de reprodutividade do vírus e, por consequência, o número total de mortos. 

## Reprodutividade do vírus ao longo do tempo

Na figura abaixo é demonstrado o aumento do número de reprodução do vírus ao longo do tempo. É possível notar que o Brasil vem tendo uma tendência de decaimento, enquanto que o estado de Pernambuco tem uma tendência de crescimento.

![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/imagens/R0_time/R0_estad.png)
![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/imagens/R0_time/PE.png)
![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/imagens/R0_time/CE.png)
![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/imagens/R0_time/AM.png)
![Image of EDOSUCQ](https://github.com/ravellys/COVID-19-Brasil/blob/master/imagens/R0_time/SP.png)










