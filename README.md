# Computação gráfica - Ray tracing

O trabalho consistiu na implemetação do algoritmo de ray tracing. Para isso, foi utilizado um guia de implementação, o livro "Ray Tracing in one Weekend" do Peter Shirley. O guia mostrou passo-a-passo como o ray tracing poderia ser implementado, utilzando exemplos de código em C++. Assim, a tarefa desse TP foi a de adaptar o código para python. Para realizar essa tarefa, utilizou-se bibliotecas para a manipulaçao de entrada/saida, vetores, operações matématicas e de métodos probabilísticos, além de Classes em python.

Para ler os parâmetros de execução, foi utilizado a biblioteca sys. Foi possível ler esses parâmetros através da lista sys.args.

O formato escolhido para a imagem resultante do programa foi o ppm, pois imagens nesse formato são simples de serem escritas. Os comandos utilizados para a manipulação do arquivo de saída foram as funções open(file, mode) e file.write().

Para a implementação do código foi necessário utilizar vetores. Isso foi feito por meio do uso da biblioteca numpy. Boa parte das operações utilizadas no trabalho são facilmente realizáveis através dessa biblioteca. Contudo, foi implementado as seguintes funções padrões: norm, unitVector e squareLength.

Para auxiliar a simular os efeitos físicos que ocorrem em determinados materias quando um raio de luz entra em contato com uma superfície, forarm definidas as funções reflect, refract, schlick, randomInunitSphere, randomInUnitDisk.

Todos os métodos que necessitaram de um resultado aleatório utilizaram a função uniform(0,1) da biblioteca random para gerar um número aleatório em uma distribuição uniforme.

Alguns métodos precisaram dos cálculos de senos, cossenos e tangentes. Para isso foi utilizado a biblioteca math.

Assim como no código presente no livro, foram utilizadas classes para a representação de elementos no processo de ray tracing. Contudo, houveram algumas diferenças. Não foi criado nenhuma classe de interface, pois a assinatuara dos métodos em python são resolvidas em tempo de execução. Além disso, foram criadas classes o retorno de objetos e a passagem de parâmetros.

As classes utilizadas foram as seguintes:
- Ray: presenta um raio de luz. Possui origem e direção, sendo possível dispará-lo
- HitRecord: representa todos os dados sobre o acerto de um raio em um objeto (se deu certo, t, ponto de colosiao, normal e material).
- ScatterRecord: representa todos os dados de uma colisão de um raio em um material (se deu certo, para onde foi o raio, albedo).
- Lambertian, Metal e Dielectric: representam o tipo de material com seus respectivos ScatterRecords.
- Sphere, HitableList: representam objectos com seus respectivos hitRecords.
- Camera: representa a camera utilizada no ray tracing com os dados necessários para montar sua posição e seu plano de visão.
- RefractData: representa o parametro utilizado para refratar um vetor;

Além disso tudo, foram utilizados 3 métodos principais: a main, com o fluxo principal de execução; o calculateColor, que calcula a cor gerada por um raio dado um determinado limite de profundidade (foi utilizada proifundidade 8); e o randomScene, que gera um mundo de 500 esferas aleatórias (menos as 3 maiores).

## Execução

O programa principal pode ser executado através de 3 opções diferentes de comando:

```sh
python ray_tracing.py
```
```sh
python ray_tracing.py nome_arquivo_de_saida nx ny
```
```sh
python ray_tracing.py nome_arquivo_de_saida nx ny ns
```
Nesses comandos, nx e ny representam, respectivamente, os números de pixel na horizontal e vertical da imagem. ns representa o número de raios disparados por pixel, para a realização do anti-aliasing. Caso os valores não sejam informados, o nome do arquivo de saída será "img.ppm", nx = 480, ny =340 e ns = 100.

## Resultados

Seguem alguns exemplos de imagens geradas por meio desse algoritmo:

![Primeira imagem](./outputs/img1.ppm)

![Segunda imagem](./outputs/img2.ppm)